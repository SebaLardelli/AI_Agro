import os
from openai import OpenAI
from dotenv import load_dotenv


OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

def get_completion(prompt, model="gpt-4.1",temperature=0):
    # Usamos la variable OPENAI_API_KEY cargada desde secrets o .env
    client = OpenAI(api_key=OPENAI_API_KEY)

    messages = [{"role": "user", "content": prompt}]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature, # grado de aleatoriedad
    )
    return response.choices[0].message.content

lamp_review = """
Necesitaba una lámpara bonita para mi habitación, y esta tenía \
almacenamiento adicional y no un precio demasiado alto. \
La recibí rápidamente. La cuerda de nuestra lámpara se rompió durante el \
tránsito y la compañía amablemente envió una nueva. \
Llegó también en pocos días. Fue fácil de armar. \
Tenía una pieza faltante, así que contacté a su \
soporte y muy rápidamente me enviaron la pieza que faltaba! \
¡Lumina me parece una gran empresa que se preocupa \
por sus clientes y productos!!
"""

prompt = f"""
Identifica los siguientes elementos del texto de la reseña:
- Sentimiento (positivo o negativo)
- ¿El revisor está expresando ira? (verdadero o falso)
- Artículo comprado por el revisor
- Compañía que fabricó el artículo

La reseña está delimitada con comillas triples invertidas. \
Formatea tu respuesta como un objeto JSON con \
"Sentimiento", "Ira", "Artículo" y "Marca" como las claves.
Si la información no está presente, usa "desconocido" \
como el valor.
Haz tu respuesta lo más corta posible.
Formatea el valor de Ira como un booleano.

Texto de la reseña: '''{lamp_review}'''
"""
response = get_completion(prompt)
print(response)
