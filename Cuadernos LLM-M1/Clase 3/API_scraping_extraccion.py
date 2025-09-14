import os
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
from dotenv import load_dotenv
from IPython.display import HTML, display, Markdown

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')


client = OpenAI(api_key=OPENAI_API_KEY)



# completion = client.chat.completions.create(
#     model="gpt-4o-mini",
#     messages=[
#         {"role": "user", "content": "Escribe una palabra relacionada al agro"}
#     ]
# )

# print(completion.choices[0].message.content)


# completion = client.chat.completions.create(
#     model="gpt-4o",
#     max_tokens=500,
#     messages=[
#         {"role": "user", "content": f"Genera una oracion breve que incluya la palabra 'cultivo' y sea de utilidad para la agricultura.'"}
#     ]
# )

# print(completion.choices[0].message.content)

"""LLM y variables"""

# nombre = "Otto Matic"
# edad_perro = 21/7

# completion = client.chat.completions.create(
#     model="gpt-4o",
#     max_tokens=500,
#     messages=[
#         {"role": "user", "content": f"""Si {nombre} fuera un perro, tendría {edad_perro} años.
#         Describe en qué etapa de la vida estaría ese perro y qué podría implicar en términos de nivel de energía, intereses y comportamiento."""}
#         ]
# )

# print(completion.choices[0].message.content)


"""Analisis de sentimiento"""

# completion = client.chat.completions.create(
#     model="gpt-4o",
#     max_tokens=500,
#     messages=[
#         {"role": "user", "content": f"Analiza el sentimiento del siguiente tweet: Thank you @AbiyAhmedAli for your warm welcome during my visit to Ethiopia. I'm inspired by our insightful discussions on Ethiopia's development progress, and I'm excited by the opportunity to continue supporting our partners to track and accelerate progress in health, agriculture and financial inclusion. @PMEthiopia"},
#     ]
# )

# print(completion.choices[0].message.content)


""""Chatbot"""

# historial_conversacion = []

# while True:
#     user_input = input("Usuario: ")

#     if user_input.lower() == "salir":
#         print("Conversación finalizada.")
#         break

#     historial_conversacion.append({"role": "user", "content": user_input})

#     completion = client.chat.completions.create(
#         model="gpt-4o",
#         messages=historial_conversacion,
#         max_tokens=500
#     )

#     respuesta_asistente_ai = completion.choices[0].message.content
#     print(f"Assistant: {respuesta_asistente_ai}")
#     historial_conversacion.append({"role": "assistant", "content": respuesta_asistente_ai})


#Funciones y LLM
###**Usando funciones en programas de IA**

"""Las funciones se pueden usar junto con variables en programas de IA. 
En la celda de abajo, vas a usar variables y la función `round()` 
para armar un prompt que vas a usar para un LLM con la función `get_llm_response()`. 
La función `get_llm_response()` es re parecida a `print_llm_response()` 
(que usaste antes); la principal diferencia es que te devuelve un string como 
resultado en vez de solo mostrar la respuesta del LLM. 
De esta manera, podés guardar la respuesta del LLM en la variable `response`."""

#Ejemplo limpio

"""def traductor(palabra, idioma):
    completion = client.chat.completions.create(
      model="gpt-4o",
      max_tokens=1000,
      messages=[
          {"role": "user", "content": f"Traduce la palabra {palabra} al {idioma}.  Responde solo con la palabra traducida, nada más"}
      ]
  )
    return(completion.choices[0].message.content)

traductor("Niña", "aleman")"""

#Ejemplo con redondeo

# ""def obtener_respuesta_ia(prompt):
#       completion = client.chat.completions.create(
#         model="gpt-4o",
#         max_tokens=1000,
#         messages=[
#             {"role": "user", "content": prompt}
#         ]
#     )
#       return(completion.choices[0].message.content)


# nombre = "Tommy"
# papas = 4.75
# prompt = f"""Escribí un pareado sobre mi amigo {nombre} que tiene como {round(papas)} papas"""
# respuesta = obtener_respuesta_ia(prompt)
# print(respuesta)


# ingrediente_secreto = "ajo"
# numero_de_lineas = 5
# prompt = f"""Escribí una receta que utilice {ingrediente_secreto} que tiene como extension maxima {round(numero_de_lineas)}"""
# respuesta = obtener_respuesta_ia(prompt)
# print(respuesta)""


"""Trabajo con Listas y Funciones"""

#     """get_llm_response"""

# def obtener_respuesta_ia(prompt):
#       completion = client.chat.completions.create(
#         model="gpt-4o",
#         max_tokens=500,
#         messages=[
#             {"role": "user", "content": prompt}
#         ]
#     )
#       return(completion.choices[0].message.content)

# lista_amigos = ["Tommy", "Isabel", "Daniel"]

# prompt = f"""
# Escribí un conjunto de poemas de cumpleaños de cuatro líneas para mis amigos {lista_amigos}.
# Los poemas tienen que estar inspirados en la primera letra del nombre de cada amigo.
# """
# respuesta = obtener_respuesta_ia(prompt)

# print(respuesta

"""Automatizacion de tareas"""

# def obtener_respuesta_ia(prompt):
#       completion = client.chat.completions.create(
#         model="gpt-4o",
#         max_tokens=500,
#         messages=[
#             {"role": "user", "content": prompt}
#         ]
#     )
#       return(completion.choices[0].message.content)

# lista_de_tareas = [
# "Redactar un breve correo electrónico a mi jefe explicando que llegaré tarde a la reunión de mañana.",
# "Escribir un poema de cumpleaños para Otto, celebrando su cumpleaños número 28.",
# "Escribir una reseña de 300 palabras de la película 'La llegada'."
# ]

# tarea = lista_de_tareas[1]
# respuesta = obtener_respuesta_ia(tarea)
# print(respuesta)

"""Ciclos for"""

# def obtener_respuesta_ia(prompt):
#       completion = client.chat.completions.create(
#         model="gpt-4o",
#         max_tokens=500,
#         messages=[
#             {"role": "user", "content": prompt}
#         ]
#     )
#       return(completion.choices[0].message.content)

# lista_de_tareas = [
# "Redactar un breve correo electrónico a mi jefe explicando que llegaré tarde a la reunión de mañana.",
# "Escribir un poema de cumpleaños para Otto, celebrando su cumpleaños número 28.",
# "Escribir una reseña de 300 palabras de la película 'La llegada'."
# ]

# for tarea in lista_de_tareas:
#     respuesta = obtener_respuesta_ia(tarea)
#     print(respuesta)


"""Promocionar productos"""

# def obtener_respuesta_ia(prompt):
#       completion = client.chat.completions.create(
#         model="gpt-4o",
#         max_tokens=500,
#         messages=[
#             {"role": "user", "content": prompt}
#         ]
#     )
#       return(completion.choices[0].message.content)


# sabores_helados = [
#     "Vainilla",
#     "Chocolate",
#     "Pistacho",
#     "Menta granizada"
# ]

# for sabor in sabores_helados:
#     prompt = f"""Para el sabor de helado mencionado a continuación, proporcioná una descripción muy breve y cautivadora en español./n
#     Trata de que sea en una sola linea, de tal manera que pueda usarse con fines promocionales.

#     Sabor: {sabor}

#     """
#     respuesta = obtener_respuesta_ia(sabor)
#     print(respuesta)


"""Listas y diccionarios"""

# def obtener_respuesta_ia(prompt):
#       completion = client.chat.completions.create(
#         model="gpt-4o",
#         max_tokens=500,
#         messages=[
#             {"role": "user", "content": prompt}
#         ]
#     )
#       return(completion.choices[0].message.content)

# preferencias_alimentarias_tommy = {
# "restricciones_dietarias": "vegetariano",
# "ingredientes_favoritos": ["tofu", "aceitunas"],
# "nivel_de_experiencia": "intermedio",
# "nivel_máximo_de_picante": 6
# }

# prompt = f"""Por favor, sugiere una receta que intente incluir
# los siguientes ingredientes:
# {preferencias_alimentarias_tommy["ingredientes_favoritos"]}.
# La receta debe adherirse a las siguientes restricciones dietarias:
# {preferencias_alimentarias_tommy["restricciones_dietarias"]}.
# La dificultad de la receta debe ser:
# {preferencias_alimentarias_tommy["nivel_de_experiencia"]}
# El nivel máximo de picante en una escala del 1 al 10 debe ser:
# {preferencias_alimentarias_tommy["nivel_máximo_de_picante"]}
# Proporciona una descripción de dos oraciones.
# """
# respuesta = obtener_respuesta_ia(prompt)
# print(respuesta)

"""Refinando el prompt con los ingredientes disponibles"""

# def obtener_respuesta_ia(prompt):
#       completion = client.chat.completions.create(
#         model="gpt-4o",
#         max_tokens=500,
#         messages=[
#             {"role": "user", "content": prompt}
#         ]
#     )
#       return(completion.choices[0].message.content)

# especias_disponibles = ["comino", "cúrcuma", "orégano", "pimentón"]

# preferencias_alimentarias_tommy = {
# "restricciones_dietarias": "vegetariano",
# "ingredientes_favoritos": ["tofu", "aceitunas"],
# "nivel_de_experiencia": "intermedio",
# "nivel_máximo_de_picante": 6
# }

# prompt = f"""Por favor, sugiere una receta que intente incluir
# los siguientes ingredientes:
# {preferencias_alimentarias_tommy["ingredientes_favoritos"]}.
# La receta debe adherirse a las siguientes restricciones dietarias:
# {preferencias_alimentarias_tommy["restricciones_dietarias"]}.
# La dificultad de la receta debe ser:
# {preferencias_alimentarias_tommy["nivel_de_experiencia"]}
# El nivel máximo de picante en una escala del 1 al 10 debe ser:
# {preferencias_alimentarias_tommy["nivel_máximo_de_picante"]}
# Proporciona una descripción de dos oraciones.
# La receta no debe incluir especias que no estén en esta lista:
# Especias: {especias_disponibles}
# """
# respuesta = obtener_respuesta_ia(prompt)
# print(respuesta)

"""**Nota:** Podemos ignorar con seguridad cualquier advertencia que veamos sobre actualizar pip.

bs4 es la abreviatura de Beautiful Soup 4. Podemos consultar la documentación de Beautiful Soup si queremos aprender más sobre el paquete, pero nos
proporciona herramientas para interpretar páginas web HTML dentro de programas Python.

Ahora que hemos instalado el paquete bs4, ¡podemos usarlo en nuestros programas!

Primero, necesitamos importar la función BeautifulSoup que usaremos del paquete bs4, así como algunos otros paquetes:"""

###Obtener datos de la web

# En esta sección, "rasparemos" o descargaremos datos HTML de un sitio web, 
# en este caso de un boletín de Batch publicado por DeepLearning.AI.
# Usaremos el paquete Python requests para descargar 
# los datos de la página web y hacerlos disponibles en nuestro programa:



def obtener_respuesta_ia(prompt):
      completion = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=500,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
      return(completion.choices[0].message.content)



# La url de uno de los boletines de Batch
url = 'https://www.dw.com/es/l%C3%ADneas-de-nazca-descubren-con-ia-m%C3%A1s-de-300-nuevos-geoglifos/a-70312858'

# Obteniendo el contenido de los contenidos de la página web
response = requests.get(url)

# Imprimimos la respuesta de las solicitudes
print(response)


HTML(f'<iframe src={url} width="60%" height="400"></iframe>')

# Usando beautifulsoup para extraer el texto
soup = BeautifulSoup(response.text, 'html.parser')

# Encontramos todo el texto en elementos de párrafo en la página web
all_text = soup.find_all('p')

# Creamos una cadena vacía para almacenar el texto extraído
combined_text = ""

# Iteramos sobre 'all_text' y añadimos a la cadena combined_text
for text in all_text:
    combined_text = combined_text + "\n" + text.get_text()

# Imprimimos el texto combinado final
print(combined_text)


prompt = f"""Extrae los puntos clave del siguiente texto.\n
 Añade una tabla con los datos más relevantes de tal manera que facilite la lectura y un posterior diseño de dataset.

Texto:
{combined_text}


"""

#Luego pasemos el prompt al LLM:
respuesta = obtener_respuesta_ia(prompt)
print(respuesta)
display(Markdown(respuesta))