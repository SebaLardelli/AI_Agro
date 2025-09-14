import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

cliente = genai.Client(api_key=GOOGLE_API_KEY)

MODEL_ID = "gemini-2.0-flash" 

# text_to_process = """Estimado Amazon, la semana pasada pedí una figura de acción de Optimus Prime
# en su tienda en línea en Alemania. Desafortunadamente, cuando abrí el paquete,
# descubrí con horror que me habían enviado una figura de acción de Megatron
# en su lugar. Como enemigo de toda la vida de los Decepticons, espero que pueda
# entender mi dilema. Para resolver el problema, exijo un cambio de Megatron por
# la figura de Optimus Prime que pedí. Adjunto copias de mis registros relativos
# a esta compra. Espero tener noticias suyas pronto. Atentamente, Bumblebee."""

# print("\nTexto de entrada definido.")


# ## 1. Sumarizacion
# pregunta = f"""Sumariza el siguiente texto en dos oraciones de rapida lectura

# Texto: {text_to_process}
# """

# respuesta = cliente.models.generate_content(
#     model=MODEL_ID,
#     contents=[pregunta] 
# )
# print(respuesta.text)



##2. Clasificación de Sentimiento
# pregunta = f"""Clasificá el siguiente texto como positivo, negativo o neutral y explicá por qué:

# Texto: {text_to_process}
# """

# respuesta = cliente.models.generate_content(
#     model=MODEL_ID,
#     contents=[pregunta] 
# )
# print(respuesta.text)


##3. Reconocimiento de Entidades Nombradas (NER)
# prompt = f"""Extraé todas las entidades nombradas del siguiente texto (personas, organizaciones, lugares, objetos) y clasificálas:

# Texto: {text_to_process}
# """

# respuesta = cliente.models.generate_content(
#     model=MODEL_ID,
#     contents=[prompt]
# )
# print(respuesta.text)


##4. Respuesta a preguntas (Question Answering)
# pregunta = "¿Qué producto recibió el cliente?"
# contexto = text_to_process

# prompt = f"""Respondé la siguiente pregunta basada en el texto:

# Texto: {contexto}
# Pregunta: {pregunta}
# """

# respuesta = cliente.models.generate_content(
#     model=MODEL_ID,
#     contents=[contexto, pregunta]
# )
# print(respuesta.text)


##5. Resumen automático
# prompt = f"""Resumí el siguiente texto en no más de 3 líneas:

# Texto: {text_to_process}
# """

# respuesta = cliente.models.generate_content(
#     model=MODEL_ID,
#     contents=[prompt]
# )
# print(respuesta.text)


##6. Traducción (Español a Inglés)
# prompt = f"""Traducí al inglés este texto:

# Texto: {text_to_process}
# """

# respuesta = cliente.models.generate_content(
#     model=MODEL_ID,
#     contents=[prompt]
# )
# print(respuesta.text)


##7. Generación de respuesta (como atención al cliente)
# respuesta_inicial = "Estimado cliente, lamentamos mucho lo ocurrido con su pedido. "

# prompt = f"""{text_to_process}

# Redactá una respuesta del servicio de atención al cliente que comience así:

# "{respuesta_inicial}"

# Cuya extension no supere las 4 lineas.
# """

# respuesta = cliente.models.generate_content(
#     model=MODEL_ID,
#     contents=[prompt]
# )
# print(respuesta.text)


##8. Clasificación Zero-Shot (sin entrenamiento previo)
# etiquetas = ["queja", "elogio", "consulta", "pedido", "agradecimiento"]

# prompt = f"""Clasificá el siguiente texto en una de estas categorías: {', '.join(etiquetas)}. Justificá tu elección.

# Texto: {text_to_process}
# """

# respuesta = cliente.models.generate_content(
#     model=MODEL_ID,
#     contents=[prompt]
# )
# print(respuesta.text)

"""EJERCICIO"""

"""Escribí un texto corto sobre una experiencia personal en un transporte público en Buenos Aires.

Luego, generá:

- Un resumen.
- Una clasificación de sentimiento.
- Una lista de entidades nombradas."""


# texto_transporte_bsas = """Una tarde volviendo de la facultad, subí al colectivo 132 en el centro de 
# Buenos Aires. El micro iba lleno y apenas conseguí apoyarme cerca de la puerta.
# Entre el ruido del motor y las charlas, sonaba de fondo 
# la radio del chofer con un tango viejo. En cada parada subía más gente y 
# todos se iban acomodando como podían, con una mezcla de paciencia y resignación 
# típica de la ciudad. Cuando bajé en mi barrio, ya de noche, sentí que ese viaje 
# comprimía un pedacito de la vida porteña: el apuro, la cercanía con 
# desconocidos y esa energía que nunca se detiene."""

# preguntas = [
#     "Resumí el siguiente texto en dos oraciones de rapida lectura\n\n",
#     "Clasificá el siguiente texto como positivo, negativo o neutral y explicá por qué:\n\n",
#     "Extraé todas las entidades nombradas del siguiente texto (personas, organizaciones, lugares, objetos) y clasificálas:\n\n"
# ]


# for pregunta in preguntas: 
#     prompt = f"""{pregunta}Texto: {texto_transporte_bsas}"""
#     respuesta = cliente.models.generate_content(

#         model=MODEL_ID,
#         contents=[prompt] 

#     )

#     print(respuesta.text)

