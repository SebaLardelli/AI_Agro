import os
import sys
import pandas as pd
import gradio as gr

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=OPENAI_API_KEY)


if not OPENAI_API_KEY:
    raise ValueError(
        "❌ ERROR: No se encontró la variable OPENAI_API_KEY. "
        "Por favor, revisa que esté en tu archivo .env y que se llame exactamente así."
    )
else:
    print("✅ OPENAI_API_KEY cargada correctamente. Se puede continuar con el experimento.")


"""3) Prompts: Variante A (Zero-shot) y Variante B (Few-shot)"""


# prompt_A = """Descripción de la práctica: Optimización del uso del agua en cultivos de secano mediante técnicas de conservación de humedad.

# Palabras clave: conservación agua, secano, humedad suelo, optimización.

# Temas relacionados:"""

#zero-shot = no tiene ejemplos

# prompt_B = """Descripción de la práctica: Implementación de rotación de cultivos para mejorar la salud del suelo y reducir plagas.

# Palabras clave: rotación cultivos, salud suelo, manejo plagas, sostenibilidad.

# Temas relacionados: Agroecología, Manejo Integrado de Plagas, Fertilización Natural, Diversificación Agrícola.


# Descripción de la práctica: Uso de drones para monitoreo de cultivos y detección temprana de enfermedades.

# Palabras clave: drones agricultura, monitoreo cultivos, detección enfermedades, agricultura precisión.

# Temas relacionados: Teledetección Agrícola, Agricultura Inteligente, Sensores Remotos, Análisis de Imágenes Aéreas.


# Descripción de la práctica: Optimización del uso del agua en cultivos de secano mediante técnicas de conservación de humedad.

# Palabras clave: conservación agua, secano, humedad suelo, optimización.

# Temas relacionados:"""

#few-shot = tiene ejemplos


# print('📝 Prompt A (Zero-shot) - Prácticas Agroindustria:')
# print('-' * 50)
# print(prompt_A)
# print('\n📝 Prompt B (Few-shot) - Prácticas Agroindustria:')
# print('-' * 50)
# print(prompt_B)

"""Respuesta del modelo"""

# 📝 Prompt A (Zero-shot) - Prácticas Agroindustria:
# --------------------------------------------------
# Descripción de la práctica: Optimización del uso del agua en cultivos de secano mediante técnicas de conservación de humedad.

# Palabras clave: conservación agua, secano, humedad suelo, optimización.

# Temas relacionados:

# 📝 Prompt B (Few-shot) - Prácticas Agroindustria:
# --------------------------------------------------
# Descripción de la práctica: Implementación de rotación de cultivos para mejorar la salud del suelo y reducir plagas.

# Palabras clave: rotación cultivos, salud suelo, manejo plagas, sostenibilidad.        

# Temas relacionados: Agroecología, Manejo Integrado de Plagas, Fertilización Natural, Diversificación Agrícola.


# Descripción de la práctica: Uso de drones para monitoreo de cultivos y detección temprana de enfermedades.

# Palabras clave: drones agricultura, monitoreo cultivos, detección enfermedades, agricultura precisión.

# Temas relacionados: Teledetección Agrícola, Agricultura Inteligente, Sensores Remotos, Análisis de Imágenes Aéreas.


# Descripción de la práctica: Optimización del uso del agua en cultivos de secano mediante técnicas de conservación de humedad.

# Palabras clave: conservación agua, secano, humedad suelo, optimización.


"""Definimos la respuesta del modelo para cada prompt"""

prompt_A = """Descripción de la práctica: Optimización del uso del agua en cultivos de secano mediante técnicas de conservación de humedad.

Palabras clave: conservación agua, secano, humedad suelo, optimización.

Temas relacionados:"""

prompt_B = """Descripción de la práctica: Implementación de rotación de cultivos para mejorar la salud del suelo y reducir plagas.

Palabras clave: rotación cultivos, salud suelo, manejo plagas, sostenibilidad.

Temas relacionados: Agroecología, Manejo Integrado de Plagas, Fertilización Natural, Diversificación Agrícola.


Descripción de la práctica: Uso de drones para monitoreo de cultivos y detección temprana de enfermedades.

Palabras clave: drones agricultura, monitoreo cultivos, detección enfermedades, agricultura precisión.

Temas relacionados: Teledetección Agrícola, Agricultura Inteligente, Sensores Remotos, Análisis de Imágenes Aéreas.


Descripción de la práctica: Optimización del uso del agua en cultivos de secano mediante técnicas de conservación de humedad.

Palabras clave: conservación agua, secano, humedad suelo, optimización.

Temas relacionados:"""

# def get_response(
#     prompt, model="gpt-4o-mini", temperature=0.7, max_tokens=256
# ):
#     """
#     Genera una respuesta usando OpenAI Chat Completions.
#     Retorna el texto del assistant.
#     """
#     try:
#         # client.chat.completions.create retorna un objeto con choices
#         response = client.chat.completions.create(
#             model=model,
#             messages=[{"role": "user", "content": prompt}],
#             temperature=temperature,
#             max_tokens=max_tokens,
#         )
#         # Acceder al contenido de la primera choice correctamente
#         content = response.choices[0].message.content
#         return content
#     except Exception as e:
#         # Manejo básico de errores
#         print("Error al generar respuesta:", e)
#         return None

# test_prompts = [prompt_A, prompt_B]
# responses = []
# num_tests = 5
# model_to_use = (
#     "gpt-4o-mini"  
# )  

# print('🚀 Iniciando experimento A/B Testing con OpenAI...')
# for idx, prompt in enumerate(test_prompts):
#     var_name = chr(ord('A') + idx)
#     print(f'📊 Generando respuestas para Variante {var_name}...')
#     for i in range(num_tests):
#         resp_text = get_response(prompt, model=model_to_use)
#         data = {
#             'variante': var_name,
#             'prompt': prompt,
#             'respuesta': resp_text
#         }
#         responses.append(data)
#         print(f'  ✓ Respuesta {i+1}/{num_tests} generada')
#     print()
# df = pd.DataFrame(responses)
# df.to_csv('respuestas_openai.csv', index=False)

# print('📄 Resumen del experimento:')
# print(f'Total de respuestas generadas: {len(df)}')
# print(df.head())


# ## 6) Interfaz de evaluación humana (widgets) yo utilizo Gradio

# # Cargar el CSV de respuestas generadas
# df = pd.read_csv('respuestas_openai.csv')
# df = df.sample(frac=1).reset_index(drop=True)  # Mezclar para evaluación ciega
# df['feedback'] = pd.Series(dtype='float')
# response_index = 0

# # Función para actualizar la respuesta según el feedback del usuario
# def update_response(feedback=None):
#     global response_index, df
    
#     # Guardar el feedback anterior
#     if feedback is not None:
#         df.at[response_index, 'feedback'] = feedback
#         response_index += 1

#     # Revisar si hay más respuestas
#     if response_index < len(df):
#         new_response = df.iloc[response_index]['respuesta']
#         count_text = f"Respuesta: {response_index + 1}/{len(df)} (Variante {df.iloc[response_index]['variante']})"
#         return f"<p>{new_response}</p>", count_text
#     else:
#         # Guardar resultados finales
#         df.to_csv('resultados_openai.csv', index=False)
#         summary_df = df.groupby('variante').agg(
#             cantidad=('feedback', 'count'),
#             puntuacion=('feedback', 'mean')
#         ).reset_index()
#         summary_text = summary_df.to_string(index=False)
#         return "✅ Prueba A/B completada. Resultados guardados en resultados_openai.csv", summary_text

# # Crear la interfaz Gradio
# with gr.Blocks() as demo:
#     response_box = gr.HTML(label="Respuesta del modelo")
#     count_label = gr.Label()
    
#     with gr.Row():
#         thumbs_down = gr.Button("👎")
#         thumbs_up = gr.Button("👍")
    
#     # Conectar botones a la función
#     thumbs_down.click(update_response, inputs=gr.State(value=0), outputs=[response_box, count_label])
#     thumbs_up.click(update_response, inputs=gr.State(value=1), outputs=[response_box, count_label])
    
#     # Inicializar la primera respuesta
#     response_box.value, count_label.value = update_response()

# print('👇 Evalúa cada respuesta usando los botones:')
# demo.launch()

"""7) Conclusiones y próximos pasos

- Incrementar el número de iteraciones para mayor poder estadístico
- Probar diferentes modelos (`gpt-3.5-turbo`, `gpt-4`, `gpt-4o`) para comparar coste/beneficio
- Guardar metadatos (temperatura, modelo) junto a cada respuesta para análisis posterior
- Probar la ejecución en Colab y en local para validar la carga de secrets"""

prompt_A = """Descripción de la práctica: Optimización del uso del agua en cultivos de secano mediante técnicas de conservación de humedad.

Palabras clave: conservación agua, secano, humedad suelo, optimización, temperadura, modelo.

Temas relacionados:"""

prompt_B = """Descripción de la práctica: Implementación de rotación de cultivos para mejorar la salud del suelo y reducir plagas.

Palabras clave: conservación agua, secano, humedad suelo, optimización, temperadura, modelo.

Temas relacionados: Agroecología, Manejo Integrado de Plagas, Fertilización Natural, Diversificación Agrícola.


Descripción de la práctica: Uso de drones para monitoreo de cultivos y detección temprana de enfermedades.

Palabras clave: drones agricultura, monitoreo cultivos, detección enfermedades, agricultura precisión, temperadura, modelo.

Temas relacionados: Teledetección Agrícola, Agricultura Inteligente, Sensores Remotos, Análisis de Imágenes Aéreas.


Descripción de la práctica: Optimización del uso del agua en cultivos de secano mediante técnicas de conservación de humedad.

Palabras clave: conservación agua, secano, humedad suelo, optimización, temperadura, modelo.

Temas relacionados:"""


def get_response(
    prompt, model="gpt-4", temperature=0.7, max_tokens=256
):
    """
    Genera una respuesta usando OpenAI Chat Completions.
    Retorna el texto del assistant.
    """
    try:
        # client.chat.completions.create retorna un objeto con choices
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        # Acceder al contenido de la primera choice correctamente
        content = response.choices[0].message.content
        return content
    except Exception as e:
        # Manejo básico de errores
        print("Error al generar respuesta:", e)
        return None

test_prompts = [prompt_A, prompt_B]
responses = []
num_tests = 10
model_to_use = (
    "gpt-4"  
)  

print('🚀 Iniciando experimento A/B Testing con OpenAI...')
for idx, prompt in enumerate(test_prompts):
    var_name = chr(ord('A') + idx)
    print(f'📊 Generando respuestas para Variante {var_name}...')
    for i in range(num_tests):
        resp_text = get_response(prompt, model=model_to_use)
        data = {
            'variante': var_name,
            'prompt': prompt,
            'respuesta': resp_text
        }
        responses.append(data)
        print(f'  ✓ Respuesta {i+1}/{num_tests} generada')
    print()
df = pd.DataFrame(responses)
df.to_csv('respuestas_openai.csv', index=False)

print('📄 Resumen del experimento:')
print(f'Total de respuestas generadas: {len(df)}')
print(df.head())

# Cargar el CSV de respuestas generadas
df = pd.read_csv('respuestas_openai.csv')
df = df.sample(frac=1).reset_index(drop=True)  # Mezclar para evaluación ciega
df['feedback'] = pd.Series(dtype='float')
response_index = 0

# Función para actualizar la respuesta según el feedback del usuario
def update_response(feedback=None):
    global response_index, df
    
    # Guardar el feedback anterior
    if feedback is not None:
        df.at[response_index, 'feedback'] = feedback
        response_index += 1

    # Revisar si hay más respuestas
    if response_index < len(df):
        new_response = df.iloc[response_index]['respuesta']
        count_text = f"Respuesta: {response_index + 1}/{len(df)} (Variante {df.iloc[response_index]['variante']})"
        return f"<p>{new_response}</p>", count_text
    else:
        # Guardar resultados finales
        df.to_csv('resultados_openai.csv', index=False)
        summary_df = df.groupby('variante').agg(
            cantidad=('feedback', 'count'),
            puntuacion=('feedback', 'mean')
        ).reset_index()
        summary_text = summary_df.to_string(index=False)
        return "✅ Prueba A/B completada. Resultados guardados en resultados_openai.csv", summary_text

# Crear la interfaz Gradio
with gr.Blocks() as demo:
    response_box = gr.HTML(label="Respuesta del modelo")
    count_label = gr.Label()
    
    with gr.Row():
        thumbs_down = gr.Button("👎")
        thumbs_up = gr.Button("👍")
    
    # Conectar botones a la función
    thumbs_down.click(update_response, inputs=gr.State(value=0), outputs=[response_box, count_label])
    thumbs_up.click(update_response, inputs=gr.State(value=1), outputs=[response_box, count_label])
    
    # Inicializar la primera respuesta
    response_box.value, count_label.value = update_response()

print('👇 Evalúa cada respuesta usando los botones:')
demo.launch()