import openai
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from openai import OpenAI
from datetime import datetime, timedelta
import warnings
from dotenv import load_dotenv
warnings.filterwarnings('ignore')

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))




"""## Capítulo 1: Análisis Predictivo en la Agricultura

   ## Predicción de Riesgos de Plagas con Machine Learning + LLM"""





# # Función para obtener respuestas especializadas del LLM
# def obtener_analisis_agricola(prompt, modelo="gpt-4o"):
#     response = client.chat.completions.create(
#         model=modelo,
#         messages=[
#             {"role": "system", "content": "Eres un experto agrónomo especializado en agricultura de precisión y análisis de datos agrícolas."},
#             {"role": "user", "content": prompt}
#         ],
#         max_tokens=1000
#     )
#     return response.choices[0].message.content

# # Generación de datos sintéticos para el modelo predictivo
# np.random.seed(42)

# # Datos de muestra: [humedad_del_suelo, temperatura, humedad_relativa, velocidad_viento, precipitacion]
# n_samples = 1000
# X = np.random.rand(n_samples, 5) * np.array([100, 40, 100, 30, 50])  # Escalas realistas

# # Crear etiquetas basadas en condiciones lógicas
# # Riesgo alto si: humedad alta (>70), temperatura moderada (20-30), viento bajo (<10)
# y = ((X[:, 0] > 70) & (X[:, 1] > 20) & (X[:, 1] < 30) & (X[:, 3] < 10)).astype(int)

# # Añadir algo de ruido para hacer más realista
# noise_indices = np.random.choice(n_samples, size=int(0.1 * n_samples), replace=False)
# y[noise_indices] = 1 - y[noise_indices]

# print(f"Dataset generado: {n_samples} muestras")
# print(f"Distribución de clases - Sin plagas: {np.sum(y==0)}, Con plagas: {np.sum(y==1)}")

""" Resultado """

# Dataset generado: 1000 muestras
# Distribución de clases - Sin plagas: 879, Con plagas: 121

"""Entrenar el modelo predictivo"""
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# model = RandomForestClassifier(n_estimators=100, random_state=42)
# model.fit(X_train, y_train)

# # Evaluar el modelo
# y_pred = model.predict(X_test)
# accuracy = accuracy_score(y_test, y_pred)
# print(f"Precisión del modelo: {accuracy:.3f}")
# print("\nReporte de clasificación:")
# print(classification_report(y_test, y_pred, target_names=['Sin Plagas', 'Con Plagas']))

""" Resultado """
# Reporte de clasificación:
#               precision    recall  f1-score   support

#   Sin Plagas       0.89      0.99      0.94       176
#   Con Plagas       0.67      0.08      0.15        24

#     accuracy                           0.89       200
#    macro avg       0.78      0.54      0.54       200
# weighted avg       0.86      0.89      0.84       200

"""Análisis en tiempo real con nuevos datos de sensores"""

# nuevos_datos = np.array([[75, 25, 85, 8, 12]])  # [humedad_suelo, temp, humedad_rel, viento, precipitacion]

# # Predecir riesgo de plagas
# prediccion = model.predict(nuevos_datos)[0]
# probabilidad = model.predict_proba(nuevos_datos)[0]

# # Interpretar resultados
# if prediccion == 1:
#     riesgo = f"ALTO riesgo de infestación de plagas con una probabilidad de {probabilidad[1]*100:.1f}%."
# else:
#     riesgo = f"BAJO riesgo de infestación de plagas con una probabilidad de {probabilidad[0]*100:.1f}%."

# print(f"Condiciones actuales:")
# print(f"- Humedad del suelo: {nuevos_datos[0][0]}%")
# print(f"- Temperatura: {nuevos_datos[0][1]}°C")
# print(f"- Humedad relativa: {nuevos_datos[0][2]}%")
# print(f"- Velocidad del viento: {nuevos_datos[0][3]} km/h")
# print(f"- Precipitación: {nuevos_datos[0][4]} mm")
# print(f"\nRESULTADO: {riesgo}")

""" Resultado """

# Condiciones actuales:
# - Humedad del suelo: 75%
# - Temperatura: 25°C
# - Humedad relativa: 85%
# - Velocidad del viento: 8 km/h
# - Precipitación: 12 mm

# RESULTADO: BAJO riesgo de infestación de plagas con una probabilidad de 76.0%.

"""Generar informe completo usando LLM"""

# datos_sensores = f"""Humedad del suelo: {nuevos_datos[0][0]}%, 
# Temperatura: {nuevos_datos[0][1]}°C, 
# Humedad relativa: {nuevos_datos[0][2]}%, 
# Velocidad del viento: {nuevos_datos[0][3]} km/h, 
# Precipitación: {nuevos_datos[0][4]} mm"""

# prompt = f"""Basado en la siguiente evaluación de riesgos de plagas: {riesgo}
# Y las condiciones ambientales: {datos_sensores}

# Genera un informe técnico completo que incluya:
# 1. Análisis de las condiciones actuales
# 2. Explicación del nivel de riesgo
# 3. Recomendaciones específicas de manejo
# 4. Cronograma de monitoreo
# 5. Medidas preventivas inmediatas"""

# informe = obtener_analisis_agricola(prompt)
# print("=== INFORME DE ANÁLISIS PREDICTIVO ===")
# print(informe)

""" Resultado """

# RESULTADO: BAJO riesgo de infestación de plagas con una probabilidad de 76.0%.
# === INFORME DE ANÁLISIS PREDICTIVO ===
# ### Informe Técnico sobre Condiciones de Cultivo y Manejo de Riesgos de Plagas

# #### 1. Análisis de las Condiciones Actuales

# - **Humedad del Suelo:** Con un 75% de humedad, el suelo se encuentra en un nivel óptimo para la mayoría de los cultivos, asegurando una buena disponibilidad de agua para la 
# absorción de nutrientes.
# - **Temperatura:** Los 25°C son ideales para el crecimiento de muchas plantas, especialmente las que se desarrollan en climas cálidos. Esta temperatura favorece la fotosíntesis y el metabolismo vegetal.
# - **Humedad Relativa:** Un 85% de humedad relativa es alta y puede favorecer el desarrollo de enfermedades fúngicas si se mantiene por periodos prolongados.
# - **Velocidad del Viento:** A 8 km/h, la velocidad del viento es moderada y no representa un riesgo inmediato para el cultivo en términos de deshidratación o daño físico.    
# - **Precipitación:** 12 mm de precipitación sugiere un riego adecuado del suelo, pero es necesario monitorear para evitar encharcamientos que puedan llevar a la asfixia de las raíces o el desarrollo de hongos.

# #### 2. Explicación del Nivel de Riesgo

# El nivel de riesgo de infestación de plagas es BAJO, con una probabilidad del 76%. Este bajo riesgo puede atribuirse al control efectivo de plagas existentes, condiciones climáticas que no favorecen su desarrollo rápidamente, o a intervenciones previas efectivas. Sin embargo, con condiciones moderadamente húmedas y temperaturas cálidas, sigue existiendo un potencial para el desarrollo de plagas si las condiciones cambian.

# #### 3. Recomendaciones Específicas de Manejo

# - **Monitoreo Regular:** Continuar con la vigilancia de posibles signos de plagas y enfermedades, especialmente los hongos que puedan surgir debido a la alta humedad relativa.
# - **Manejo del Riego:** Ajustar el riego para mantener la humedad del suelo en niveles 
# óptimos sin causar saturación. Esto ayudará a prevenir condiciones que favorecen enfermedades.
# - **Control Biológico:** Evaluar la introducción de controladores biológicos como insectos benéficos que puedan ayudar a mantener el equilibrio ecológico y reducir posibilidades de infestación.

# #### 4. Cronograma de Monitoreo

# - **Diario:** Inspección visual del follaje y la base de las plantas para detectar signos tempranos de enfermedades fúngicas o presencia de plagas.
# - **Semanal:** Revisión detallada de las trampas de feromonas y conteo de insectos capturados para análisis de tendencias poblacionales de plagas.
# - **Quincenal:** Análisis de la humedad del suelo y ajustes de riego según las condiciones climáticas y necesidades específicas del cultivo.

# #### 5. Medidas Preventivas Inmediatas

# - **Ventilación Adecuada:** En cultivos de invernadero, ajustar los sistemas de ventilación para reducir la humedad relativa y minimizar el riesgo de hongos.
# - **Aplicación de Fungicidas Naturales:** Considerar productos de bajo impacto ambiental en áreas propensas a la formación de hongos.
# - **Cercado y Protección Física:** Asegurar que los cercados o barreras físicas están intactos para prevenir la entrada de plagas.

# Este informe proporciona una visión clara y comprensible de las condiciones actuales y 
# los pasos recomendados para mantener un ambiente que minimice los riesgos de plagas. Es crucial mantener la flexibilidad para adaptarse a cambios en las condiciones climatológicas y de crecimiento del cultivo.



"""## Capítulo 2: Técnicas de Agricultura de Precisión

   ## Análisis Multi-Sensor para Recomendaciones Personalizadas"""


"""Simulación de datos de sensores IoT en tiempo real"""
# class SensorData:
#     def __init__(self, zona):
#         self.zona = zona
#         self.timestamp = datetime.now()
        
#     def generar_datos(self):
#         return {
#             "zona": self.zona,
#             "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
#             "soil_moisture": np.random.normal(35, 10),  # Humedad del suelo en %
#             "temperature": np.random.normal(22, 5),     # Temperatura en °C
#             "ph": np.random.normal(6.5, 0.5),          # pH del suelo
#             "nutrient_levels": {
#                 "nitrogen": np.random.normal(50, 15),   # ppm
#                 "phosphorus": np.random.normal(30, 10), # ppm
#                 "potassium": np.random.normal(40, 12)   # ppm
#             },
#             "crop_stage": np.random.choice(["siembra", "vegetativa", "floración", "maduración"])
#         }

# # Generar datos para múltiples zonas
# zonas = ["Norte", "Sur", "Este", "Oeste"]
# datos_sensores = {}

# for zona in zonas:
#     sensor = SensorData(zona)
#     datos_sensores[zona] = sensor.generar_datos()
    
# # Mostrar datos generados
# for zona, datos in datos_sensores.items():
#     print(f"\n=== ZONA {zona} ===")
#     print(f"Humedad del suelo: {datos['soil_moisture']:.1f}%")
#     print(f"Temperatura: {datos['temperature']:.1f}°C")
#     print(f"pH: {datos['ph']:.1f}")
#     print(f"Nitrógeno: {datos['nutrient_levels']['nitrogen']:.0f} ppm")
#     print(f"Fósforo: {datos['nutrient_levels']['phosphorus']:.0f} ppm")
#     print(f"Potasio: {datos['nutrient_levels']['potassium']:.0f} ppm")
#     print(f"Etapa del cultivo: {datos['crop_stage']}")

""" Resultado """

# En resumen, el enfoque basado en datos sugiere que, aunque el riesgo de plagas es actualmente bajo, una estrategia de prevención activa y monitoreo continuo es esencial para 
# mantener las poblaciones de plagas bajo control. Dado que las condiciones ambientales son decisivas, cada pequeña variación debe ser evaluada en tiempo real para ajustar las 
# tácticas de manejo de plagas.

# === ZONA Norte ===
# Humedad del suelo: 43.8%
# Temperatura: 21.9°C
# pH: 6.4
# Nitrógeno: 69 ppm
# Fósforo: 36 ppm
# Potasio: 36 ppm
# Etapa del cultivo: siembra

# === ZONA Sur ===
# Humedad del suelo: 37.9%
# Temperatura: 18.3°C
# pH: 6.5
# Nitrógeno: 57 ppm
# Fósforo: 32 ppm
# Potasio: 45 ppm
# Etapa del cultivo: siembra

# === ZONA Este ===
# Humedad del suelo: 27.3%
# Temperatura: 21.7°C
# pH: 6.2
# Nitrógeno: 65 ppm
# Fósforo: 35 ppm
# Potasio: 72 ppm
# Etapa del cultivo: floración

# === ZONA Oeste ===
# Humedad del suelo: 30.8%
# Temperatura: 23.7°C
# pH: 6.7
# Nitrógeno: 37 ppm
# Fósforo: 25 ppm
# Potasio: 53 ppm
# Etapa del cultivo: siembra


"""Análisis y recomendaciones personalizadas por zona"""

# for zona, datos in datos_sensores.items():
#     # Crear descripción de datos para el LLM
#     data_description = f"""Zona: {zona}
#     Humedad del suelo: {datos['soil_moisture']:.1f}%
#     Temperatura: {datos['temperature']:.1f}°C
#     pH del suelo: {datos['ph']:.1f}
#     Niveles de nutrientes:
#     - Nitrógeno: {datos['nutrient_levels']['nitrogen']:.0f} ppm
#     - Fósforo: {datos['nutrient_levels']['phosphorus']:.0f} ppm
#     - Potasio: {datos['nutrient_levels']['potassium']:.0f} ppm
#     Etapa del cultivo: {datos['crop_stage']}"""
    
#     prompt = f"""Analiza los siguientes datos de sensores de agricultura de precisión y proporciona 
#     recomendaciones específicas y técnicas para:
    
#     1. Programa de riego optimizado
#     2. Plan de fertilización específico
#     3. Ajustes de pH si son necesarios
#     4. Cronograma de actividades según la etapa del cultivo
#     5. Alertas o precauciones especiales
    
#     Datos de la zona:
#     {data_description}
    
#     Proporciona recomendaciones técnicas precisas con cantidades específicas."""
    
#     recommendations = obtener_analisis_agricola(prompt)
#     print(f"\n{'='*50}")
#     print(f"RECOMENDACIONES PARA ZONA {zona}")
#     print(f"{'='*50}")
#     print(recommendations)
#     print("\n")

""" Resultado """

# ==================================================
# RECOMENDACIONES PARA ZONA Norte
# ==================================================
# Para desarrollar un plan técnico basado en los datos proporcionados, es esencial considerar las condiciones actuales y las necesidades típicas del cultivo en la etapa de siembra. Las recomendaciones a continuación están orientadas a optimizar el rendimiento y la salud del cultivo.

# ### 1. Programa de riego optimizado

# - **Revisar capacidad de campo y lluvias recientes**: Aunque la humedad actual del suelo está en un 43.8%, lo cual es generalmente adecuado para la mayoría de los cultivos en etapa de siembra, es crucial monitorear el balance hídrico según la capacidad de campo específica del suelo de la zona.
# - **Frecuencia y cantidad**: Implementar un sistema de riego localizado, como el riego 
# por goteo, para mantener la humedad en el rango óptimo (generalmente entre 50-70% de la capacidad de campo). Realizar riegos ligeros de 10-15 mm cada 3-4 días, dependiendo de las precipitaciones y la evapotranspiración, para no sobresaturar el suelo y favorecer un buen desarrollo del sistema radicular.

# ### 2. Plan de fertilización específico

# - **Nitrógeno**: Con 69 ppm, el nivel de nitrógeno es moderado. Considerando la etapa de siembra, iniciar con una aplicación de 30-40 kg/ha de nitrógeno para favorecer el enraizamiento inicial. Usar urea o un fertilizante de liberación controlada para lograr un efecto prolongado.
# - **Fósforo**: El nivel de fósforo es bajo para muchas especies, siendo crucial para el desarrollo radicular inicial. Aplicar superfosfato triple a razón de 50-60 kg/ha inmediatamente después de la siembra o incorporado al momento de la siembra para garantizar 
# su disponibilidad inmediata.
# - **Potasio**: Los niveles de potasio están también en la parte baja para numerosas especies. Sugiero una aplicación de 40-50 kg/ha de K2O para equilibrar el suelo y promover la resistencia del cultivo a enfermedades.

# ### 3. Ajustes de pH si son necesarios

# - **Evaluación de pH**: Con un pH de 6.4, el suelo está dentro de un rango ligeramente 
# ácido, que es generalmente adecuado para la mayoría de los cultivos. No se requieren ajustes de pH inmediatos. Continuar el monitoreo, ya que condiciones más ácidas (menores 
# a 6) podrían requerir enmiendas con cal agrícola.

# ### 4. Cronograma de actividades según la etapa del cultivo

# - **Primera semana (siembra)**: Verificar la calidad de la semilla, la uniformidad de la siembra, y aplicar el plan de fertilización básica.
# - **Segunda a cuarta semana (emergencia y establecimiento)**:
#   - Monitorear emergencias y realizar resiembras si es necesario.
#   - Implementar control inicial de malezas.
#   - Continuar con el programa de riego y ajustar según las necesidades climáticas.     

# ### 5. Alertas o precauciones especiales

# - **Monitoreo del clima**: En el norte, el clima puede variar; los vientos fuertes o heladas tempranas son un riesgo a tener en cuenta. Usar cubiertas o técnicas de manejo contra heladas si la temperatura baja significativamente.
# - **Seguimiento de plagas y enfermedades**: Durante la fase de siembra, las plagas de suelo son una amenaza potencial. Implementar protocolos de monitoreo y, si se observan presencias significativas, iniciar tratamientos con insecticidas selectivos.

# Estas recomendaciones buscan maximizar la eficiencia en el uso de recursos y optimizar 
# el rendimiento del cultivo en la etapa inicial. Es crucial mantener un monitoreo constante de las variables agrícolas y adaptar el manejo según la evolución de las condiciones del campo y el clima.



# ==================================================
# RECOMENDACIONES PARA ZONA Sur
# ==================================================
# Para optimizar la gestión del cultivo en la zona Sur y basándonos en los datos proporcionados, aquí tienes un conjunto de recomendaciones específicas y técnicas:

# ### 1. Programa de Riego Optimizado:
# Dado que la humedad del suelo es del 37.9% y estás en la etapa de siembra, es crucial asegurar que el nivel de humedad sea constante y adecuado para la germinación. Considera lo siguiente:

# - **Frecuencia de Riego**: Inicialmente, realiza riegos ligeros pero frecuentes, asegurando que el primer centímetro de suelo no se seque. Esto podría ser alrededor de 2-3 veces por semana, dependiendo de la evaporación local y precipitaciones.
# - **Volumen de Riego**: Aplicar aproximadamente 10-15 mm por riego. Ajusta este volumen si las condiciones climáticas cambian o el suelo muestra diferente retención.
# - **Monitoreo**: Utiliza sensores de humedad del suelo para ajustar el programa en tiempo real, incrementando la frecuencia si la humedad cae por debajo del 30%.

# ### 2. Plan de Fertilización Específico:
# En la etapa de siembra, es esencial aportar la nutrición necesaria para un buen establecimiento del cultivo.

# - **Nitrógeno**: Con 57 ppm, el nivel es adecuado para el inicio pero planea una aplicación ligera. Añadir 20 kg/ha de Nitrógeno en forma de urea (46:0:0), incorporada ligeramente al suelo para evitar las pérdidas por volatilización.

# - **Fósforo**: Con 32 ppm está en un rango razonable, pero dado su importancia en el desarrollo radicular temprano, aplicar 40 kg/ha de superfosfato (0:20:0) al momento de la siembra.

# - **Potasio**: Con 45 ppm, se encuentra en un nivel aceptable, pero considerando que es esencial para el crecimiento, puedes aplicar 30 kg/ha de sulfato de potasio (0:0:50) si los análisis futuros indican disminución.

# ### 3. Ajustes de pH si Son Necesarios:
# El pH de 6.5 es óptimo para la mayoría de cultivos, permitiendo la disponibilidad adecuada de nutrientes. No se requieren ajustes inmediatos. Sin embargo, es bueno monitorear cada temporada.

# ### 4. Cronograma de Actividades Según la Etapa del Cultivo:
# Considerando que estás en la etapa de siembra, estas actividades son fundamentales:    

# - **Preparación del Suelo**: Termina la labranza antes de la siembra para mejorar la aireación y estructura del suelo.
# - **Siembra Directa**: Realiza la siembra cuando las condiciones de humedad y temperatura son óptimas.
# - **Control de Malezas**: Inicia un plan de control de malezas pre-emergente utilizando herbicidas selectivos.
# - **Monitoreo de Plagas y Enfermedades**: Inicia monitoreos semanales para identificar 
# cualquier problema tempranamente.

# ### 5. Alertas o Precauciones Especiales:
# - **Escasez de Aguas**: Monitorea las precipitaciones y ajusta riegos en temporadas secas.
# - **Prevención de Enfermedades**: Dado el microclima, utiliza semillas tratadas con fungicidas para prevenir enfermedades comunes.
# - **Erosión**: En caso de pendientes, utilizar técnicas de cultivo en contorno para prevenir erosión.

# Siguiendo estas recomendaciones, se optimizará el rendimiento del cultivo en esta etapa crítica. Es vital mantener un monitoreo constante y ajustar las prácticas basadas en cambios climáticos o de otros factores no controlables.



# ==================================================
# RECOMENDACIONES PARA ZONA Este
# ==================================================
# Para optimizar el manejo del cultivo en la zona Este, he analizado los datos de sensores de agricultura de precisión proporcionados. A continuación, te presento recomendaciones técnicas específicas para cada aspecto solicitado:

# ### 1. Programa de riego optimizado
# - **Humedad del suelo actual**: 27.3%
# - **Recomendación**: Durante la etapa de floración, es crucial mantener un nivel de humedad adecuado para asegurar una buena formación de flores. Para la mayoría de los cultivos en floración, el contenido de humedad ideal oscila entre el 30% y el 60%. Dado que 
# estás bajo el 30%, te sugiero:
#   - Incrementar la frecuencia de riego y ajustar el volumen para elevar la humedad del 
# suelo a un rango más óptimo.
#   - Aplicar riego moderado de aproximadamente 20 mm por sesión, dos veces por semana, monitoreando el porcentaje de humedad para evitar anegamiento.

# ### 2. Plan de fertilización específico
# Los niveles actuales de nutrientes son:
# - **Nitrógeno: 65 ppm**
# - **Fósforo: 35 ppm**
# - **Potasio: 72 ppm**

# Recomendaciones para las condiciones actuales:
# - **Nitrógeno**: Durante la floración, se recomienda un nivel más alto de nitrógeno para la mayoría de los cultivos. Aplicar un fertilizante nitrogenado, como urea, a razón de 30 kg/ha para elevar los niveles de nitrógeno.
# - **Fósforo y potasio**: Los niveles actuales están en un rango bajo-moderado. Se recomienda una aplicación de un fertilizante balanceado, como 10-30-20, a razón de 50 kg/ha, para asegurar una nutrición adecuada durante la floración.

# ### 3. Ajustes de pH
# - **pH actual**: 6.2
# - **Recomendación**: El pH del suelo está en un nivel ligeramente ácido, que es aceptable para la mayoría de los cultivos. No se requiere un ajuste significativo, pero para optimizar la absorción de nutrientes:
#   - Puedes considerar una ligera enmienda con cal a razón de 50 kg/ha si el cultivo lo 
# permite, para ajustar el pH hacia 6.5, optimizando así la disponibilidad de nutrientes.
# ### 4. Cronograma de actividades según la etapa del cultivo
# Durante la floración, las actividades deben enfocarse en:
# - **Semana 1-2**:
#   - Aplicación de fertilizantes nitrogenados y fosfatados.
#   - Monitoreo diario de la humedad del suelo.
# - **Semana 3**:
#   - Revisar el estado de las flores para detectar problemas de polinización.
#   - Aplicación de riego según necesidad basada en nuevas mediciones de humedad.        
# - **Semana 4-5**:
#   - Revisión de plagas y enfermedades, aplicando control biológico o químico si es necesario.
#   - Evaluar el desarrollo floral y ajustar el riego y fertilización conforme cambien las necesidades.

# ### 5. Alertas o precauciones especiales
# - **Temperatura**: A 21.7°C, estás en un rango favorable, pero mantenerse alerta ante cambios bruscos es clave.
# - **Riesgo de plagas o enfermedades**: Durante la floración, el riesgo de plagas como pulgón y enfermedades como el mildiu es alto. Monitorea los cultivos y aplica preventivos adecuados si es necesario.
# - **Calibración de sensores**: Asegúrate de que los sensores de humedad y nutrientes están calibrados correctamente para obtener lecturas precisas.

# Estas recomendaciones deberían ayudarte a maximizar el potencial del ciclo de cultivo actual, asegurando que las condiciones sean óptimas para el desarrollo floral y la futura fructificación.



# ==================================================
# RECOMENDACIONES PARA ZONA Oeste
# ==================================================
# Para proporcionar recomendaciones específicas y técnicas basadas en los datos de sensores proporcionados, es importante considerar las necesidades típicas de cultivos comunes durante la etapa de siembra. Sin embargo, estos datos deben personalizarse aún más según el tipo específico de cultivo. A continuación, se presentan recomendaciones generales para la zona Oeste con las condiciones de suelo y clima indicadas.

# ### 1. Programa de Riego Optimizado

# La humedad actual del suelo es del 30.8%. Dado que estás en la etapa de siembra, es crucial mantener una humedad adecuada para asegurar una buena germinación. La humedad óptima para la mayoría de los cultivos durante la germinación es del 60-70%. Sugiero un sistema de riego por goteo para proporcionar el agua de manera precisa y eficiente.       

# - **Frecuencia de Riego**: Diariamente, en las primeras horas de la mañana.
# - **Volumen de Agua**: Aproximadamente 10 mm por riego (aproximadamente 10 litros por metro cuadrado), ajustando según la tasa de infiltración y la capacidad de retención hídrica del suelo.

# ### 2. Plan de Fertilización Específico

# Los niveles de nutrientes indicados sugieren que está presente una deficiencia de nitrógeno, que suele ser esencial en las primeras etapas del crecimiento del cultivo.       

# - **Nitrógeno**: Aplica un fertilizante nitrogenado, como urea (46% N). Objetivo de incremento necesidad = 60 ppm.
#   - **Cantidad**: Aproximadamente 1.2 kg de urea (46% N) por 1 tonelada de suelo para incrementar el nivel de nitrógeno en 23 ppm.
# - **Fósforo**: Dado un nivel moderado, su aplicación puede ser reducida.
#   - **Fertilizante recomendado**: Fosfato diamónico (DAP - 18-46-0).
#   - **Cantidad**: Aplica alrededor de 0.54 kg de DAP por tonelada de suelo (teniendo en cuenta la eficiencia de absorción del fósforo en suelo).
# - **Potasio**: Los niveles son aceptables. Considera un suplemento moderado.
#   - **Fertilizante recomendado**: Sulfato de potasio (50% K2O).
#   - **Cantidad**: Aplica 0.4 kg por tonelada para mantener niveles adecuados.

# ### 3. Ajustes de pH si son necesarios

# El pH del suelo es de 6.7, que es adecuado para la mayoría de los cultivos. No se requieren ajustes significativos al pH. Monitorea regularmente para asegurarte de que no caiga por debajo de 6.5.

# ### 4. Cronograma de Actividades Según la Etapa del Cultivo

# Al estar en la etapa de siembra, las siguientes actividades deben considerarse:        

# - **Día 0-10**: Siembra y riego inmediatamente después de sembrar para asegurar la humedad adecuada.
# - **Día 10-20**: Aplicar fertilizantes según lo especificado arriba. Monitorear la aparición de plántulas.
# - **Día 20-30**: Revisión de cualquier síntoma de deficiencia nutricional o estrés hídrico.

# ### 5. Alertas o Precauciones Especiales

# - **Monitoreo de plagas y enfermedades**: Las condiciones de humedad pueden favorecer ciertos hongos y plagas. Implementa un sistema de monitoreo con trampas o inspecciones visuales.
# - **Riesgo de compactación del suelo**: Evita actividades pesadas sobre el suelo húmedo, ya que podría causar compactación, afectando el crecimiento radicular.
# - **Condiciones climáticas**: Mantente informado sobre cambios climáticos repentinos que puedan influir en la germinación y el establecimiento inicial del cultivo.

# Estas recomendaciones deben afinarse con análisis en campo y según el tipo de cultivo. 
# Además, considera consultas con un especialista local para ajustes conforme a variedades específicas de plantas cultivadas en la zona.



"""## Capítulo 3: Optimización de la Productividad del Suelo

   ## Sistema de Recomendación Inteligente de Fertilizantes"""


"""Datos de análisis de suelo para diferentes parcelas"""

# parcelas_suelo = {
#     "Parcela_A": {
#         "area_ha": 25.5,
#         "soil_data": {
#             "pH": 5.8,
#             "organic_matter": 3.2,  # porcentaje
#             "nutrient_content": {
#                 "nitrogen": 40,  # ppm
#                 "phosphorus": 25,  # ppm
#                 "potassium": 35   # ppm
#             },
#             "soil_type": "franco-arcilloso",
#             "drainage": "moderado"
#         },
#         "crop_type": "maíz"
#     },
#     "Parcela_B": {
#         "area_ha": 18.3,
#         "soil_data": {
#             "pH": 7.2,
#             "organic_matter": 2.8,
#             "nutrient_content": {
#                 "nitrogen": 55,
#                 "phosphorus": 15,
#                 "potassium": 28
#             },
#             "soil_type": "franco-arenoso",
#             "drainage": "bueno"
#         },
#         "crop_type": "soja"
#     },
#     "Parcela_C": {
#         "area_ha": 32.1,
#         "soil_data": {
#             "pH": 6.1,
#             "organic_matter": 4.1,
#             "nutrient_content": {
#                 "nitrogen": 35,
#                 "phosphorus": 45,
#                 "potassium": 52
#             },
#             "soil_type": "franco",
#             "drainage": "excelente"
#         },
#         "crop_type": "trigo"
#     }
# }

# print("Parcelas registradas en el sistema:")
# for parcela, datos in parcelas_suelo.items():
#     print(f"- {parcela}: {datos['area_ha']} ha, Cultivo: {datos['crop_type']}")

""" Resultado """

# Estas recomendaciones deben ser ajustadas en función de más datos específicos sobre el 
# cultivo en particular y el historial del suelo. El monitoreo rutinario y los ajustes en tiempo real mejorarán el manejo agrícola y optimizarán la producción.


# Parcelas registradas en el sistema:
# - Parcela_A: 25.5 ha, Cultivo: maíz
# - Parcela_B: 18.3 ha, Cultivo: soja
# - Parcela_C: 32.1 ha, Cultivo: trigo

"""Función para generar recomendaciones de fertilización específicas"""

# def generar_plan_fertilizacion(parcela_id, datos_parcela):
#     soil_data = datos_parcela['soil_data']
#     area = datos_parcela['area_ha']
#     cultivo = datos_parcela['crop_type']
    
#     soil_description = f"""Análisis de suelo para {parcela_id}:
#     - Área: {area} hectáreas
#     - Cultivo: {cultivo}
#     - pH del suelo: {soil_data['pH']}
#     - Materia orgánica: {soil_data['organic_matter']}%
#     - Tipo de suelo: {soil_data['soil_type']}
#     - Drenaje: {soil_data['drainage']}
#     - Nivel de nitrógeno: {soil_data['nutrient_content']['nitrogen']} ppm
#     - Nivel de fósforo: {soil_data['nutrient_content']['phosphorus']} ppm
#     - Nivel de potasio: {soil_data['nutrient_content']['potassium']} ppm"""
    
#     prompt = f"""Como experto en fertilidad del suelo, basado en los siguientes datos, 
#     diseña un plan de fertilización técnico y específico que incluya:
    
#     1. Análisis detallado de las condiciones actuales del suelo
#     2. Recomendaciones específicas de fertilizantes (tipos y cantidades por hectárea)
#     3. Cronograma de aplicación (fechas y métodos)
#     4. Correcciones de pH si son necesarias
#     5. Estimación de costos por hectárea
#     6. Rendimiento esperado con el plan propuesto
#     7. Monitoreo y seguimiento recomendado
    
#     {soil_description}
    
#     Proporciona cantidades exactas y recomendaciones técnicas precisas."""
    
#     return obtener_analisis_agricola(prompt)

# # Generar planes para todas las parcelas
# planes_fertilizacion = {}
# for parcela_id, datos in parcelas_suelo.items():
#     plan = generar_plan_fertilizacion(parcela_id, datos)
#     planes_fertilizacion[parcela_id] = plan
    
#     print(f"\n{'='*60}")
#     print(f"PLAN DE FERTILIZACIÓN - {parcela_id}")
#     print(f"{'='*60}")
#     print(plan)
#     print("\n")

""" Resultado """

# ============================================================
# PLAN DE FERTILIZACIÓN - Parcela_A
# ============================================================
# Diseñar un plan de fertilización específico para la Parcela_A requerirá una evaluación 
# exhaustiva de los datos proporcionados. A continuación, se presenta un plan detallado: 

# ### 1. Análisis detallado de las condiciones actuales del suelo
# - **pH del suelo**: A 5.8, el pH es ligeramente ácido, lo cual puede afectar la disponibilidad de algunos nutrientes para el maíz.
# - **Materia orgánica**: Con un 3.2%, está en un rango aceptable, proporcionando buena estructura del suelo y capacidad de retención de nutrientes.
# - **Tipo de suelo**: Franco-arcilloso, que ofrece buena retención de agua y nutrientes, pero necesita cuidado en cuanto a compactación y drenaje.
# - **Drenaje**: Moderado, lo cual es aceptable para el maíz, pero se necesita monitoreo 
# para evitar encharcamiento.
# - **Nutrientes**:
#   - **Nitrógeno**: 40 ppm es bajo para maíz, que típicamente necesita más nitrógeno.   
#   - **Fósforo**: 25 ppm muestra una deficiencia para maíz, que tiene una alta demanda de fósforo para un desarrollo radicular efectivo.
#   - **Potasio**: 35 ppm es bajo, se recomienda un valor mayor para optimizar el rendimiento del maíz.

# ### 2. Recomendaciones específicas de fertilizantes (tipos y cantidades por hectárea)  
# - **Nitrógeno (N)**:
#   - Aplicar urea (46-0-0) a una tasa de 150 kg/ha para corregir la deficiencia de nitrógeno. Se recomiendan dos aplicaciones divididas.
# - **Fósforo (P)**:
#   - Aplicar fosfato diamónico (DAP, 18-46-0) a una tasa de 100 kg/ha. Esto proporcionará fósforo adicional necesario.
# - **Potasio (K)**:
#   - Aplicar cloruro de potasio (KCl, 0-0-60) a una tasa de 100 kg/ha.

# ### 3. Cronograma de aplicación (fechas y métodos)
# - **Antes de la siembra** (1-2 semanas antes):
#   - Labrar profundamente e incorporar el DAP para el ajuste de fósforo.
# - **Durante la siembra**:
#   - Incorporar parte de la urea (100 kg/ha) en banda junto con la semilla.
# - **Post-emergencia** (20-30 días después de la siembra):
#   - Realizar la segunda aplicación de urea (50 kg/ha) junto con el cloruro de potasio. 
#   - Aplicaciones en cobertura con araje superficial para evitar pérdida por volatilización.

# ### 4. Correcciones de pH si son necesarias
# - **Incrementar pH**:
#   - Aplicar cal agrícola (carbonato de calcio) a una dosis de 1 tonelada/ha. Realizar esta práctica al menos 3 meses antes de la siembra para mejorar la absorción de nutrientes.

# ### 5. Estimación de costos por hectárea
# - **Urea**: 150 kg * $0.50/kg = $75
# - **DAP**: 100 kg * $0.70/kg = $70
# - **KCl**: 100 kg * $0.40/kg = $40
# - **Cal agrícola**: 1 tonelada * $30/tonelada = $30
# - **Costos adicionales (mano de obra, maquinaria, etc.)**: Aproximadamente $100        
# - **Total estimado por hectárea**: $315

# ### 6. Rendimiento esperado con el plan propuesto
# - Con prácticas óptimas de manejo, el rendimiento esperado podría aumentar a 8-10 toneladas por hectárea, asumiendo condiciones climáticas favorables y una gestión eficaz del cultivo.

# ### 7. Monitoreo y seguimiento recomendado
# - **Monitoreo semanal de plagas** y enfermedades.
# - **Análisis de suelo anual** para ajustar las recomendaciones de fertilización futuras.
# - **Observación post-aplicaciones** de fertilizantes para evaluar eficiencias y cualquier síntoma de deficiencia.
# - **Uso de tecnologías de agricultura de precisión** como imágenes satelitales o drones para evaluar la uniformidad del crecimiento y estado del cultivo.

# Con estos pasos y un monitoreo continuo, el plan de fertilización puede aumentar significativamente el rendimiento del maíz en la Parcela_A.



# ============================================================
# PLAN DE FERTILIZACIÓN - Parcela_B
# ============================================================
# Para diseñar un plan de fertilización preciso y técnico para la Parcela_B, se debe tener en cuenta tanto el análisis del suelo como las necesidades específicas del cultivo de soja. Aquí está el plan detallado:

# ### 1. Análisis detallado de las condiciones actuales del suelo

# - **pH del suelo**: 7.2 (ligeramente alcalino, pero no representa un problema serio para la soja).
# - **Materia orgánica**: 2.8% (moderado, puede mejorarse para retener más nutrientes y agua).
# - **Tipo de suelo**: franco-arenoso (buen drenaje, pero puede necesitar prácticas para 
# mejorar la retención de nutrientes).
# - **Niveles de nutrientes**:
#   - **Nitrógeno (N)**: 55 ppm (moderadamente bajo, se requiere suplementación).        
#   - **Fósforo (P)**: 15 ppm (bajo, se requiere corrección).
#   - **Potasio (K)**: 28 ppm (bajo, se requiere suplementación).

# ### 2. Recomendaciones específicas de fertilizantes

# #### Nitrógeno (N)

# - Se recomienda una aplicación de 120 kg/ha de nitrógeno total durante el ciclo de cultivo. Esto puede lograrse con:
#   - **Urea** (46% N): 260 kg/ha.

# #### Fósforo (P)

# - Se recomienda aplicar 60 kg/ha de fósforo para elevar los niveles en el suelo. Utilizar:
#   - **Superfosfato triple (TSP)** (46% P2O5): 130 kg/ha.

# #### Potasio (K)

# - Se recomienda aplicar 80 kg/ha de potasio. Usar:
#   - **Cloruro de potasio (KCl)** (60% K2O): 130 kg/ha.

# ### 3. Cronograma de aplicación

# - **Antes de la siembra**:
#   - Aplicar todo el fósforo y potasio recomendados al momento de la preparación del suelo.

# - **Post-emergencia**:
#   - Fraccionar el nitrógeno en dos aplicaciones. Aplicar 50% al inicio del desarrollo vegetativo y el otro 50% en el inicio de floración.

# ### 4. Correcciones de pH

# - El pH de 7.2 es adecuado y no requiere corrección en este caso. El enfoque debe centrarse en mantener este pH estable.

# ### 5. Estimación de costos por hectárea

# - **Urea**: 260 kg/ha a $0.50/kg = $130/ha
# - **Superfosfato triple**: 130 kg/ha a $0.70/kg = $91/ha
# - **Cloruro de potasio**: 130 kg/ha a $0.45/kg = $58.5/ha

# Total estimado de fertilización: $279.5/ha

# ### 6. Rendimiento esperado con el plan propuesto

# Con la fertilización adecuada, se puede esperar un rendimiento de soja entre 3.5 y 4.0 
# toneladas/ha, dependiendo de las condiciones climáticas y prácticas de manejo agronómico.

# ### 7. Monitoreo y seguimiento recomendado

# - **Monitoreo del desarrollo del cultivo**: Realizar un seguimiento del crecimiento de 
# la soja cada 2-3 semanas para ajustar la aplicación de fertilizantes si es necesario.  
# - **Pruebas del suelo posteriores**: Realizar una nueva prueba de suelo después de la cosecha para evaluar el efecto de las prácticas de fertilización y planificar para el siguiente ciclo.
# - **Control de plagas y enfermedades**: Mantener un programa de protección fitosanitaria para prevenir problemas que puedan influir en la efectividad de la fertilización.    

# Este plan está diseñado para optimizar la fertilidad del suelo de la Parcela_B y maximizar el rendimiento del cultivo de soja, siempre considerando las condiciones actuales del suelo y las necesidades del cultivo.



# ============================================================
# PLAN DE FERTILIZACIÓN - Parcela_C
# ============================================================
# Para diseñar un plan de fertilización adecuado para la Parcela_C de 32.1 hectáreas cultivadas con trigo, se debe realizar un análisis exhaustivo de los datos del suelo proporcionados. A continuación, se presenta un plan técnico y específico:

# ### 1. Análisis detallado de las condiciones actuales del suelo

# - **pH del Suelo:** 6.1, ligeramente ácido, generalmente adecuado para el cultivo de trigo.
# - **Materia Orgánica:** 4.1%, un buen nivel que favorecerá la retención de nutrientes y agua.
# - **Tipo de Suelo:** Franco, ofreciendo un equilibrio óptimo entre retención de agua y 
# drenaje.
# - **Drenaje:** Excelente, lo cual es beneficioso para evitar saturación y asfixia de las raíces.
# - **Nutrientes:**
#   - **Nitrógeno (N):** 35 ppm. Esto es relativamente bajo para las necesidades de trigo.
#   - **Fósforo (P):** 45 ppm. Un nivel razonable, pero puede ser mejorado para maximizar el rendimiento.
#   - **Potasio (K):** 52 ppm. Nivel moderado, podría optimizarse.

# ### 2. Recomendaciones específicas de fertilizantes

# - **Nitrógeno (N):** Se recomienda aplicar 150 kg de nitrógeno por hectárea. Utilizar urea (46-0-0) como fuente principal.
# - **Fósforo (P):** Añadir 50 kg de P2O5 por hectárea. Puede usarse superfosfato triple 
# (0-46-0).
# - **Potasio (K):** Aplicar 50 kg de K2O por hectárea. Utilizar cloruro de potasio (0-0-60).

# ### 3. Cronograma de aplicación

# - **Primer Aplicación (Pre-siembra):**
#   - **Fecha:** 2-4 semanas antes de la siembra.
#   - **Método:** Incorporar el fósforo (superfosfato triple) durante el laboreo del suelo.

# - **Segundo Aplicación (A los 30-40 días post-siembra):**
#   - **Fecha:** Momento de macollamiento.
#   - **Método:** Aplicar la mitad del nitrógeno (urea) en cobertera.

# - **Tercera Aplicación (Al inicio del encañado):**
#   - **Fecha:** Aproximadamente 60-70 días post-siembra.
#   - **Método:** Aplicar la otra mitad del nitrógeno (urea) y el total del potasio (cloruro de potasio).

# ### 4. Correcciones de pH

# - El pH de 6.1 es adecuado para el trigo; no se requieren modificaciones importantes. Si se busca optimizar ligeramente, podrían agregarse 500 kg de cal agrícola por hectárea para elevar el pH a niveles más óptimos (6.5).

# ### 5. Estimación de costos por hectárea

# - **Urea (46-0-0):** Aproximadamente $0.64/kg. $\Rightarrow$ $192 por ha.
# - **Superfosfato triple (0-46-0):** Aproximadamente $0.72/kg. $\Rightarrow$ $36 por ha.- **Cloruro de potasio (0-0-60):** Aproximadamente $0.50/kg. $\Rightarrow$ $25 por ha. 
# - **Cal agrícola:** Aproximadamente $0.08/kg. $\Rightarrow$ $40 por ha (opcional).     

# - **Costo total estimado:** $293 por ha sin cal/$333 por ha con cal.

# ### 6. Rendimiento esperado con el plan propuesto

# Con una fertilización adecuada, se espera incrementar el rendimiento a aproximadamente 
# 6-7 toneladas por hectárea, dependiendo de las condiciones climáticas.

# ### 7. Monitoreo y seguimiento recomendado

# - **Muestreo de Suelo:** Realizar análisis de suelo anualmente para ajustar futuros planes de fertilización.
# - **Seguimiento de Nutrientes:** Monitorizar los niveles de nitrógeno, fósforo y potasio mediante análisis de tejidos durante el periodo de crecimiento.
# - **Inspección del Cultivo:** Revisar periódicamente las condiciones del cultivo para detectar signos de deficiencias nutricionales o estrés.

# Implementar este plan proporcionará a la Parcela_C una base sólida para mejorar la productividad y asegurar una gestión sostenible del suelo.



"""## Capítulo 4: Gestión Inteligente de Mano de Obra Agrícola

   ## Sistema de Programación Dinámica de Tareas"""


# # Simulación de datos ambientales y operacionales en tiempo real
# def obtener_datos_ambientales():
#     return {
#         "weather_forecast": {
#             "hoy": {
#                 "fecha": datetime.now().strftime("%Y-%m-%d"),
#                 "temp_max": np.random.normal(28, 3),
#                 "temp_min": np.random.normal(18, 2),
#                 "precipitation": np.random.exponential(5),
#                 "wind_speed": np.random.normal(10, 3),
#                 "humidity": np.random.normal(65, 10)
#             },
#             "pronostico_3_dias": [
#                 {
#                     "fecha": (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d"),
#                     "temp_max": np.random.normal(27, 4),
#                     "precipitation": np.random.exponential(8),
#                     "wind_speed": np.random.normal(12, 4)
#                 } for i in range(1, 4)
#             ]
#         },
#         "soil_conditions": {
#             "moisture_level": np.random.normal(45, 8),
#             "temperature": np.random.normal(22, 2),
#             "fertility_level": np.random.choice(["bajo", "medio", "alto"], p=[0.2, 0.5, 0.3])
#         },
#         "operational_data": {
#             "workers_available": np.random.randint(8, 15),
#             "machinery_status": {
#                 "tractor_1": np.random.choice(["disponible", "mantenimiento"], p=[0.8, 0.2]),
#                 "cosechadora": np.random.choice(["disponible", "ocupada"], p=[0.7, 0.3]),
#                 "pulverizadora": "disponible"
#             },
#             "fuel_level": np.random.uniform(0.3, 1.0)
#         }
#     }

# # Obtener datos actuales
# datos_operacionales = obtener_datos_ambientales()

# print("=== DATOS OPERACIONALES ACTUALES ===")
# print(f"Fecha: {datos_operacionales['weather_forecast']['hoy']['fecha']}")
# print(f"Temperatura: {datos_operacionales['weather_forecast']['hoy']['temp_max']:.1f}°C")
# print(f"Precipitación: {datos_operacionales['weather_forecast']['hoy']['precipitation']:.1f}mm")
# print(f"Humedad del suelo: {datos_operacionales['soil_conditions']['moisture_level']:.1f}%")
# print(f"Trabajadores disponibles: {datos_operacionales['operational_data']['workers_available']}")
# print(f"Estado de maquinaria: {datos_operacionales['operational_data']['machinery_status']}")
# print(f"Nivel de combustible: {datos_operacionales['operational_data']['fuel_level']:.0%}")


""" Resultado """

# # Simulación de datos ambientales y operacionales en tiempo real
# def obtener_datos_ambientales():
#     return {
#         "weather_forecast": {
#             "hoy": {
#                 "fecha": datetime.now().strftime("%Y-%m-%d"),
#                 "temp_max": np.random.normal(28, 3),
#                 "temp_min": np.random.normal(18, 2),
#                 "precipitation": np.random.exponential(5),
#                 "wind_speed": np.random.normal(10, 3),
#                 "humidity": np.random.normal(65, 10)
#             },
#             "pronostico_3_dias": [
#                 {
#                     "fecha": (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d"),
#                     "temp_max": np.random.normal(27, 4),
#                     "precipitation": np.random.exponential(8),
#                     "wind_speed": np.random.normal(12, 4)
#                 } for i in range(1, 4)
#             ]
#         },
#         "soil_conditions": {
#             "moisture_level": np.random.normal(45, 8),
#             "temperature": np.random.normal(22, 2),
#             "fertility_level": np.random.choice(["bajo", "medio", "alto"], p=[0.2, 0.5, 0.3])
#         },
#         "operational_data": {
#             "workers_available": np.random.randint(8, 15),
#             "machinery_status": {
#                 "tractor_1": np.random.choice(["disponible", "mantenimiento"], p=[0.8, 0.2]),
#                 "cosechadora": np.random.choice(["disponible", "ocupada"], p=[0.7, 0.3]),
#                 "pulverizadora": "disponible"
#             },
#             "fuel_level": np.random.uniform(0.3, 1.0)
#         }
#     }

# # Obtener datos actuales
# datos_operacionales = obtener_datos_ambientales()

# print("=== DATOS OPERACIONALES ACTUALES ===")
# print(f"Fecha: {datos_operacionales['weather_forecast']['hoy']['fecha']}")
# print(f"Temperatura: {datos_operacionales['weather_forecast']['hoy']['temp_max']:.1f}°C")
# print(f"Precipitación: {datos_operacionales['weather_forecast']['hoy']['precipitation']:.1f}mm")
# print(f"Humedad del suelo: {datos_operacionales['soil_conditions']['moisture_level']:.1f}%")
# print(f"Trabajadores disponibles: {datos_operacionales['operational_data']['workers_available']}")
# print(f"Estado de maquinaria: {datos_operacionales['operational_data']['machinery_status']}")
# print(f"Nivel de combustible: {datos_operacionales['operational_data']['fuel_level']:.0%}")

"""Generar programación dinámica de tareas""" # este me genero error

# def generar_programa_trabajo(datos):
#     # Preparar descripción de datos para el LLM
#     weather_today = datos['weather_forecast']['hoy']
#     soil = datos['soil_conditions']
#     operational = datos['operational_data']
    
#     environment_description = f"""CONDICIONES OPERACIONALES ACTUALES:
    
#     CLIMA HOY ({weather_today['fecha']}):
#     - Temperatura máxima: {weather_today['temp_max']:.1f}°C
#     - Temperatura mínima: {weather_today['temp_min']:.1f}°C
#     - Precipitación pronosticada: {weather_today['precipitation']:.1f}mm
#     - Velocidad del viento: {weather_today['wind_speed']:.1f} km/h
#     - Humedad relativa: {weather_today['humidity']:.1f}%
    
#     CONDICIONES DEL SUELO:
#     - Humedad del suelo: {soil['moisture_level']:.1f}%
#     - Temperatura del suelo: {soil['temperature']:.1f}°C
#     - Nivel de fertilidad: {soil['fertility_level']}
    
#     RECURSOS DISPONIBLES:
#     - Trabajadores disponibles: {operational['workers_available']} personas
#     - Estado de maquinaria: {operational['machinery_status']}
#     - Nivel de combustible: {operational['fuel_level']:.0%}
    
#     PRONÓSTICO PRÓXIMOS 3 DÍAS:"""
    
#     for i, forecast in enumerate(datos['weather_forecast']['pronostico_3_dias']):
#         environment_description += f"\n    Día {i+1} ({forecast['fecha']}): {forecast['temp_max']:.1f}°C, {forecast['precipitation']:.1f}mm lluvia"
    
#     prompt = f"""{environment_description}
    
#     Como experto en gestión agrícola con IA, genera un programa de trabajo dinámico y optimizado que incluya:
    
#     1. PRIORIZACIÓN DE TAREAS para hoy basada en condiciones actuales
#     2. ASIGNACIÓN DE PERSONAL específica por tarea
#     3. CRONOGRAMA DETALLADO (horarios específicos)
#     4. USO OPTIMIZADO DE MAQUINARIA disponible
#     5. CONTINGENCIAS por cambios climáticos
#     6. PLANIFICACIÓN PRÓXIMOS 3 DÍAS
#     7. ALERTAS Y RECOMENDACIONES ESPECIALES
    
#     Considera actividades como: siembra, riego, aplicación de fertilizantes, control de malezas, 
#     cosecha, mantenimiento de equipos, y otras tareas agrícolas relevantes.
    
#     Proporciona un plan específico, técnico y actionable."""
    
#     return obtener_analisis_agricola(prompt)

# # Generar programa de trabajo
# programa_trabajo = generar_programa_trabajo(datos_operacionales)
# print("\n" + "="*70)
# print("PROGRAMA DE TRABAJO DINÁMICO - GESTIÓN IA")
# print("="*70)
# print(programa_trabajo)




"""## Capítulo 5: Sistema de Riego Inteligente en Tiempo Real

   ## Optimización de Recursos Hídricos con IA"""



"""Simulación de sistema de sensores de riego IoT"""
# class SistemaRiegoInteligente:
#     def __init__(self, zonas):
#         self.zonas = zonas
#         self.datos_historicos = self.generar_datos_historicos()
        
#     def generar_datos_historicos(self):
#         # Simular 30 días de datos históricos
#         fechas = [(datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(30, 0, -1)]
#         return {
#             'fechas': fechas,
#             'humedad_promedio': np.random.normal(40, 10, 30),
#             'evapotranspiracion': np.random.normal(5.2, 1.5, 30),
#             'precipitacion': np.random.exponential(3, 30)
#         }
    
#     def obtener_datos_tiempo_real(self):
#         return {
#             zona: {
#                 "moisture_level": np.random.normal(35, 12),
#                 "root_zone_temperature": np.random.normal(24, 3),
#                 "soil_conductivity": np.random.normal(0.8, 0.3),
#                 "potential_root_disease_risk": np.random.choice(["bajo", "moderado", "alto"], p=[0.6, 0.3, 0.1]),
#                 "growth_stage": np.random.choice(["vegetativa", "floración", "fructificación", "maduración"]),
#                 "water_requirement": np.random.choice(["bajo", "medio", "alto"], p=[0.2, 0.5, 0.3]),
#                 "last_irrigation": np.random.randint(1, 5)  # días desde último riego
#             } for zona in self.zonas
#         }

# # Inicializar sistema para 4 zonas de cultivo
# zonas_cultivo = ["Zona_Norte", "Zona_Sur", "Zona_Este", "Zona_Oeste"]
# sistema_riego = SistemaRiegoInteligente(zonas_cultivo)

# # Obtener datos en tiempo real
# datos_riego = sistema_riego.obtener_datos_tiempo_real()

# print("=== ESTADO ACTUAL DEL SISTEMA DE RIEGO ===")
# for zona, datos in datos_riego.items():
#     print(f"\n{zona}:")
#     print(f"  Humedad del suelo: {datos['moisture_level']:.1f}%")
#     print(f"  Temperatura zona radicular: {datos['root_zone_temperature']:.1f}°C")
#     print(f"  Riesgo enfermedad radicular: {datos['potential_root_disease_risk']}")
#     print(f"  Etapa de crecimiento: {datos['growth_stage']}")
#     print(f"  Requerimiento hídrico: {datos['water_requirement']}")
#     print(f"  Días desde último riego: {datos['last_irrigation']}")

""" Resultado """

#   Riesgo enfermedad radicular: bajo
#   Etapa de crecimiento: floración
#   Requerimiento hídrico: alto
#   Días desde último riego: 2

# Zona_Este:
#   Humedad del suelo: 18.5%
#   Temperatura zona radicular: 19.9°C
#   Riesgo enfermedad radicular: bajo
#   Etapa de crecimiento: maduración
#   Requerimiento hídrico: bajo
#   Días desde último riego: 4

# Zona_Oeste:
#   Humedad del suelo: 30.2%
#   Temperatura zona radicular: 19.9°C
#   Riesgo enfermedad radicular: bajo
#   Etapa de crecimiento: maduración
#   Requerimiento hídrico: medio
#   Días desde último riego: 4


"""Generar programa de riego optimizado por zona"""

# def optimizar_programa_riego(zona_id, datos_zona, datos_clima):
#     # Combinar datos de la zona con pronóstico climático
#     data_description = f"""ANÁLISIS DE RIEGO - {zona_id}:
    
#     CONDICIONES ACTUALES DEL SUELO:
#     - Humedad del suelo: {datos_zona['moisture_level']:.1f}%
#     - Temperatura zona radicular: {datos_zona['root_zone_temperature']:.1f}°C
#     - Conductividad del suelo: {datos_zona['soil_conductivity']:.2f} dS/m
#     - Riesgo enfermedad radicular: {datos_zona['potential_root_disease_risk']}
#     - Días desde último riego: {datos_zona['last_irrigation']}
    
#     ESTADO DEL CULTIVO:
#     - Etapa de crecimiento: {datos_zona['growth_stage']}
#     - Requerimiento hídrico: {datos_zona['water_requirement']}
    
#     CONDICIONES CLIMÁTICAS:
#     - Temperatura actual: {datos_clima['weather_forecast']['hoy']['temp_max']:.1f}°C
#     - Precipitación esperada hoy: {datos_clima['weather_forecast']['hoy']['precipitation']:.1f}mm
#     - Humedad relativa: {datos_clima['weather_forecast']['hoy']['humidity']:.1f}%
#     - Velocidad del viento: {datos_clima['weather_forecast']['hoy']['wind_speed']:.1f} km/h"""
    
#     prompt = f"""{data_description}
    
#     Como experto en riego de precisión, genera un programa de riego optimizado que incluya:
    
#     1. DECISIÓN DE RIEGO (sí/no) con justificación técnica
#     2. CANTIDAD DE AGUA específica (mm o litros/m²)
#     3. HORARIO ÓPTIMO de aplicación
#     4. DURACIÓN Y FRECUENCIA recomendada
#     5. MÉTODO DE APLICACIÓN más eficiente
#     6. CONSIDERACIONES ESPECIALES (enfermedad radicular, lixiviación, etc.)
#     7. PRÓXIMO RIEGO PROGRAMADO
#     8. ALERTAS Y MONITOREO continuo
    
#     Considera eficiencia hídrica, prevención de enfermedades, optimización nutricional 
#     y condiciones climáticas actuales y pronosticadas."""
    
#     return obtener_analisis_agricola(prompt)

# # Generar programas de riego para todas las zonas
# programas_riego = {}
# for zona_id, datos_zona in datos_riego.items():
#     programa = optimizar_programa_riego(zona_id, datos_zona, datos_operacionales)
#     programas_riego[zona_id] = programa
    
#     print(f"\n{'='*60}")
#     print(f"PROGRAMA DE RIEGO OPTIMIZADO - {zona_id}")
#     print(f"{'='*60}")
#     print(programa)
#     print("\n")


