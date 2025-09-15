import requests
import os
from google import genai
from google.genai import types
import matplotlib.pyplot as plt
from rich.console import Console
from rich.markdown import Markdown
from dotenv import load_dotenv

load_dotenv()

console = Console()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
api_key = os.getenv('OPEN_WEATHER_API_KEY')

cliente_gemini = genai.Client(api_key=GOOGLE_API_KEY)

MODEL_ID = "gemini-2.5-pro"

url = f"http://api.openweathermap.org/data/2.5/weather?q=Mar+del+Plata&units=metric&appid={api_key}"

""" Obtener respuesta de la API climática """

response = requests.get(url)
data = response.json()

print("Datos climáticos obtenidos:")
print(data)

# Obtener pronóstico de 5 días
url_5dias = f"http://api.openweathermap.org/data/2.5/forecast?q=Rosario&units=metric&lang=es&appid={api_key}"

response_5dias = requests.get(url_5dias)
data_5dias = response_5dias.json()


""" Respuesta """

# Datos climáticos obtenidos:
# {'coord': {'lon': -57.5575, 'lat': -38.0023}, 'weather': [{'id': 801, 'main': 'Clouds', 'description': 'few clouds', 'icon': '02d'}], 'base': 'stations', 'main': {'temp': 15, 'feels_like': 14.33, 'temp_min': 13.86, 'temp_max': 16.64, 'pressure': 1019, 'humidity': 68, 'sea_level': 1019, 'grnd_level': 1016}, 'visibility': 10000, 'wind': {'speed': 5.81, 'deg': 360, 'gust': 5.81}, 'clouds': {'all': 21}, 'dt': 1757874949, 'sys': {'type': 2, 'id': 2018627, 'country': 'AR', 'sunrise': 1757843515, 'sunset': 
# 1757885988}, 'timezone': -10800, 'id': 3430863, 'name': 'Mar del Plata', 'cod': 200}

""" Procesamiento de Datos Climáticos """

# Extraer datos específicos
temperatura = data['main']['temp']
descripcion = data['weather'][0]['description']
velocidad_viento = data['wind']['speed']
humedad = data['main']['humidity']
presion = data['main']['pressure']

# Mostrar datos organizados
print("=== CONDICIONES CLIMÁTICAS ACTUALES ===")
print(f"Temperatura: {temperatura}°C")
print(f"Descripción: {descripcion}")
print(f"Velocidad del viento: {velocidad_viento} m/s")
print(f"Humedad relativa: {humedad}%")
print(f"Presión atmosférica: {presion} hPa")

""" Respuesta """

# Datos climáticos obtenidos:
# {'coord': {'lon': -57.5575, 'lat': -38.0023}, 'weather': [{'id': 801, 'main': 'Clouds', 'description': 'few clouds', 'icon': '02d'}], 'base': 'stations', 'main': {'temp': 15, 'feels_like': 14.33, 'temp_min': 13.86, 'temp_max': 16.64, 'pressure': 1019, 'humidity': 68, 'sea_level': 1019, 'grnd_level': 1016}, 'visibility': 10000, 'wind': {'speed': 5.81, 'deg': 360, 'gust': 5.81}, 'clouds': {'all': 21}, 'dt': 1757874949, 'sys': {'type': 2, 'id': 2018627, 'country': 'AR', 'sunrise': 1757843515, 'sunset': 
# 1757885988}, 'timezone': -10800, 'id': 3430863, 'name': 'Mar del Plata', 'cod': 200}
# === CONDICIONES CLIMÁTICAS ACTUALES ===
# Temperatura: 15°C
# Descripción: few clouds
# Velocidad del viento: 5.81 m/s
# Humedad relativa: 68%
# Presión atmosférica: 1019 hPa

""" Crear informe climático estructurado """

informe_clima = f"""REPORTE CLIMÁTICO - REGIÓN PAMPEANA
Fecha: Tiempo actual
Ubicación: Buenos Aires, Argentina

CONDICIONES METEOROLÓGICAS:
- Temperatura: {temperatura}°C
- Condición general: {descripcion}
- Humedad relativa: {humedad}%
- Velocidad del viento: {velocidad_viento} m/s
- Presión atmosférica: {presion} hPa
"""

print(informe_clima)

""" Respuesta """

# Datos climáticos obtenidos:
# {'coord': {'lon': -57.5575, 'lat': -38.0023}, 'weather': [{'id': 801, 'main': 'Clouds', 'description': 'few clouds', 'icon': '02d'}], 'base': 'stations', 'main': {'temp': 15, 'feels_like': 14.33, 'temp_min': 13.86, 'temp_max': 16.64, 'pressure': 1019, 'humidity': 68, 'sea_level': 1019, 'grnd_level': 1016}, 'visibility': 10000, 'wind': {'speed': 5.81, 'deg': 360, 'gust': 5.81}, 'clouds': {'all': 21}, 'dt': 1757874949, 'sys': {'type': 2, 'id': 2018627, 'country': 'AR', 'sunrise': 1757843515, 'sunset': 
# 1757885988}, 'timezone': -10800, 'id': 3430863, 'name': 'Mar del Plata', 'cod': 200}
# === CONDICIONES CLIMÁTICAS ACTUALES ===
# Temperatura: 15°C
# Descripción: few clouds
# Velocidad del viento: 5.81 m/s
# Humedad relativa: 68%
# Presión atmosférica: 1019 hPa
# REPORTE CLIMÁTICO - REGIÓN PAMPEANA
# Fecha: Tiempo actual
# Ubicación: Buenos Aires, Argentina

# CONDICIONES METEOROLÓGICAS:
# - Temperatura: 15°C
# - Condición general: few clouds
# - Humedad relativa: 68%
# - Velocidad del viento: 5.81 m/s
# - Presión atmosférica: 1019 hPa

""" Análisis Agronómico con Google Gemini """

# Función para consultar Gemini
def consultar_gemini(prompt):
    response = cliente_gemini.models.generate_content(
        model=MODEL_ID,
        contents=[prompt]
    )
    return response.text

# Análisis agronómico con Gemini
prompt_agricola = f"""Como agrónomo especialista en la región pampeana argentina, analiza las siguientes condiciones climáticas y proporciona recomendaciones técnicas específicas:

{informe_clima}

Incluye en tu análisis:
1. ¿Es un buen momento para aplicaciones de agroquímicos?
2. ¿Qué precauciones deben tomar los operarios agrícolas?
3. ¿Cómo afectan estas condiciones a los cultivos de soja y maíz?
4. ¿Se recomienda riego en estas condiciones?
5. Recomendaciones específicas para las próximas 24-48 horas

Responde de forma técnica pero práctica."""

respuesta_gemini = consultar_gemini(prompt_agricola)
print("=== ANÁLISIS AGRONÓMICO CON GEMINI ===")
console.print(Markdown(respuesta_gemini))


"""" Respuesta """
# Datos climáticos obtenidos:
# {'coord': {'lon': -57.5575, 'lat': -38.0023}, 'weather': [{'id': 801, 'main': 'Clouds', 'description': 'few clouds', 'icon': '02d'}], 'base': 'stations', 'main': {'temp': 14.81, 'feels_like': 14.12, 'temp_min': 13.86, 'temp_max': 16.08, 'pressure': 1019, 'humidity': 68, 'sea_level': 1019, 'grnd_level': 1016}, 'visibility': 10000, 'wind': {'speed': 4.92, 'deg': 360, 'gust': 5.81}, 'clouds': {'all': 21}, 'dt': 1757875557, 'sys': {'type': 2, 'id': 2018627, 'country': 'AR', 'sunrise': 1757843515, 'sunset': 1757885988}, 'timezone': -10800, 'id': 3430863, 'name': 'Mar del Plata', 'cod': 200}
# === CONDICIONES CLIMÁTICAS ACTUALES ===
# Temperatura: 14.81°C
# Descripción: few clouds
# Velocidad del viento: 4.92 m/s
# Humedad relativa: 68%
# Presión atmosférica: 1019 hPa
# REPORTE CLIMÁTICO - REGIÓN PAMPEANA
# Fecha: Tiempo actual
# Ubicación: Buenos Aires, Argentina

# CONDICIONES METEOROLÓGICAS:
# - Temperatura: 14.81°C
# - Condición general: few clouds
# - Humedad relativa: 68%
# - Velocidad del viento: 4.92 m/s
# - Presión atmosférica: 1019 hPa

# === ANÁLISIS AGRONÓMICO CON GEMINI ===
# ¡Excelente! Como agrónomo con experiencia en la Pampa Húmeda, analizo este reporte para darte        
# recomendaciones claras y aplicables.

# Aquí está mi análisis técnico y práctico de las condiciones actuales:

# ─────────────────────────────────────────────────────────────────────────────────────────────────────                                    Análisis Agronómico Integral

# Las condiciones presentadas (14.8°C, 68% HR, 1019 hPa de presión y pocas nubes) son típicas de un díaestable de otoño o principios de primavera en la región. La alta presión indica buen tiempo, sin     
# probabilidad de lluvias inminentes. Sin embargo, el factor crítico y limitante para la mayoría de laslabores es la velocidad del viento.

# ─────────────────────────────────────────────────────────────────────────────────────────────────────                      1. ¿Es un buen momento para aplicaciones de agroquímicos?

# Respuesta corta: No, no es un momento ideal.

# Análisis técnico: El principal problema es la velocidad del viento de 4.92 m/s, que equivale a 17.7  
# km/h. Este valor se encuentra por encima del umbral máximo recomendado para la mayoría de las        
# pulverizaciones terrestres, que se sitúa en los 15 km/h.

#  • Riesgo de Deriva: Con vientos de esta intensidad, el riesgo de deriva es muy alto. Esto significa 
#    que una porción significativa del producto aplicado (herbicida, fungicida, insecticida) no llegará   al objetivo (malezas, cultivo) y se desplazará fuera del lote, con graves consecuencias:
#     • Baja eficacia del tratamiento: Se desperdicia producto y no se controla adecuadamente el       
#       objetivo.
#     • Fitotoxicidad en lotes vecinos: Se pueden dañar cultivos sensibles linderos.
#     • Contaminación ambiental: Afectación de cursos de agua, zonas buffer, áreas residenciales o     
#       apiarios.
#  • Evaporación: El viento acelera la evaporación de las gotas más finas antes de que lleguen al      
#    blanco, reduciendo la dosis efectiva.
#  • Condiciones favorables (que no alcanzan a compensar): La temperatura (menor a 25°C) y la humedad  
#    relativa (mayor a 60%) son, en principio, excelentes para minimizar la evaporación y favorecer la 
#    absorción del producto por las hojas. Sin embargo, el viento anula estos beneficios.

# Recomendación práctica: Esperar. Lo más probable es que el viento disminuya su intensidad en las     
# primeras horas de la mañana o al atardecer. Se debe monitorear constantemente con un anemómetro de   
# mano y buscar una "ventana de aplicación" con vientos por debajo de los 12-15 km/h.

#                       2. ¿Qué precauciones deben tomar los operarios agrícolas?

# Si la aplicación fuera absolutamente impostergable (lo cual no se recomienda), las precauciones debenser extremas:

#  • Uso obligatorio de EPP (Equipo de Protección Personal): Dada la alta probabilidad de deriva, el   
#    operario está más expuesto. Es indispensable el uso de traje impermeable, guantes de nitrilo,     
#    máscara con filtros adecuados, protección ocular y botas.
#  • Tecnología Anti-deriva: Es mandatorio utilizar herramientas para mitigar el riesgo:
#     • Pastillas de pulverización de aire inducido (AI): Generan gotas más grandes y pesadas, menos   
#       propensas a la deriva.
#     • Bajar la altura del botalón: Reducir la distancia entre las pastillas y el objetivo al mínimo  
#       posible y seguro.
#     • Reducir la velocidad de avance: Esto mejora la penetración y reduce la turbulencia generada por      la máquina.
#     • Uso de coadyuvantes: Incorporar al caldo de pulverización aceites o polímeros anti-deriva.     
#  • Verificación de la dirección del viento: El operario debe ser consciente en todo momento de hacia 
#    dónde sopla el viento y asegurarse de que no haya zonas sensibles (casas, escuelas, cursos de     
#    agua, cultivos orgánicos) en esa dirección.

#                   3. ¿Cómo afectan estas condiciones a los cultivos de soja y maíz?

# Dado que la temperatura es de 14.8°C, estamos fuera de la temporada de crecimiento activo para la    
# soja y el maíz (cultivos estivales). Por lo tanto, el análisis se centra en la etapa del ciclo       
# productivo en que nos encontramos:

#  • Período de Barbecho (lo más probable): Estas condiciones son favorables para el desarrollo de     
#    malezas de ciclo otoño-invierno-primaveral. La buena radiación solar (pocas nubes) y la humedad   
#    moderada promueven su crecimiento. El objetivo principal en esta etapa es el control de malezas   
#    para acumular agua y nutrientes para el próximo cultivo de verano. La limitante, nuevamente, es la   aplicación de herbicidas por el viento.
#  • Rastrojo Post-cosecha: Las condiciones de humedad y temperatura moderadas son adecuadas para la   
#    actividad microbiana que descompone el rastrojo en superficie, un pilar fundamental del sistema de   siembra directa.
#  • Siembras muy tempranas (improbable, pero posible): Si se tratara de un maíz de siembra
#    ultra-temprana en una zona particular, esta temperatura fresca ralentizaría su emergencia y       
#    crecimiento inicial (V1-V3), pudiendo generar estrés por frío, aunque sin riesgo de heladas       
#    inminentes. El viento aumentaría la tasa de evapotranspiración, secando la capa superficial del   
#    suelo.

#                             4. ¿Se recomienda riego en estas condiciones?

# Respuesta corta: Absolutamente no.

# Análisis técnico: La evapotranspiración (ET) del cultivo de referencia será baja. La temperatura     
# fresca es el factor dominante que limita la pérdida de agua, a pesar de que el viento la incremente  
# ligeramente. Los cultivos principales no están en su período crítico de demanda hídrica. Aplicar     
# riego ahora sería ineficiente y un desperdicio de agua y energía. El objetivo agronómico en esta     
# época del año es conservar la humedad del perfil del suelo, no añadir más.

# Recomendación práctica: Mantener la cobertura del rastrojo en superficie. Esta es la mejor
# herramienta para reducir la evaporación directa desde el suelo causada por el viento y el sol.       

#                     5. Recomendaciones específicas para las próximas 24-48 horas

#  1 Monitoreo Intensivo del Viento: Es la tarea prioritaria. Utilizar pronósticos meteorológicos de   
#    precisión y un anemómetro en el lote. Identificar las ventanas de calma, que suelen ocurrir entre 
#    las 6:00 y las 9:00 AM o después de las 6:00 PM.
#  2 Planificar la Pulverización: Tener el equipo calibrado y el caldo listo para salir a pulverizar en   cuanto las condiciones del viento lo permitan. Priorizar los lotes con mayor enmalezamiento o con 
#    presencia de malezas resistentes en estados iniciales, que son más fáciles de controlar.
#  3 Recorrer los Lotes: Aprovechar el buen tiempo para el monitoreo a pie o en vehículo. Evaluar el   
#    estado y tipo de malezas presentes, revisar la humedad superficial del suelo y detectar posibles  
#    problemas como plagas de suelo (ej. gusanos blancos, bichos bolita) que puedan afectar la futura  
#    siembra.
#  4 Mantenimiento de Maquinaria: Es un día ideal para realizar tareas de mantenimiento y calibración  
#    de equipos al aire libre, ya que las condiciones son cómodas para trabajar.
#  5 Evitar Labores que Remuevan el Suelo: El viento de 17.7 km/h puede causar erosión eólica en suelos   desnudos o recién laboreados. Mantener la cobertura es clave.

# ─────────────────────────────────────────────────────────────────────────────────────────────────────En resumen: condiciones meteorológicas estables y favorables para tareas a campo, pero con una       
# restricción clave por el viento para las pulverizaciones. La clave es el monitoreo y la paciencia    
# para encontrar la ventana de aplicación óptima y segura.

""" Visualización de Datos Climáticos """

# Crear gráfico de condiciones actuales
fig, ax = plt.subplots(figsize=(12, 6))

parametros = ['Temperatura (°C)', 'Humedad (%)', 'Viento (m/s)', 'Presión (hPa)']
valores = [temperatura, humedad, velocidad_viento, presion/10]  # Presión dividida por 10 para escala
colores = ['red', 'blue', 'green', 'orange']

bars = ax.bar(parametros, valores, color=colores)
ax.set_ylabel('Valor')
ax.set_title('Condiciones Climáticas Actuales - Buenos Aires')

# Agregar valores sobre las barras
for bar, valor in zip(bars, [temperatura, humedad, velocidad_viento, presion]):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
            f'{valor:.1f}',
            ha='center', va='bottom')

plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

""" Pronóstico Extendido para Planificación Agrícola"""


# Extraer datos para análisis
fechas = []
temperaturas = []
humedades = []
velocidades_viento = []

for pronostico in data_5dias['list'][:20]:  # Primeros 20 registros (5 días)
    fechas.append(pronostico['dt_txt'])
    temperaturas.append(pronostico['main']['temp'])
    humedades.append(pronostico['main']['humidity'])
    velocidades_viento.append(pronostico['wind']['speed'])

# Crear gráfico de tendencia
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(15, 12))

# Temperatura
ax1.plot(fechas, temperaturas, 'r-o', linewidth=2)
ax1.set_title('Pronóstico de Temperatura (5 días)')
ax1.set_ylabel('Temperatura (°C)')
ax1.tick_params(axis='x', rotation=45)
ax1.grid(True, alpha=0.3)

# Humedad
ax2.plot(fechas, humedades, 'b-s', linewidth=2)
ax2.set_title('Pronóstico de Humedad Relativa (5 días)')
ax2.set_ylabel('Humedad (%)')
ax2.tick_params(axis='x', rotation=45)
ax2.grid(True, alpha=0.3)

# Velocidad del viento
ax3.plot(fechas, velocidades_viento, 'g-^', linewidth=2)
ax3.set_title('Pronóstico de Velocidad del Viento (5 días)')
ax3.set_ylabel('Velocidad (m/s)')
ax3.set_xlabel('Fecha y Hora')
ax3.tick_params(axis='x', rotation=45)
ax3.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print(f"Pronóstico obtenido para {len(fechas)} períodos de 3 horas")

# Datos climáticos obtenidos:5cDesktop\x5cCurso IA en el Agro\x5cutn-agro-ai\x5cCuaderno{'coord': {'lon': -57.5575, 'lat': -38.0023}, 'weather': [{'id': 801, 'main': 'Clouds', 'description': 'few clouds', 'icon': '02d'}], 'base': 'stations', 'main': {'temp': 13.85, 'feels_like': 13.01, 'temp_min': 13.84, 'temp_max': 15.29, 'pressure': 1019, 'humidity': 66, 'sea_level': 1019, 'grnd_level': 1016}, 'visibility': 10000, 'wind': {'speed': 5.81, 'deg': 360, 'gust': 5.36}, 'clouds': {'all': 21}, 'dt': 1757876881, 'sys': {'type': 2, 'id': 2018627, 'country': 'AR', 'sunrise': 1757843515, 'sunset': 1757885988}, 'timezone': -10800, 'id': 3430863, 'name': 'Mar del Plata', 'cod': 200}
# === CONDICIONES CLIMÁTICAS ACTUALES ===
# Temperatura: 13.85°C
# Descripción: few clouds
# Velocidad del viento: 5.81 m/s     
# Humedad relativa: 66%
# Presión atmosférica: 1019 hPa      
# REPORTE CLIMÁTICO - REGIÓN PAMPEANA
# Fecha: Tiempo actual
# Ubicación: Buenos Aires, Argentina 

# CONDICIONES METEOROLÓGICAS:        
# - Temperatura: 13.85°C
# - Condición general: few clouds
# - Humedad relativa: 66%
# - Velocidad del viento: 5.81 m/s
# - Presión atmosférica: 1019 hPa

# === ANÁLISIS AGRONÓMICO CON GEMINI ===
# ¡Excelente! Como ingeniero agrónomo con experiencia en la Región Pampeana, procedo a  
# analizar el reporte climático y a proporcionar las recomendaciones técnicas
# correspondientes.

# ──────────────────────────────────────────────────────────────────────────────────────           Análisis Agronómico y Recomendaciones Técnicas - Región Pampeana

# Basado en el reporte climático (Temperatura: 13.85°C, Humedad: 66%, Viento: 5.81 m/s, 
# Presión: 1019 hPa, Cielo: Pocas nubes), este es mi diagnóstico y plan de acción:      

#               1. ¿Es un buen momento para aplicaciones de agroquímicos?

# Respuesta corta: NO, no es un momento recomendable.

# Análisis técnico:

#  • Factor Crítico - Viento: La velocidad del viento es de 5.81 m/s. Para convertirlo a   una unidad más utilizada en el campo: 5.81 m/s * 3.6 = 20.9 km/h. Este valor está  
#    por encima del umbral máximo recomendado para la mayoría de las aplicaciones       
#    terrestres, que se sitúa entre 12-15 km/h.
#  • Riesgo de Deriva: Un viento de casi 21 km/h provocará una deriva significativa.    
#    Esto implica que una parte importante del producto no llegará al objetivo (el      
#    cultivo o la maleza), reduciendo la eficacia de la aplicación y, lo que es más     
#    grave, contaminando lotes vecinos, cursos de agua o zonas sensibles.
#  • Temperatura y Humedad: La temperatura (13.85°C) es algo baja para la óptima        
#    absorción de herbicidas sistémicos como el glifosato, que requieren un metabolismo 
#    activo de la planta (idealmente >15°C). Sin embargo, la humedad relativa del 66% es   buena, ya que reduce la rápida evaporación de las gotas, dándoles más tiempo para  
#    ser absorbidas.
#  • Conclusión: A pesar de la buena humedad, el viento es el factor limitante y        
#    prohibitivo. Realizar una aplicación en estas condiciones es ineficiente,
#    antieconómico y ambientalmente irresponsable.

#               2. ¿Qué precauciones deben tomar los operarios agrícolas?

#  • Protección Personal: Aunque la temperatura es agradable, la condición de "pocas    
#    nubes" implica una alta radiación UV. Se recomienda el uso de sombrero de ala      
#    ancha, protector solar y ropa de manga larga para prevenir la exposición solar.    
#  • Polvo en Suspensión: El viento puede levantar polvo y partículas del suelo,        
#    especialmente en lotes recién cosechados o labrados. Es fundamental el uso de      
#    protección ocular (gafas de seguridad) para evitar irritaciones.
#  • Operación de Maquinaria: Al operar maquinaria de gran porte (tractores,
#    cosechadoras), el viento lateral puede afectar la estabilidad, especialmente en    
#    caminos rurales o al transportar implementos altos. Se debe conducir con mayor     
#    precaución.
#  • Para Aplicaciones (si se ignora la recomendación): Si por una emergencia ineludible   se decide aplicar, es imperativo utilizar toda la tecnología anti-deriva
#    disponible:
#     • Pastillas de inducción de aire (gotas más pesadas).
#     • Bajar la altura del botalón al mínimo posible.
#     • Reducir la velocidad de avance.
#     • Monitorear constantemente la dirección del viento para no afectar zonas
#       sensibles.

#           3. ¿Cómo afectan estas condiciones a los cultivos de soja y maíz?

# Dado que la temperatura es de 13.85°C, estamos probablemente en un período de otoño   
# (post-cosecha) o inicio de primavera (pre-siembra o emergencia temprana).

#  • Escenario Otoñal (Post-cosecha / Barbecho):
#     • Secado de Granos: Las condiciones son excelentes para el secado final del grano 
#       en planta (si aún queda algo por cosechar) y para la aireación de granos en     
#       silos. La baja humedad y el viento favorecen la pérdida de humedad del grano.   
#     • Manejo de Rastrojo: El viento facilita el secado del rastrojo en superficie.    
#     • Barbecho Químico: Como se mencionó, estas condiciones son pésimas para la       
#       aplicación de herbicidas de barbecho.
#  • Escenario de Primavera (Siembra / Emergencia):
#     • Humedad del Suelo: El viento y la baja humedad provocan una rápida evaporación  
#       del agua en la capa superficial del suelo. Esto es crítico si se está por       
#       sembrar, ya que puede comprometer la germinación y emergencia si la humedad no  
#       es la adecuada en la línea de siembra.
#     • Estrés en Plántulas: Si los cultivos están en estados iniciales (V1-V4), el     
#       viento genera un estrés mecánico (las plantas son "sacudidas") y aumenta la tasa      de evapotranspiración. Esto puede causar estrés hídrico incluso si hay humedad  
#       disponible en el perfil, ya que la planta transpira más rápido de lo que puede  
#       absorber agua. El crecimiento se verá ralentizado por las bajas temperaturas.   

#                     4. ¿Se recomienda riego en estas condiciones?

# Definitivamente NO para sistemas de riego por aspersión (ej. pivote central).

#  • Ineficiencia Absoluta: Con vientos de 21 km/h, la uniformidad de distribución del  
#    agua será nula. El patrón de riego se deformará completamente, con zonas
#    sobrerregadas y otras completamente secas.
#  • Pérdidas por Evaporación y Deriva: Un porcentaje muy alto del agua se evaporará en 
#    el aire o será arrastrado por el viento fuera del lote antes de tocar el suelo. Es 
#    un desperdicio de agua y de la energía utilizada para bombearla.
#  • Decisión de Riego: La decisión de regar debe basarse en el balance hídrico del     
#    suelo (medido con sondas o mediante calicatas), no en las condiciones atmosféricas 
#    de un día. Si el cultivo necesita agua, se debe esperar a que el viento calme para 
#    realizar una aplicación eficiente.

#              5. Recomendaciones específicas para las próximas 24-48 horas

#  1 POSTERGAR TODA PULVERIZACIÓN: No aplicar agroquímicos hasta que la velocidad del   
#    viento descienda de forma sostenida por debajo de los 15 km/h.
#  2 BUSCAR VENTANAS DE APLICACIÓN: Monitorear el pronóstico para identificar momentos  
#    de calma, típicamente en las primeras horas de la mañana o al atardecer, donde el  
#    viento suele disminuir y la humedad relativa aumentar.
#  3 MONITOREAR HUMEDAD EN LA CAMA DE SIEMBRA: Si se está planificando la siembra, es   
#    crucial revisar la humedad en los primeros 5-7 cm del suelo. Estas condiciones la  
#    reducirán rápidamente. Considerar ajustar la profundidad de siembra si es necesario   o esperar a una lluvia ligera.
#  4 APROVECHAR PARA COSECHA Y AIREACIÓN: Si aún queda algún lote por cosechar (ej. maíz   tardío), son condiciones ideales. Es un momento perfecto para encender los
#    ventiladores de los silos y bajar la humedad del grano almacenado de forma
#    económica.
#  5 PREVENIR EROSIÓN EÓLICA: En lotes con suelo desnudo y muy trabajado (labranza      
#    convencional), este viento puede causar "voladura". Priorizar la siembra directa y 
#    la cobertura con rastrojo para proteger el suelo.

# En resumen, las condiciones actuales son desfavorables para las tareas más sensibles  
# como la pulverización y el riego, pero pueden ser beneficiosas para otras como la     
# cosecha o el secado de granos. La planificación y el monitoreo constante del
# pronóstico son claves.
# Pronóstico obtenido para 20 períodos de 3 horas

""" Análisis Predictivo con Gemini """

# Preparar resumen del pronóstico para análisis
temp_promedio = sum(temperaturas) / len(temperaturas)
humedad_promedio = sum(humedades) / len(humedades)
viento_promedio = sum(velocidades_viento) / len(velocidades_viento)
temp_maxima = max(temperaturas)
temp_minima = min(temperaturas)

resumen_pronostico = f"""PRONÓSTICO EXTENDIDO (5 DÍAS) - PAMPA HÚMEDA

RESUMEN ESTADÍSTICO:
- Temperatura promedio: {temp_promedio:.1f}°C
- Temperatura máxima: {temp_maxima:.1f}°C
- Temperatura mínima: {temp_minima:.1f}°C
- Humedad relativa promedio: {humedad_promedio:.1f}%
- Velocidad de viento promedio: {viento_promedio:.1f} m/s

TENDENCIAS OBSERVADAS:
- Rango térmico: {temp_maxima - temp_minima:.1f}°C
- Condiciones de viento: {'Calmo' if viento_promedio < 3 else 'Moderado' if viento_promedio < 6 else 'Fuerte'}
- Nivel de humedad: {'Bajo' if humedad_promedio < 50 else 'Moderado' if humedad_promedio < 70 else 'Alto'}"""

print(resumen_pronostico)

""" Respuesta """

# Datos climáticos obtenidos:
# {'coord': {'lon': -57.5575, 'lat': -38.0023}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04n'}], 'base': 'stations', 'main': {'temp': 9.46, 'feels_like': 7.13, 'temp_min': 8.62, 'temp_max': 10.61, 'pressure': 1020, 'humidity': 63, 'sea_level': 1020, 'grnd_level': 1017}, 'visibility': 10000, 'wind': {'speed': 4.47, 'deg': 360, 'gust': 4.92}, 'clouds': {'all': 84}, 'dt': 1757890044, 'sys': {'type': 2, 'id': 268283, 'country': 'AR', 'sunrise': 1757843515, 'sunset': 1757885988}, 'timezone': -10800, 'id': 3430863, 'name': 'Mar del Plata', 'cod': 200}
# === CONDICIONES CLIMÁTICAS ACTUALES ===
# Temperatura: 9.46°C
# Descripción: broken clouds
# Velocidad del viento: 4.47 m/s
# Humedad relativa: 63%
# Presión atmosférica: 1020 hPa
# REPORTE CLIMÁTICO - REGIÓN PAMPEANA
# Fecha: Tiempo actual
# Ubicación: Buenos Aires, Argentina

# CONDICIONES METEOROLÓGICAS:
# - Temperatura: 9.46°C
# - Condición general: broken clouds
# - Humedad relativa: 63%
# - Velocidad del viento: 4.47 m/s
# - Presión atmosférica: 1020 hPa

# === ANÁLISIS AGRONÓMICO CON GEMINI ===
# ¡Excelente iniciativa! Analicemos en detalle estas condiciones climáticas desde una   
# perspectiva agronómica para la Región Pampeana.

# Como agrónomo especialista en la zona, mi primer diagnóstico es que estamos ante un   
# escenario típico de fines de otoño o invierno. Las condiciones son estables (alta     
# presión) pero con factores limitantes muy claros para ciertas labores.

# Aquí mi análisis técnico y recomendaciones prácticas:

# ──────────────────────────────────────────────────────────────────────────────────────                            Análisis Agronómico Detallado

#               1. ¿Es un buen momento para aplicaciones de agroquímicos?

# Respuesta corta: No. Es una condición de ALTO RIESGO y BAJA EFICIENCIA.

# Análisis técnico:

#  • Viento (Factor Crítico): La velocidad de 4.47 m/s equivale a 16.1 km/h. Este valor 
#    se encuentra por encima del umbral de seguridad recomendado para la mayoría de las 
#    aplicaciones, que se sitúa entre 3 y 12 km/h.
#     • Riesgo Principal: Deriva física. A esta velocidad, las gotas más finas del caldo      de pulverización no llegarán al objetivo (las malezas o el cultivo), siendo     
#       arrastradas fuera del lote. Esto no solo implica una pérdida económica y una    
#       menor eficacia del tratamiento, sino que también representa un grave riesgo de  
#       contaminación a lotes vecinos, cursos de agua, zonas periurbanas y cultivos     
#       sensibles.
#  • Temperatura (Factor de Eficacia): Con 9.46°C, el metabolismo de las malezas es muy 
#    lento.
#     • Impacto en Herbicidas Sistémicos: Productos como el glifosato, 2,4-D o
#       graminicidas (haloxifop, cletodim) requieren que la maleza esté activa para     
#       translocar el principio activo hasta su sitio de acción. A esta temperatura, la 
#       absorción y translocación son mínimas, lo que resultará en un control deficiente      y podría favorecer la selección de individuos resistentes.
#     • Herbicidas de Contacto: Podrían tener algo más de efectividad, pero aún así, su 
#       acción se ve reducida por el bajo metabolismo general de la planta.
#  • Humedad Relativa (Condición Favorable): El 63% es un buen valor. Ayuda a que las   
#    gotas se mantengan líquidas por más tiempo sobre la hoja, favoreciendo la absorción   y reduciendo la evaporación. Sin embargo, este factor positivo no compensa los     
#    riesgos generados por el viento y la baja temperatura.

# Conclusión: La aplicación debe ser pospuesta. El riesgo de deriva es demasiado alto y 
# la eficacia del tratamiento será muy baja.

#               2. ¿Qué precauciones deben tomar los operarios agrícolas?

# El trabajo en el campo continúa, así que es fundamental velar por la seguridad del    
# personal:

#  • Estrés por Frío: La temperatura es baja y la velocidad del viento genera una       
#    sensación térmica aún menor. Los operarios deben usar vestimenta de abrigo
#    adecuada, en capas, para poder regular su temperatura. Es crucial proteger cabeza, 
#    manos y pies.
#  • Equipo de Protección Personal (EPP): Independientemente de que no se apliquen      
#    agroquímicos, para cualquier tarea de mantenimiento o monitoreo, el uso de EPP     
#    básico (guantes, calzado de seguridad) es indispensable.
#  • Manejo de Maquinaria: El frío puede afectar la destreza manual. Se debe tener      
#    precaución extra al operar maquinaria pesada o realizar ajustes mecánicos.
#    Verificar el correcto funcionamiento de los sistemas de calefacción de las cabinas. • Hidratación: Aunque no se sienta sed por el frío, es importante mantenerse
#    hidratado.

#           3. ¿Cómo afectan estas condiciones a los cultivos de soja y maíz?

# Dado el ciclo de cultivos en la Región Pampeana, esta temperatura indica que no       
# estamos en la temporada de crecimiento activo de soja o maíz (cultivos de verano). El 
# análisis se centra en el estado de los lotes:

#  • Rastrojo en el Lote: Si los lotes provienen de la cosecha de soja o maíz, estas    
#    condiciones de baja temperatura y humedad moderada ralentizan la descomposición del   rastrojo. Esto es beneficioso para mantener la cobertura del suelo, protegerlo de  
#    la erosión eólica e hídrica y conservar la humedad para la siembra del próximo     
#    cultivo.
#  • Barbecho Químico: La principal implicancia es para el control de malezas invernales   que competirán con el futuro cultivo de gruesa. La imposibilidad de aplicar        
#    herbicidas hoy permite que malezas como Rama Negra (Conyza spp.), Raigrás (Lolium  
#    spp.) o Viola (Viola arvensis) sigan creciendo y ganando tamaño, lo que dificultará   su control posterior.
#  • Cultivos de Invierno (Trigo/Cebada): Si bien la pregunta es por soja y maíz, es    
#    relevante mencionar que para un cultivo de trigo o cebada en estado de macollaje,  
#    estas condiciones son favorables. La temperatura fresca promueve un buen desarrollo   radicular y de macollos, sin un estrés hídrico significativo.

#                     4. ¿Se recomienda riego en estas condiciones?

# Respuesta: No, bajo ningún concepto.

# Justificación técnica:

#  • Baja Evapotranspiración (ET): La demanda hídrica del ambiente y de cualquier       
#    cultivo de invierno activo es extremadamente baja debido a la baja temperatura, la 
#    nubosidad parcial y la humedad moderada.
#  • Eficiencia Nula: Aplicar agua ahora sería un gasto innecesario de agua y energía,  
#    ya que el perfil del suelo probablemente tenga humedad suficiente y no hay demanda 
#    que lo justifique.
#  • Riesgo de Heladas: Regar en estas condiciones saturaría la capa superficial del    
#    suelo. Si la temperatura desciende por debajo de 0°C durante la noche (lo cual es  
#    muy probable partiendo de 9.46°C), el agua en la superficie se congelaría, pudiendo   causar daños en la corona de los cultivos de invierno.

#              5. Recomendaciones específicas para las próximas 24-48 horas

#  1 Monitoreo, no Acción: La prioridad es el monitoreo. No tomar decisiones de
#    aplicación.
#     • Clima: Seguir de cerca el pronóstico, prestando especial atención a la
#       disminución de la velocidad del viento. Buscar una ventana de aplicación con    
#       vientos por debajo de 12 km/h y, si es posible, con temperaturas diurnas que    
#       superen los 14-15°C para mejorar la eficacia.
#     • Lotes: Aprovechar para recorrer los lotes a pie. Identificar qué malezas están  
#       presentes, su tamaño y estado de desarrollo. Esto permitirá planificar la       
#       estrategia de control (qué herbicidas y dosis usar) para cuando las condiciones 
#       mejoren.
#  2 Planificación de la Pulverización:
#     • Tener el equipo listo y calibrado.
#     • Seleccionar los herbicidas adecuados para las malezas identificadas.
#     • Considerar el uso de coadyuvantes de alta calidad (aceites, tensioactivos) para 
#       mejorar la eficacia de la aplicación cuando se realice en condiciones de        
#       temperatura subóptimas.
#  3 Mantenimiento de Equipos: Este es un excelente momento para realizar tareas de     
#    mantenimiento y calibración en pulverizadoras, sembradoras y otra maquinaria,      
#    asegurando que estén en perfectas condiciones para cuando se presente la ventana de   trabajo.
#  4 Seguridad del Personal: Insistir en las medidas de protección contra el frío para  
#    todo el personal que trabaje a la intemperie.

# En resumen, estamos en una fase de espera activa y planificación. Las condiciones     
# actuales impiden realizar aplicaciones eficientes y seguras, pero son ideales para la 
# recopilación de información a campo que nos permitirá tomar las mejores decisiones en 
# los próximos días.
# Pronóstico obtenido para 20 períodos de 3 horas
# PRONÓSTICO EXTENDIDO (5 DÍAS) - PAMPA HÚMEDA

# RESUMEN ESTADÍSTICO:
# - Temperatura promedio: 18.9°C
# - Temperatura máxima: 27.4°C
# - Temperatura mínima: 12.4°C
# - Humedad relativa promedio: 71.2%
# - Velocidad de viento promedio: 2.3 m/s

# TENDENCIAS OBSERVADAS:
# - Rango térmico: 15.0°C
# - Condiciones de viento: Calmo
# - Nivel de humedad: Alto

""" Generar plan de actividades con Gemini"""

prompt_planificacion = f"""Como asesor agropecuario especializado en la región pampeana, analiza este pronóstico extendido y genera un PLAN DE ACTIVIDADES DE CAMPO para los próximos 5 días:

{resumen_pronostico}

CONSIDERA EN TU ANÁLISIS:
- Cultivos típicos de la zona: soja, maíz, trigo
- Actividades agrícolas: pulverizaciones, fertilización, siembra, cosecha
- Condiciones óptimas para cada actividad
- Restricciones por viento, humedad y temperatura
- Seguridad de los operarios

GENERA:
1. CRONOGRAMA DIARIO de actividades recomendadas
2. VENTANAS ÓPTIMAS para aplicaciones
3. ACTIVIDADES A EVITAR en cada período
4. ALERTAS ESPECIALES si las hubiera
5. PREPARATIVOS recomendados

Formato: Día por día con horarios específicos."""

plan_actividades = consultar_gemini(prompt_planificacion)
print("=== PLAN DE ACTIVIDADES AGRÍCOLAS (5 DÍAS) ===")
console.print(Markdown(plan_actividades))

""" Resultado """

# Datos climáticos obtenidos:
# {'coord': {'lon': -57.5575, 'lat': -38.0023}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04n'}], 'base': 'stations', 'main': {'temp': 9.33, 'feels_like': 6.97, 'temp_min': 8.3, 'temp_max': 10.61, 'pressure': 1020, 'humidity': 63, 'sea_level': 1020, 'grnd_level': 1017}, 'visibility': 10000, 'wind': {'speed': 4.47, 'deg': 360, 'gust': 5.81}, 'clouds': {'all': 84}, 'dt': 1757890682, 'sys': 
# {'type': 2, 'id': 268283, 'country': 'AR', 'sunrise': 1757843515, 'sunset': 1757885988}, 'timezone': -10800, 'id': 3430863, 'name': 'Mar del Plata', 'cod': 200}
# === CONDICIONES CLIMÁTICAS ACTUALES ===
# Temperatura: 9.33°C
# Descripción: broken clouds
# Velocidad del viento: 4.47 m/s
# Humedad relativa: 63%
# Presión atmosférica: 1020 hPa
# REPORTE CLIMÁTICO - REGIÓN PAMPEANA
# Fecha: Tiempo actual
# Ubicación: Buenos Aires, Argentina

# CONDICIONES METEOROLÓGICAS:
# - Temperatura: 9.33°C
# - Condición general: broken clouds
# - Humedad relativa: 63%
# - Velocidad del viento: 4.47 m/s
# - Presión atmosférica: 1020 hPa

# === ANÁLISIS AGRONÓMICO CON GEMINI ===
# Claro que sí. Como agrónomo con experiencia en la región pampeana, procedo a realizar 
# un análisis técnico y práctico de las condiciones climáticas presentadas.

# Análisis General de la Situación

# Las condiciones descritas (9.3°C, 63% HR, viento de 16 km/h y alta presión) son       
# típicas de un día de otoño-invierno o principios de primavera en la provincia de      
# Buenos Aires. La alta presión (1020 hPa) sugiere estabilidad atmosférica, pero el     
# factor más limitante y riesgoso en este momento es la velocidad del viento.

# ──────────────────────────────────────────────────────────────────────────────────────              1. ¿Es un buen momento para aplicaciones de agroquímicos?

# Respuesta corta: No, no es un momento recomendable para aplicaciones foliares.        

# Análisis Técnico:

#  • Viento (Factor Crítico): Una velocidad de 4.47 m/s equivale a 16.1 km/h. Este valor   se encuentra por encima del umbral máximo recomendado para la mayoría de las       
#    aplicaciones, que suele ser de 12-15 km/h. Un viento de esta intensidad genera un  
#    riesgo muy alto de deriva, lo que implica:
#     • Pérdida de producto: El agroquímico no llega al objetivo (la maleza o el        
#       cultivo), reduciendo drásticamente la eficacia del tratamiento y malgastando    
#       dinero.
#     • Contaminación: El producto puede depositarse en lotes vecinos, cursos de agua,  
#       áreas sensibles o zonas urbanas, causando daños no deseados y potenciales       
#       problemas legales.
#     • Fitotoxicidad: Puede afectar a cultivos linderos que no son el objetivo de la   
#       aplicación.
#  • Temperatura: 9.3°C es una temperatura baja. Para la aplicación de herbicidas       
#    sistémicos (como el glifosato), la eficacia se ve reducida, ya que el metabolismo  
#    de las malezas es lento y la translocación del producto dentro de la planta es     
#    deficiente. Los herbicidas de contacto pueden funcionar mejor, pero aun así, la    
#    actividad biológica es baja.
#  • Humedad Relativa: 63% es una condición favorable. Es un buen nivel que evita la    
#    evaporación rápida de las gotas, permitiendo que el producto permanezca en estado  
#    líquido sobre la hoja por más tiempo y favoreciendo su absorción.

# Conclusión: A pesar de la buena humedad, el viento es el factor que anula por completola viabilidad de una aplicación segura y eficaz en este momento.

# ──────────────────────────────────────────────────────────────────────────────────────              2. ¿Qué precauciones deben tomar los operarios agrícolas?

# Independientemente de si se decide aplicar o no (lo cual no se recomienda), las       
# precauciones son fundamentales:

#  • Equipo de Protección Personal (EPP): Es obligatorio el uso de EPP completo: traje  
#    impermeable, guantes de nitrilo, botas de goma, máscara con filtros para vapores   
#    orgánicos y partículas, y protección ocular (antiparras). El viento aumenta el     
#    riesgo de que el rocío de la pulverización entre en contacto directo con el        
#    operario.
#  • Monitoreo en el Lote: No confiar únicamente en el reporte general. Medir la        
#    velocidad y dirección del viento en el lote y a la altura de la barra de aplicación   con un anemómetro de mano. El viento puede variar significativamente entre la      
#    cabecera y el centro del lote.
#  • Riesgo de Inversión Térmica: La alta presión atmosférica, combinada con cielo      
#    despejado (si las "broken clouds" se disipan hacia la tarde/noche) y viento que    
#    calma, son condiciones predisponentes para la inversión térmica. Si el viento      
#    amaina al atardecer, no aplicar. Las gotas finas quedan suspendidas en una capa de 
#    aire frío cerca del suelo y pueden viajar kilómetros de forma impredecible.        
#  • Tecnología de Aplicación: Si se viera obligado a aplicar en condiciones de viento  
#    moderado (límite de 12-15 km/h), es imperativo usar pastillas antideriva (con      
#    inducción de aire), reducir la presión de trabajo y bajar la altura del botalón    
#    para minimizar la deriva.

# ──────────────────────────────────────────────────────────────────────────────────────          3. ¿Cómo afectan estas condiciones a los cultivos de soja y maíz?

# Dado el período del año que sugiere la temperatura, el análisis se centra en el estadode post-cosecha o barbecho.

#  • Soja y Maíz (Campaña de Gruesa): Estos cultivos ya han sido cosechados. El impacto 
#    es sobre el rastrojo y el lote en preparación para la próxima siembra (trigo/cebada   o la gruesa siguiente).
#  • Manejo del Barbecho: La temperatura fresca y la humedad moderada son condiciones   
#    que pueden favorecer la germinación y el crecimiento lento de malezas de
#    otoño-invierno (ej. raigrás, rama negra, crucíferas). El viento seco puede resecar 
#    la capa superficial del suelo, pero la baja temperatura limita la pérdida de agua  
#    por evaporación.
#  • Cultivos de Cobertura: Si se sembró un cultivo de cobertura (ej. vicia, centeno),  
#    estas condiciones de temperatura fresca son adecuadas para su crecimiento
#    vegetativo, aunque sin tasas explosivas. El viento puede generar cierto estrés     
#    mecánico, pero no es perjudicial.
#  • Estrés por Frío: La temperatura por sí sola (9.3°C) no genera un daño directo, pero   sí ralentiza todos los procesos biológicos en el suelo y en las plantas. El        
#    principal riesgo asociado a estas condiciones en los próximos días sería la        
#    ocurrencia de heladas.

# ──────────────────────────────────────────────────────────────────────────────────────                    4. ¿Se recomienda riego en estas condiciones?

# Respuesta: No, de ninguna manera.

# Análisis Técnico:

#  • Baja Evapotranspiración (ET): La combinación de baja temperatura, nubosidad parcial   y humedad moderada resulta en una demanda hídrica atmosférica muy baja. Las plantas   (si las hubiera en activo crecimiento, como un trigo) transpiran muy poco.
#  • Balance Hídrico: Regar en estas condiciones sería ineficiente. El agua se
#    infiltraría lentamente en un suelo ya frío, enfriándolo aún más y pudiendo generar 
#    condiciones de anegamiento superficial si la infiltración es lenta.
#  • Eficiencia Energética y de Recurso: Sería un gasto innecesario de agua y energía   
#    (bombeo). El perfil del suelo en la región pampeana suele tener una buena recarga  
#    durante el otoño-invierno.

# ──────────────────────────────────────────────────────────────────────────────────────             5. Recomendaciones específicas para las próximas 24-48 horas

#  1 Suspender Aplicaciones Foliares: La prioridad número uno es no realizar
#    aplicaciones de pulverización hasta que el viento disminuya de forma sostenida por 
#    debajo de los 12 km/h.
#  2 Buscar la Ventana de Aplicación Correcta: Monitorear el pronóstico. La mejor       
#    oportunidad suele ser en las primeras horas de la mañana (6 a 9 AM), cuando el     
#    viento tiende a calmarse y la humedad relativa es mayor. Evitar el atardecer por el   riesgo de inversión térmica.
#  3 Monitoreo de Lotes: Aprovechar este tiempo para recorrer los campos. Realizar un   
#    relevamiento del estado y tamaño de las malezas. Una maleza pequeña y sin estrés es   más fácil de controlar cuando las condiciones mejoren.
#  4 Preparación de Maquinaria: Es un excelente momento para realizar la calibración del   pulverizador, limpiar filtros y picos, y asegurarse de tener las pastillas
#    adecuadas (antideriva) listas para cuando la ventana de aplicación se presente.    
#  5 Atención a las Heladas: Vigilar el pronóstico de temperatura mínima. Si hay        
#    cultivos de fina recién emergidos o pasturas sensibles, una helada podría
#    afectarlos. La alta presión y el cielo despejado por la noche aumentan este riesgo.
# En resumen, la jornada actual es para planificar y monitorear, no para ejecutar       
# aplicaciones. La paciencia y la toma de decisiones basada en datos medidos en el campo(especialmente el viento) son clave para una agricultura eficiente y responsable.     
# Pronóstico obtenido para 20 períodos de 3 horas
# PRONÓSTICO EXTENDIDO (5 DÍAS) - PAMPA HÚMEDA

# RESUMEN ESTADÍSTICO:
# - Temperatura promedio: 18.9°C
# - Temperatura máxima: 27.4°C
# - Temperatura mínima: 12.4°C
# - Humedad relativa promedio: 71.2%
# - Velocidad de viento promedio: 2.3 m/s

# TENDENCIAS OBSERVADAS:
# - Rango térmico: 15.0°C
# - Condiciones de viento: Calmo
# - Nivel de humedad: Alto
# === PLAN DE ACTIVIDADES AGRÍCOLAS (5 DÍAS) ===
# ¡Excelente iniciativa! Como asesor agropecuario para la región, aquí tienes un        
# análisis detallado y un plan de acción basado en el pronóstico proporcionado.

# ──────────────────────────────────────────────────────────────────────────────────────                             Análisis General del Asesor

# Colegas, el pronóstico para los próximos 5 días en la Pampa Húmeda presenta un        
# escenario muy particular: condiciones excelentes para el desarrollo de cultivos y la  
# siembra, pero de alto riesgo para las pulverizaciones y la proliferación de 
# enfermedades.

# La combinación de alta humedad relativa (71.2%), vientos calmos (2.3 m/s) y una gran  
# amplitud térmica (15°C) crea el cóctel perfecto para dos fenómenos clave:

#  1 Inversión Térmica: Durante las primeras horas de la mañana y al atardecer, el aire 
#    frío (más denso) queda atrapado cerca del suelo por una capa de aire más cálido.   
#    Cualquier aplicación en este momento resultará en una deriva incontrolable.        
#  2 Presión de Enfermedades Fúngicas: La alta humedad y las temperaturas moderadas son 
#    ideales para el desarrollo de royas, manchas foliares y fusarium, especialmente en 
#    trigos en etapas avanzadas y maíces tempranos.

# Nuestro plan debe ser, por lo tanto, maximizar las labores de siembra y fertilización,ser extremadamente precisos con las pulverizaciones y priorizar el monitoreo de lotes.
# ──────────────────────────────────────────────────────────────────────────────────────                    PLAN DE ACTIVIDADES DE CAMPO (Próximos 5 Días)

#                            1. CRONOGRAMA DIARIO RECOMENDADO

# Este cronograma es un modelo para cada uno de los próximos 5 días, dado que el        
# pronóstico es una media estable.

# Periodo Matutino Temprano (06:00 - 09:00 hs)

#  • Actividad Principal:
#     • Monitoreo de lotes: Es el momento ideal. Recorrer los trigos buscando presencia 
#       de royas (anaranjada, amarilla) y manchas. En maíces y sojas (si ya emergieron),      buscar daños por insectos o síntomas iniciales de enfermedades.
#     • Mantenimiento y Preparación: Engrase de maquinaria, carga de combustible,       
#       calibración final de sembradoras y pulverizadoras. Carga de insumos (semillas,  
#       fertilizantes).
#     • Traslado de maquinaria: Mover equipos a los lotes de trabajo del día.
#  • A EVITAR ABSOLUTAMENTE:
#     • Pulverizaciones: Riesgo máximo de deriva por inversión térmica. Las gotas       
#       quedarán suspendidas y se moverán sin control.
#     • Cosecha: Presencia de rocío en el cultivo y ambiente húmedo. El grano tendrá    
#       humedad excesiva.

# Periodo Matutino Medio (09:30 - 12:00 hs)

#  • Actividad Principal:
#     • Inicio de Siembra/Fertilización: El suelo ha perdido el rocío superficial, las  
#       condiciones son óptimas.
#     • Inicio de Cosecha (trigo/cebada): El rocío ya se ha evaporado. Comenzar a medir 
#       humedad del grano para dar inicio a la trilla.
#     • INICIO DE VENTANA DE PULVERIZACIÓN (ver punto 2): La inversión térmica ya se ha 
#       roto. El viento es ideal (ni calmo ni fuerte) y la temperatura aún es moderada. 
#  • A EVITAR:
#     • Apresurarse a pulverizar antes de las 9:30 si las condiciones no son claras     
#       (neblina, calma total).

# Periodo Mediodía y Tarde Temprana (12:00 - 16:00 hs)

#  • Actividad Principal:
#     • Plena Actividad: Continuar a ritmo sostenido con la siembra, fertilización y    
#       cosecha. Es el período de máxima eficiencia.
#     • Continuación de Pulverizaciones: Monitorear constantemente la temperatura. Si se      acerca a los 27°C, evaluar el riesgo de evaporación y fitotoxicidad según el    
#       producto a aplicar.
#  • A EVITAR:
#     • Pulverizar con productos hormonales (ej. 2,4-D) si la temperatura supera los    
#       25°C, por alto riesgo de volatilización.

# Periodo Tarde-Noche (16:30 - 19:00 hs)

#  • Actividad Principal:
#     • Finalización de labores: Concluir las tareas de siembra y cosecha del día.      
#     • Limpieza de equipos: Es fundamental limpiar la pulverizadora si se cambia de    
#       producto o lote al día siguiente.
#  • A EVITAR ABSOLUTAMENTE:
#     • Iniciar nuevas pulverizaciones: A partir de las 16:30-17:00 hs, el riesgo de    
#       inversión térmica regresa a medida que el suelo se enfría. Finalizar cualquier  
#       aplicación en curso con suficiente antelación.

# ──────────────────────────────────────────────────────────────────────────────────────               2. VENTANAS ÓPTIMAS PARA APLICACIONES (Pulverizaciones)

# La ventana de aplicación segura y efectiva será estrecha y crítica.

#  • Horario Estimado: Entre las 09:30 hs y las 16:00 hs.
#  • Condiciones a verificar EN EL LOTE (no solo por pronóstico):
#     1 Temperatura: Inferior a 25°C.
#     2 Humedad Relativa: Superior al 50% (el pronóstico promedio de 71% es excelente   
#       para evitar evaporación de gotas).
#     3 Viento: Constante y ligero, entre 5 y 15 km/h. El promedio de 8.3 km/h (2.3 m/s)      es ideal, pero hay que asegurarse que no haya calma total.
#     4 Ausencia de Inversión Térmica: Realizar una prueba de humo o simplemente        
#       observar el polvo de la camioneta. Si el humo/polvo no se eleva y dispersa, sino      que flota en una capa horizontal, NO APLICAR.

# ──────────────────────────────────────────────────────────────────────────────────────                       3. ACTIVIDADES A EVITAR EN CADA PERÍODO

#  • Mañana Temprana y Atardecer: CUALQUIER TIPO DE PULVERIZACIÓN.
#  • Mañana con Rocío: Cosecha de trigo/cebada. Fertilización con urea sobre el cultivo 
#    (riesgo de quemado por concentración de la solución en las gotas de rocío).        
#  • Mediodía (si la T° supera 25-27°C): Aplicación de herbicidas hormonales volátiles. 

# ──────────────────────────────────────────────────────────────────────────────────────                                4. ALERTAS ESPECIALES

#  • ALERTA ROJA - RIESGO DE DERIVA: La condición de vientos calmos y alta amplitud     
#    térmica es la más peligrosa para la deriva. Una aplicación mal realizada en estas  
#    condiciones puede afectar a lotes vecinos, cultivos sensibles, áreas periurbanas y 
#    cursos de agua. La responsabilidad legal y ambiental es máxima.
#  • ALERTA AMARILLA - PRESIÓN DE ENFERMEDADES FÚNGICAS: Las condiciones son de
#    incubadora. El monitoreo no es una opción, es una obligación. Una detección tardía 
#    de roya en trigo puede significar una pérdida de rinde irrecuperable. Estar        
#    preparados para una aplicación de fungicida en la ventana óptima.

# ──────────────────────────────────────────────────────────────────────────────────────                             5. PREPARATIVOS RECOMENDADOS

#  1 Calibración de Equipos: Antes de salir al campo, asegurar que la pulverizadora esté   perfectamente calibrada. Utilizar pastillas anti-deriva (ej. con inducción de aire)   es altamente recomendable.
#  2 Medición en Campo: Contar con un anemómetro de mano y un termohigrómetro para medir   las condiciones reales en el lote antes y durante la aplicación. No confiar        
#    ciegamente en el pronóstico general.
#  3 Plan de Monitoreo: Definir qué lotes son prioritarios para revisar cada día. Llevar   lupas de mano y bolsas para tomar muestras si es necesario.
#  4 Logística de Insumos: Tener semillas, fertilizantes y fitosanitarios listos y en el   campo para aprovechar al máximo las ventanas operativas.
#  5 Seguridad del Operario:
#     • Hidratación: Aunque las temperaturas no son extremas, las jornadas serán largas.      Asegurar provisión de agua fresca.
#     • EPP (Equipo de Protección Personal): Indispensable para el mezclador y aplicador      durante las pulverizaciones (guantes, máscara, traje impermeable).
#     • Descanso: Planificar las jornadas para evitar la fatiga, que es causa de        
#       accidentes y errores.

# Este plan le permitirá navegar una semana climáticamente favorable pero técnicamente  
# desafiante. La clave será la disciplina, el monitoreo constante y el respeto estricto 
# por las buenas prácticas agrícolas. ¡A su disposición para cualquier consulta

""" Comparación Regional con Análisis Multi-zona """

# Definir regiones agrícolas argentinas
regiones_agricolas = {
    "Pampa Húmeda": (-33.7, -60.5),
    "Cuyo": (-32.9, -68.8),
    "NOA (Salta)": (-26.8, -65.2),
    "NEA (Corrientes)": (-27.5, -58.8),
    "Patagonia Norte": (-41.8, -68.9)
}

def obtener_datos_clima_region(lat, lon):
    """Obtiene datos climáticos para una región específica"""
    url = f"https://api.openweathermap.org/data/2.5/weather?units=metric&lat={lat}&lon={lon}&appid={api_key}"
    try:
        response = requests.get(url)
        data = response.json()
        return {
            'temp': data['main']['temp'],
            'humedad': data['main']['humidity'],
            'viento': data['wind']['speed'],
            'descripcion': data['weather'][0]['description']
        }
    except Exception as e:
        print(f"Error obteniendo datos: {e}")
        return None

# Recopilar datos de todas las regiones
datos_regionales = {}
for region, coords in regiones_agricolas.items():
    print(f"Obteniendo datos para {region}...")
    datos = obtener_datos_clima_region(coords[0], coords[1])
    if datos:
        datos_regionales[region] = datos

print(f"\nDatos obtenidos para {len(datos_regionales)} regiones")

""" Resultado """

# Este plan le permitirá operar de manera segura y eficiente, convirtiendo un pronósticocon riesgos ocultos en una oportunidad productiva. Quedo a su disposición para        
# cualquier consulta.
# Obteniendo datos para Pampa Húmeda...
# Obteniendo datos para Cuyo...
# Obteniendo datos para NOA (Salta)...
# Obteniendo datos para NEA (Corrientes)...
# Obteniendo datos para Patagonia Norte...

# Datos obtenidos para 5 regiones

""" Visualizar comparación regional """

if datos_regionales:
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 15))

    regiones = list(datos_regionales.keys())
    temps = [datos['temp'] for datos in datos_regionales.values()]
    hums = [datos['humedad'] for datos in datos_regionales.values()]
    vientos = [datos['viento'] for datos in datos_regionales.values()]

    # Gráfico de temperaturas
    bars1 = ax1.bar(regiones, temps, color='red', alpha=0.7)
    ax1.set_title('Temperatura por Región Agrícola', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Temperatura (°C)')
    ax1.tick_params(axis='x', rotation=45)

    # Agregar valores sobre barras
    for bar, temp in zip(bars1, temps):
        ax1.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.3,
                f'{temp:.1f}°C', ha='center', va='bottom')

    # Gráfico de humedad
    bars2 = ax2.bar(regiones, hums, color='blue', alpha=0.7)
    ax2.set_title('Humedad Relativa por Región', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Humedad (%)')
    ax2.tick_params(axis='x', rotation=45)

    for bar, hum in zip(bars2, hums):
        ax2.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1,
                f'{hum:.0f}%', ha='center', va='bottom')

    # Gráfico de viento
    bars3 = ax3.bar(regiones, vientos, color='green', alpha=0.7)
    ax3.set_title('Velocidad del Viento por Región', fontsize=14, fontweight='bold')
    ax3.set_ylabel('Velocidad del Viento (m/s)')
    ax3.set_xlabel('Regiones Agrícolas')
    ax3.tick_params(axis='x', rotation=45)

    for bar, viento in zip(bars3, vientos):
        ax3.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.1,
                f'{viento:.1f}', ha='center', va='bottom')

    plt.tight_layout()
    plt.show()

    print("=== DATOS REGIONALES COMPARATIVOS ===")
    for region, datos in datos_regionales.items():
        print(f"{region}: {datos['temp']:.1f}°C, {datos['humedad']}% HR, {datos['viento']:.1f} m/s - {datos['descripcion']}")

""" Resultado """

#   Datos obtenidos para 5 regiones
# === DATOS REGIONALES COMPARATIVOS ===
# Pampa Húmeda: 19.8°C, 72% HR, 4.2 m/s - scattered clouds
# Cuyo: 19.8°C, 28% HR, 3.1 m/s - clear sky
# NOA (Salta): 22.1°C, 53% HR, 0.8 m/s - scattered clouds
# NEA (Corrientes): 22.8°C, 84% HR, 0.9 m/s - scattered clouds
# Patagonia Norte: 7.9°C, 37% HR, 6.2 m/s - clear sky    

# Análisis comparativo con Gemini
if datos_regionales:
    prompt_regional = f"""Como especialista en agricultura argentina, analiza las siguientes condiciones climáticas actuales en las principales regiones agrícolas del país:

{datos_regionales}

Proporciona un ANÁLISIS REGIONAL COMPARATIVO que incluya:

1. **CONDICIONES ÓPTIMAS**: ¿Qué región tiene las mejores condiciones hoy?
2. **CULTIVOS RECOMENDADOS**: ¿Qué cultivos son más apropiados para cada región según estas condiciones?
3. **ACTIVIDADES PRIORITARIAS**: ¿Qué actividades agrícolas se deberían realizar hoy en cada región?
4. **ALERTAS REGIONALES**: ¿Qué precauciones específicas debe tomar cada región?
5. **OPORTUNIDADES**: ¿Qué ventajas competitivas temporales tiene cada zona?

Considera:
- Cultivos típicos de cada región
- Épocas de siembra/cosecha por zona
- Sensibilidad climática de diferentes cultivos
- Logística y operaciones de campo

Respuesta técnica pero práctica para productores."""

    analisis_regional = consultar_gemini(prompt_regional)
    print("=== ANÁLISIS REGIONAL COMPARATIVO CON GEMINI ===")
    console.print(Markdown(analisis_regional))
else:
    print("No se pudieron obtener datos regionales para el análisis")
   
""" Resultado """

# === ANÁLISIS REGIONAL COMPARATIVO CON GEMINI ===
# Excelente. Como especialista en agronomía y conocedor de las realidades productivas deArgentina, procedo a realizar un análisis técnico y práctico basado en los datos      
# proporcionados.

# ──────────────────────────────────────────────────────────────────────────────────────                 ANÁLISIS AGROCLIMÁTICO COMPARATIVO PARA EL PRODUCTOR

# A continuación, se detalla el impacto de las condiciones actuales en cada una de las  
# principales regiones productivas del país, con recomendaciones específicas para la    
# toma de decisiones en el campo.

#         1. CONDICIONES ÓPTIMAS: ¿Qué región tiene las mejores condiciones hoy?        

# La región con las condiciones más favorables para la actividad agrícola hoy es Cuyo.  

#  • Justificación: Presenta una combinación ideal de temperatura templada (16.8°C),    
#    cielo despejado que maximiza la radiación solar, y una humedad relativa baja (36%).   Esta "ventana climática" es perfecta para una amplia gama de tareas de campo que   
#    requieren suelo seco, buena visibilidad y máxima eficiencia en las aplicaciones,   
#    como la cosecha de cultivos de ciclo tardío o la aplicación de fitosanitarios. La  
#    Pampa Húmeda está limitada por la lluvia, el NEA por la altísima humedad y la      
#    Patagonia por el frío extremo.

#              2. CULTIVOS RECOMENDADOS: ¿Qué favorecen estas condiciones?

#  • Pampa Húmeda: La lluvia ligera sobre un perfil que venía necesitando agua es       
#    excelente para los cereales de invierno recién implantados o por implantar (trigo, 
#    cebada). Esta humedad asegura una buena germinación y emergencia. No es un día para   sembrar, pero la condición del suelo mejora notablemente para el futuro cercano.   
#  • Cuyo: Las condiciones son óptimas para la cosecha de la vid (variedades tardías) y 
#    del olivo, ya que la baja humedad reduce el riesgo de desarrollo de hongos en la   
#    fruta y facilita el secado. También es ideal para el desarrollo de hortalizas de   
#    bulbo como ajo y cebolla, que se benefician del tiempo soleado y seco.
#  • NOA (Salta): El clima templado y la humedad moderada (68%) son muy favorables para 
#    el desarrollo vegetativo de legumbres como el poroto en sus etapas finales. También   beneficia a los cultivos de tabaco en etapas de crecimiento, ya que evita el estrés   hídrico sin generar una presión excesiva de enfermedades.
#  • NEA (Corrientes): Las altas temperaturas y el sol son ideales para cultivos        
#    subtropicales perennes. Favorece la fotosíntesis y producción en yerba mate, té y  
#    cítricos. Estos cultivos están adaptados a la alta humedad ambiental, aunque esta  
#    condición eleva el riesgo sanitario.
#  • Patagonia Norte: El frío es fundamental para los frutales de pepita (manzana, pera)   y carozo (cereza). Estas bajas temperaturas contribuyen a la acumulación de "horas 
#    de frío", un requisito indispensable para romper la dormancia y asegurar una       
#    floración uniforme y vigorosa en la primavera.

#                3. ACTIVIDADES PRIORITARIAS: ¿Qué hacer hoy en el campo?

#  • Pampa Húmeda: "Día de galpón". La lluvia y la humedad impiden el tránsito de       
#    maquinaria. Las prioridades son:
#     • Mantenimiento y regulación de sembradoras y pulverizadoras.
#     • Planificación de la siembra de fina (trigo/cebada).
#     • Control de stock de insumos (semillas, fertilizantes).
#     • Monitoreo de la humedad en granos almacenados.
#  • Cuyo: Máxima actividad a campo.
#     • Prioridad 1: Cosecha. Finalizar la recolección de uvas, olivos o nogales.       
#     • Prioridad 2: Aplicaciones Fitosanitarias. Condiciones perfectas (sin lluvia,    
#       poco viento) para aplicar herbicidas en presiembra o fungicidas/insecticidas con      máxima eficiencia y mínimo riesgo de deriva.
#     • Labores de preparación de suelo para siembras de invierno.
#  • NOA (Salta): Monitoreo y tareas de bajo impacto.
#     • Recorrida y monitoreo de lotes (scouting): La humedad y temperatura son
#       propicias para la aparición de insectos (p. ej., chinches en poroto).
#     • Tareas de logística y movimiento de equipos.
#     • Aplicaciones de fertilizantes foliares si el cultivo lo requiere.
#  • NEA (Corrientes): Foco en sanidad y riego.
#     • Monitoreo intensivo de enfermedades fúngicas en cítricos (sarna, melanosis) y   
#       yerbatales. La alta humedad es un caldo de cultivo.
#     • Verificación y mantenimiento de sistemas de riego.
#     • Tareas de poda o desmalezado que se beneficien del buen tiempo.
#  • Patagonia Norte: Gestión del frío y preparación para la dormancia.
#     • Activar sistemas de defensa anti-helada (riego por aspersión, ventiladores) si  
#       el pronóstico indica que la temperatura bajará más durante la noche.
#     • Planificar e iniciar tareas de poda en los montes frutales.
#     • Revisar la protección de viveros o plantaciones jóvenes.

#                    4. ALERTAS REGIONALES: Precauciones específicas

#  • Pampa Húmeda: ALERTA ROJA por enfermedades fúngicas. La combinación de lluvia (84% 
#    humedad) y temperaturas templadas crea un escenario ideal para la aparición de     
#    royas y manchas foliares en los primeros estadios del trigo/cebada. Monitorear de  
#    cerca en los próximos días.
#  • Cuyo: ALERTA por estrés hídrico a futuro. La baja humedad acelera la
#    evapotranspiración. Aunque hoy es bueno, es un recordatorio de que las reservas de 
#    agua (diques, acuíferos) son críticas. Se debe gestionar el riego con máxima       
#    eficiencia.
#  • NOA (Salta): ALERTA por plagas. Las condiciones de nubes, humedad media y
#    temperatura cálida son favorables para la actividad y reproducción de insectos. Es 
#    un día clave para el monitoreo.
#  • NEA (Corrientes): ALERTA MÁXIMA por presión fúngica. Con 87% de humedad, cualquier 
#    herida en las plantas o follaje denso es una puerta de entrada para hongos. El     
#    riesgo de enfermedades en cítricos, hortalizas y otros cultivos es extremadamente  
#    alto.
#  • Patagonia Norte: ALERTA MÁXIMA por heladas. Una temperatura de 5.97°C con cielo    
#    despejado ("few clouds") indica una alta probabilidad de helada radiativa durante  
#    la noche, donde la temperatura a nivel del suelo puede caer por debajo de 0°C.     
#    Cualquier cultivo sensible que no esté en dormancia corre grave peligro.

#                   5. OPORTUNIDADES: Ventajas competitivas temporales

#  • Pampa Húmeda: Oportunidad de Recarga del Perfil Hídrico. Esta lluvia, aunque       
#    detenga las labores, es "oro en polvo" para asegurar la humedad inicial para la    
#    campaña de fina, reduciendo la dependencia de lluvias futuras y dando una ventaja  
#    estratégica para el arranque del cultivo.
#  • Cuyo: Oportunidad para Calidad y Eficiencia. Es un día para lograr una cosecha de  
#    altísima calidad (sin humedad) y realizar aplicaciones fitosanitarias con una      
#    eficiencia cercana al 100%, optimizando costos y resultados.
#  • NOA (Salta): Oportunidad de Crecimiento sin Estrés. El clima balanceado ("ni frío  
#    ni calor, ni seco ni ahogado") permite que los cultivos maximicen su tasa de       
#    crecimiento sin gastar energía en defenderse de condiciones extremas.
#  • NEA (Corrientes): Oportunidad de Máxima Producción Fotosintética. El cielo
#    despejado y las altas temperaturas maximizan la captación de energía solar. Para   
#    cultivos perennes y bien regados como los cítricos, esto se traduce directamente en   más azúcares para el llenado de frutos.
#  • Patagonia Norte: Oportunidad de Inducción a una Dormancia Profunda y Uniforme. El  
#    golpe de frío es una señal fisiológica clave para los frutales. Un correcto        
#    descanso invernal es el pilar para una brotación y floración homogénea en
#    primavera, lo que se traduce en una producción más pareja y de mayor calibre. 