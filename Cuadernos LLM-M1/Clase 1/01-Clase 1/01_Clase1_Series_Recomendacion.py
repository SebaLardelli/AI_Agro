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
    Url: str
    Title: str
    Snippet: str

def serp_results(query: str, num: int = 5, api_key: str = SERP_API_KEY):
    # Devuelve una lista de SnippetCitation tomada de resultados orgánicos de Google vía SERPAPI.
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
            Url=r.get("link", ""),
            Title=r.get("title", ""),
            Snippet=r.get("snippet", "")
        )
        for r in islice(organic_results, num)
    ]


def limpiar_markdown(content: str) -> str:
    # Quita bloques de código Markdown (```...```) si existen.
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
    # Wrapper de Chat Completions. Si pasás `schema`, fuerza salida JSON con ese esquema.
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
                "strict": True  # exige cumplir "required" exactamente
            }
        }

    resp = client.chat.completions.create(**request_params)
    return limpiar_markdown(resp.choices[0].message.content)

# Prompt builders
def build_context_block(snippets: list[SnippetCitation]) -> str:
    if not snippets:
        return "(sin resultados)"
    lines = []
    for i, s in enumerate(snippets, start=1):
        lines.append(
            f"{i}. Título: {s.Title}\n   URL: {s.Url}\n   Extracto: {s.Snippet}"
        )
    return "\n".join(lines)

SYSTEM_RULES = (
    "Eres un asistente factual y breve. Responde SOLO usando el CONTEXTO provisto. "
    "Si el dato no está claramente en el contexto, responde: \"no lo sé\". "
    "Devuelve EXCLUSIVAMENTE el JSON que exige el schema (sin texto extra). "
    "Idioma: español."
)

# JSON Schema de salida
STREAMING_SCHEMA = {
    "type": "object",
    "properties": {
        "show": {"type": "string"},
        "platforms": {
            "type": "array",
            "items": {"type": "string"}
        },
        "availability_note": {"type": "string"},
        "confidence": {
            "type": "string",
            "enum": ["alta", "media", "baja", "no lo sé"]
        },
        "evidence": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "url": {"type": "string"}
                },
                "required": ["title", "url"],
                "additionalProperties": False
            }
        }
    },
    "required": ["show", "platforms", "availability_note", "confidence", "evidence"],
    "additionalProperties": False
}

def build_user_prompt_for_streaming(show: str, snippets: list[SnippetCitation]) -> str:
    pregunta = f"¿Dónde puedo ver la serie {show}?"
    contexto = build_context_block(snippets)
    return (
        f"PREGUNTA:\n{pregunta}\n\n"
        "CONTEXTO (usa exclusivamente lo siguiente):\n"
        f"{contexto}\n\n"
        "Instrucciones para el JSON:\n"
        "- 'show': el nombre exacto de la serie consultada.\n"
        "- 'platforms': lista de plataformas donde ver la serie (p. ej., Netflix, Prime Video, Max, Disney+, Apple TV+, Paramount+, etc.).\n"
        "- 'availability_note': breve nota (región/temporadas, alquiler/compra si aplica).\n"
        "- 'confidence': 'alta' si el contexto es claro y consistente; 'media' si hay indicios parciales; 'baja' si es dudoso; 'no lo sé' si no aparece.\n"
        "- 'evidence': títulos y URLs del contexto que sustentan la respuesta."
    )

# Función principal
def get_streaming_service(show: str):
    # 1) Traemos contexto 
    query = f"¿Dónde ver {show} online streaming?"
    snippets = serp_results(query, num=5)

    # 2) Armamos prompts
    user_prompt = build_user_prompt_for_streaming(show, snippets)

    # 3) Llamamos a chat_complete
    raw = chat_complete(
        syst=SYSTEM_RULES,
        user=[user_prompt],
        model="gpt-4o-mini",
        schema=STREAMING_SCHEMA
    )

    # 4) Parseo con fallback
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        data = {
            "show": show,
            "platforms": [],
            "availability_note": "",
            "confidence": "no lo sé",
            "evidence": []
        }

    # 5) Normalización
    data.setdefault("availability_note", "")
    return data

# Solo 5 para ahorrar costos
if __name__ == "__main__":
    shows = [
        "Breaking Bad",
        "The Office",
        "Game of Thrones",
        "Friends",
        "Stranger Things",
        "The Boys",
        "Dark"
    ]

    results = []
    for show in shows[:5]:
        info = get_streaming_service(show)
        results.append(info)
        plataformas = ", ".join(info["platforms"]) if info["platforms"] else "no lo sé"
        print(f"{info['show']}: {plataformas} (confianza: {info['confidence']})")

    print("\nJSON completo:")
    print(json.dumps(results, ensure_ascii=False, indent=2))

#Resupuesta 

''' 
Breaking Bad: Netflix, Prime Video, Apple TV (confianza: alta)
The Office (EE. UU.): Netflix, Amazon Prime Video, HBO Max (confianza: alta)
Game of Thrones: HBO Max, DIRECTV GO, Prime Video (confianza: alta)
Friends: Netflix, Prime Video, HBO Max, Apple TV+ (confianza: alta)
Stranger Things: Netflix, Apple TV (confianza: alta)

JSON completo:
[
  {
    "show": "Breaking Bad",
    "platforms": [
      "Netflix",
      "Prime Video",
      "Apple TV"
    ],
    "availability_note": "Puede que no esté disponible en todas las regiones.",
    "confidence": "alta",
    "evidence": [
      {
        "title": "Breaking Bad",
        "url": "https://www.netflix.com/ar/title/70143836"
      },
      {
        "title": "Breaking Bad - Season 01",
        "url": "https://www.primevideo.com/-/es/detail/Breaking-Bad/0KEKSTS1O6SJNXQ00DUZ7BPY7M"
      },
      {
        "title": "Breaking Bad",
        "url": "https://tv.apple.com/us/show/breaking-bad/umc.cmc.1v90fu25sgywa1e14jwnrt9uc?l=es"
      }
    ]
  },
  {
    "show": "The Office (EE. UU.)",
    "platforms": [
      "Netflix",
      "Amazon Prime Video",
      "HBO Max"
    ],
    "availability_note": "Actualmente disponible para streaming en varias plataformas.",
    "confidence": "alta",
    "evidence": [
      {
        "title": "The Office (EE. UU.)",
        "url": "https://www.netflix.com/ar/title/70136120"
      },
      {
        "title": "The Office - Season 1",
        "url": "https://www.primevideo.com/-/es/detail/The-Office/0H7JFOPK2QO9WVZ8D9D0J5ZRQN"
      },
      {
        "title": "Ver The Office",
        "url": "https://www.hbomax.com/ar/es/shows/78e15665-f6c8-4b58-8786-e0d9e2b65ced"
      },
      {
        "title": "The Office - Ver la serie online completas en español",
        "url": "https://www.justwatch.com/ar/serie/the-office"
      }
    ]
  },
  {
    "show": "Game of Thrones",
    "platforms": [
      "HBO Max",
      "DIRECTV GO",
      "Prime Video"
    ],
    "availability_note": "Disponible en streaming, sin opciones gratuitas.",
    "confidence": "alta",
    "evidence": [
      {
        "title": "Ver Game of Thrones (HBO)",
        "url": "https://www.hbomax.com/ar/es/shows/game-of-thrones/4f6b4985-2dc9-4ab6-ac79-d60f0860b0ac"
      },
      {
        "title": "Juego de tronos - Ver la serie de tv online",
        "url": "https://www.justwatch.com/ar/serie/juego-de-tronos"
      },
      {
        "title": "Game of Thrones, Season 7",
        "url": "https://www.primevideo.com/-/es/detail/Game-of-Thrones/0QP43Y6B2ZS1LVT6EBFMTIICOD"
      },
      {
        "title": "Juego de tronos",
        "url": "https://www.primevideo.com/-/es/detail/Juego-de-tronos/0GQTRXWTJFHS0DKID09GPGGYKY"
      }
    ]
  },
  {
    "show": "Friends",
    "platforms": [
      "Netflix",
      "Prime Video",
      "HBO Max",
      "Apple TV+"
    ],
    "availability_note": "Disponible en streaming en diferentes plataformas, dependiendo de la región.",
    "confidence": "alta",
    "evidence": [
      {
        "title": "Friends",
        "url": "https://www.netflix.com/gf-es/title/70153404"
      },
      {
        "title": "Friends, Season 1",
        "url": "https://www.primevideo.com/-/es/detail/Friends/0R9T1ZET44CYMTYM3CRF1C8UPM"
      },
      {
        "title": "Friends - Ver la serie online completas en español",
        "url": "https://www.justwatch.com/ar/serie/friends"
      },
      {
        "title": "Friends",
        "url": "https://tv.apple.com/ar/show/friends/umc.cmc.4dxfvjbc4rdww1dcp3kbgoaqm"
      }
    ]
  },
  {
    "show": "Stranger Things",
    "platforms": [
      "Netflix",
      "Apple TV"
    ],
    "availability_note": "Disponible en Netflix y Apple TV. No hay opciones gratuitas para ver.",
    "confidence": "alta",
    "evidence": [
      {
        "title": "Stranger Things | Sitio oficial de Netflix",
        "url": "https://www.netflix.com/es/title/80057281"
      },
      {
        "title": "Stranger Things - Ver la serie de tv online",
        "url": "https://www.justwatch.com/mx/serie/stranger-things"
      },
      {
        "title": "Stranger Things | Sitio oficial de Netflix",
        "url": "https://www.netflix.com/ar/title/80057281"
      },
      {
        "title": "Stranger Things - Ver la serie de tv online",
        "url": "https://www.justwatch.com/es/serie/stranger-things"
      },
      {
        "title": "Stranger Things",
        "url": "https://tv.apple.com/es/show/stranger-things/umc.cmc.6a4s868u4ocy2a9zg6ochi2nd"
      }
    ]
  }
] 
'''