import os
import json

from dataclasses import dataclass
from itertools import islice
from dotenv import load_dotenv
from serpapi import GoogleSearch
from openai import OpenAI


load_dotenv()
SERP_API_KEY = os.getenv("SERP_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)


@dataclass(frozen=True)
class SnippetCitation:
    url: str
    title: str
    snippet: str


def serp_results(query: str, num: int = 5, api_key: str = SERP_API_KEY):
    params = {
        "engine": "google",
        "q": query,
        "num": num,
        "hl": "es",
        "gl": "ar",
        "api_key": api_key,
    }
    search = GoogleSearch(params)
    res = search.get_dict()
    organic_results = res.get("organic_results", [])
    return [
        SnippetCitation(
            url=r.get("link", ""),
            title=r.get("title", ""),
            snippet=r.get("snippet", "")
        )
        for r in islice(organic_results, num)
    ]


def clean_markdown(content: str) -> str:
    if content is None:
        return ""
    content = content.strip()
    if content.startswith("```json"):
        content = content[len("```json"):].strip()
    elif content.startswith("```"):
        content = content[len("```"):].strip()
    if content.endswith("```"):
        content = content[:-3].strip()
    return content


def chat_complete(
    syst: str | None,
    user: list[str] = [],
    assistant: list[str] = [],
    max_tokens: int = 512,
    temperature: float = 0,
    model: str = "gpt-4o-mini",
    schema: dict | None = None
) -> str:
    messages: list[dict[str, str]] = []
    if syst is not None:
        messages.append({"role": "system", "content": syst})
    for i in range(len(user)):
        messages.append({"role": "user", "content": user[i]})
        if len(assistant) > i:
            messages.append({"role": "assistant", "content": assistant[i]})

    request_params = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }
    if schema is not None:
        request_params["response_format"] = {
            "type": "json_schema",
            "json_schema": {
                "name": "structured_response",
                "schema": schema,
                "strict": True
            }
        }

    resp = client.chat.completions.create(**request_params)
    return clean_markdown(resp.choices[0].message.content)


def build_context_block(snippets: list[SnippetCitation]) -> str:
    if not snippets:
        return "(sin resultados)"
    lines = []
    for i, s in enumerate(snippets, start=1):
        lines.append(
            f"{i}. Título: {s.title}\n   URL: {s.url}\n   Extracto: {s.snippet}"
        )
    return "\n".join(lines)


SYSTEM_RULES = (
    "Eres un asistente factual y breve. Responde SOLO usando el CONTEXTO provisto. "
    "Si el dato no está claramente en el contexto, responde con 'no lo sé'. "
    "Devuelve EXCLUSIVAMENTE el JSON que exige el schema (sin texto extra). "
    "Idioma: español."
)

PERSON_SCHEMA = {
    "type": "object",
    "properties": {
        "sobre": {"type": "string"},
        "nombre": {"type": "string"},
        "fallecio": {"type": "boolean"},
        "fecha_muerte": {"type": "string"},
        "tiempo_de_vida": {"type": "string"},
        "religion": {"type": "string"},
        "lugares_donde_vivio": {
            "type": "array",
            "items": {"type": "string"}
        },
        "evidencia": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "titulo": {"type": "string"},
                    "url": {"type": "string"}
                },
                "required": ["titulo", "url"],
                "additionalProperties": False
            }
        }
    },
    "required": ["sobre", "nombre", "fallecio", "tiempo_de_vida", "religion", "lugares_donde_vivio", "evidencia"],
    "additionalProperties": False
}



def build_user_prompt_for_person(topic: str, snippets: list[SnippetCitation]) -> str:
    context = build_context_block(snippets)
    return (
        f"TEMA: {topic}\n\n"
        "OBJETIVO: Extrae los datos pedidos sobre el 'papa argentino' del CONTEXTO.\n\n"
        "CONTEXTO (usa exclusivamente lo siguiente):\n"
        f"{context}\n\n"
        "Instrucciones de salida (JSON):\n"
        "- 'sobre': escribe literalmente 'papa argentino'.\n"
        "- 'nombre': nombre completo de la persona.\n"
        "- 'fallecio': true si el CONTEXTO indica que murió, false en caso contrario.\n"
        "- 'fecha_muerte': completa solo si 'fallecio' es true.\n"
        "- 'tiempo_de_vida': usa 'AAAA–AAAA' si falleció, o 'AAAA–presente' si está vivo.\n"
        "- 'religion': rama/orden de la religión (ej: Iglesia católica, jesuita).\n"
        "- 'lugares_donde_vivio': lista de ciudades/países.\n"
        "- 'evidencia': pares (titulo, url) del CONTEXTO."
    )



def get_person_info(topic: str = "papa argentino"):
    queries = [
        "papa argentino biografía",
        "papa argentino lugares donde vivió",
        "papa argentino nombre completo"
    ]

    snippets: list[SnippetCitation] = []
    seen = set()
    for q in queries:
        for s in serp_results(q, num=5):
            if s.url and s.url not in seen:
                seen.add(s.url)
                snippets.append(s)

    user_prompt = build_user_prompt_for_person(topic, snippets)

    raw = chat_complete(
        syst=SYSTEM_RULES,
        user=[user_prompt],
        model="gpt-4o-mini",
        schema=PERSON_SCHEMA
    )

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        data = {
            "sobre": topic,
            "nombre": "no lo sé",
            "fallecio": False,
            "tiempo_de_vida": "no lo sé",
            "religion": "no lo sé",
            "lugares_donde_vivio": [],
            "evidencia": []
        }

    if not data.get("evidencia"):
        data["evidencia"] = [
            {"titulo": s.title or "", "url": s.url or ""}
            for s in snippets[:5]
        ]

    return data


if __name__ == "__main__":
    info = get_person_info("papa argentino")
    print(json.dumps(info, ensure_ascii=False, indent=2))
