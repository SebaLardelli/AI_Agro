import os
from dotenv import load_dotenv
from dataclasses import dataclass
from itertools import islice
from serpapi import GoogleSearch
from openai import OpenAI


load_dotenv()
SERP_API_KEY = os.getenv("SERP_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

@dataclass(frozen=True)
class SnippetCitation:
    Url: str
    Title: str
    Snippet: str

def serp_results(query: str, num=5, api_key=SERP_API_KEY):
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

client = OpenAI(api_key=OPENAI_API_KEY)

def chat_complete(
    syst: str | None,
    user: list[str] = [],
    assistant: list[str] = [],
    max_tokens: int = 1024,
    temperature: float = 0,
    model: str = "gpt-4o-mini",
) -> str:
    messages: list[dict[str, str]] = []
    if syst is not None:
        messages.append({"role": "system", "content": syst})
    for i in range(len(user)):
        messages.append({"role": "user", "content": user[i]})
        if len(assistant) > i:
            messages.append({"role": "assistant", "content": assistant[i]})
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    resultados = serp_results("Quién ganó las elecciones en Argentina 2023", num=5)
    contexto = "\n".join([f"- {r.Snippet}" for r in resultados])
    pregunta = "¿Quién ganó las elecciones presidenciales en Argentina en 2023?"
    prompt = f"Usá exclusivamente este contexto para responder la pregunta:\n{contexto}\n\nPregunta: {pregunta}\nRespuesta breve y directa:"
    respuesta = chat_complete(syst="Sos un asistente breve y factual.", user=[prompt])
    print(" Respuesta final:", respuesta)

# Respuesta final: Javier Milei ganó las elecciones presidenciales en Argentina en 2023.