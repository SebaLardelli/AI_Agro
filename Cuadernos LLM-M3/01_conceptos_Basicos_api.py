import os
from openai import OpenAI
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown

load_dotenv() 

console = Console()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

def get_completion(prompt, model="gpt-4o-mini", temperature=0):
    # Usamos la variable OPENAI_API_KEY cargada desde secrets o .env
    client = OpenAI(api_key=OPENAI_API_KEY)

    messages = [{"role": "user", "content": prompt}]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature, # grado de aleatoriedad (0 = más predecible)
    )
    return response.choices[0].message.content



analisis_laboratorio = """
ANÁLISIS DE SUELO - LABORATORIO AGROPAMPA
Cliente: Establecimiento San José - Pergamino, Buenos Aires
Lote: 12-A (Preparación para soja 2024/25)
Fecha: 08/01/2024
Profundidad: 0-20 cm

RESULTADOS:
pH: 5.2 (ácido)
Materia orgánica: 2.8% (medio)
Nitrógeno total: 0.12% (bajo)
Fósforo disponible: 12 ppm (bajo)
Potasio intercambiable: 180 ppm (medio)
Conductividad eléctrica: 0.4 dS/m (normal)
Textura: Franco-limoso
CIC: 22.5 cmol/kg

OBSERVACIONES: Suelo típico de la pampa húmeda con acidez moderada.
Recomiendan encalado previo a siembra. Evaluar fertilización fosfatada
según análisis económico de dosis respuesta.
"""

# prompt = f"""
# Analiza los siguientes resultados de análisis de suelo y extrae la información clave:
# - Estado general del suelo (bueno/regular/deficiente)
# - ¿Requiere encalado? (verdadero o falso)
# - Nutriente más limitante
# - Establecimiento/Cliente

# Formatea tu respuesta como un objeto JSON con las claves:
# "estado_suelo", "requiere_encalado", "nutriente_limitante" y "establecimiento".

# Si la información no está presente, usa "no_especificado" como valor.
# Formatea el valor de requiere_encalado como un booleano.

# Análisis de laboratorio: '''{analisis_laboratorio}'''
# """
# response = get_completion(prompt)
# print(response)


#  Ejemplo práctico: Generación de recomendaciones

prompt_recomendaciones = f"""
Basado en este análisis de suelo, genera 3 recomendaciones técnicas específicas
para la siembra de soja en la región pampeana:

{analisis_laboratorio}

Incluye:
1. Corrección de pH (dosis de cal si corresponde)
2. Plan de fertilización (productos y dosis por hectárea)
3. Manejo específico del lote

Responde de forma técnica pero práctica.
"""

recomendaciones = get_completion(prompt_recomendaciones)
print("=== RECOMENDACIONES TÉCNICAS ===")
console.print(Markdown("## ANÁLISIS DE LABORATORIO"))
console.print(Markdown(recomendaciones))

#                                ANÁLISIS DE LABORATORIO
#         Recomendaciones Técnicas para la Siembra de Soja en la Región Pampeana        

# 1. Corrección de pH: Dado que el pH del suelo es de 5.2, se considera ácido y se      
# recomienda realizar una corrección mediante la aplicación de cal. Para elevar el pH a 
# un nivel óptimo para el cultivo de soja (entre 6.0 y 6.5), se sugiere aplicar cal     
# agrícola (carbonato de calcio) a razón de aproximadamente 1.5 a 2.0 toneladas por     
# hectárea. Esta dosis puede variar según el análisis de cal y la capacidad de
# neutralización del suelo, por lo que se recomienda realizar un análisis de cal para   
# determinar la dosis exacta. La aplicación debe realizarse al menos 4-6 semanas antes  
# de la siembra para permitir una adecuada reacción del suelo.

# 2. Plan de Fertilización: Con un contenido de nitrógeno total bajo (0.12%) y fósforo  
# disponible también bajo (12 ppm), se recomienda un plan de fertilización que
# contemple:

#  • Fósforo: Aplicar 100 kg/ha de superfosfato triple (0-46-0) para aumentar la        
#    disponibilidad de fósforo en el suelo.
#  • Nitrógeno: Incorporar 50 kg/ha de urea (46-0-0) en la siembra, considerando que la
#    soja es capaz de fijar nitrógeno, pero es importante asegurar un aporte inicial.
#  • Potasio: Dado que el potasio intercambiable es medio (180 ppm), se puede considerar   la aplicación de 50 kg/ha de cloruro de potasio (0-0-60) si se observa deficiencia
#    en el cultivo durante el desarrollo.

# Es fundamental realizar un análisis de costo-beneficio para ajustar las dosis y
# productos según la respuesta esperada y el precio de los insumos.

# 3. Manejo Específico del Lote:

#  • Rotación de Cultivos: Implementar una rotación de cultivos que incluya leguminosas
#    para mejorar la materia orgánica y la fijación de nitrógeno en el suelo.
#  • Control de Malezas: Realizar un control efectivo de malezas antes de la siembra,
#    utilizando herbicidas pre-emergentes y/o prácticas culturales que minimicen la
#    competencia.
#  • Monitoreo de Plagas y Enfermedades: Establecer un programa de monitoreo para
#    detectar plagas y enfermedades a tiempo, implementando medidas de control
#    integradas.
#  • Siembra Directa: Considerar la siembra directa para conservar la humedad del suelo
#    y mejorar la estructura del mismo, especialmente en un suelo franco-limoso.

# Estas recomendaciones buscan optimizar el rendimiento del cultivo de soja en el lote
# 12-A, teniendo en cuenta las características del suelo y las condiciones de la región
# pampeana.


