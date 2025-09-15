# Importación de librerías core
import json  # Procesamiento de datos estructurados
import os    # Operaciones del sistema de archivos
import pandas as pd  # Análisis y manipulación de datos tabulares
from ollama import chat # Cliente para interacción con modelos Ollama

MODEL_NAME = "hf.co/unsloth/gemma-3n-E4B-it-GGUF:UD-Q4_K_XL"


# Definición de la consulta técnica
consulta_tecnica = """ ¿Cuáles son las densidades de siembra recomendadas para soja en la región pampeana argentina?
       Incluir variaciones por zona geográfica y condiciones de suelo.
       """
# Estructura del mensaje para el modelo
mensaje_consulta = [
       {
              "role": "user",
              "content": consulta_tecnica
              }
              ]

print("Ejecutando consulta al modelo local...")
print(f"Consulta: {consulta_tecnica}")

# Llamada al modelo Ollama

response = chat(
       model=MODEL_NAME,
       messages=mensaje_consulta
       )

# Extracción y presentación de la respuesta
respuesta_modelo = response.message.content
print("\n" + "="*80)
print("RESPUESTA DEL MODELO:")
print("="*80)
print(respuesta_modelo)

""" Resultado """

# Ejecutando consulta al modelo local...
# Consulta:  ¿Cuáles son las densidades de siembra recomendadas para soja en la región pampeana argentina?
#        Incluir variaciones por zona geográfica y condiciones de suelo.
       

# ================================================================================
# RESPUESTA DEL MODELO:
# ================================================================================      
# ## Densidades de Siembra Recomendadas para Soja en la Región Pampeana Argentina: Variaciones por Zona y Condiciones de Suelo

# La densidad de siembra de la soja en la región pampeana argentina es un factor crítico para optimizar el rendimiento y la rentabilidad. No existe una densidad única, ya que varía según la zona geográfica, las condiciones del suelo, el manejo de la cosecha anterior y la variedad de soja utilizada.

# A continuación, se detallan las recomendaciones generales y las variaciones por zona y tipo de suelo, considerando las tendencias actuales de la agricultura moderna.       

# **Recomendaciones Generales (2023-2024):**

# *   **Rango General:** La densidad de siembra recomendada en la región pampeana se encuentra generalmente entre **280.000 a 350.000 plantas por hectárea (pfl/ha)**.        
# *   **Tendencia Actual:** Existe una tendencia creciente hacia densidades más altas, especialmente en zonas con buena disponibilidad de agua y suelos fértiles.
# *   **Importancia de la Variedad:** La densidad óptima depende en gran medida de la variedad de soja que se utilice. Las variedades más modernas y de alto potencial de rendimiento suelen ser más eficientes a densidades más altas.
# *   **Manejo de la Cosecha Anterior:** Un buen manejo de la cosecha anterior (residuo, fertilización, etc.) influye en la densidad óptima.
# *   **Análisis de Suelo:** Realizar un análisis de suelo es fundamental para ajustar la densidad de siembra y la fertilización.

# **Variaciones por Zona Geográfica:**

# 1.  **Zona Norte (Suries de Buenos Aires, Santa Fe, Entre Ríos):**
#     *   **Condiciones:** Suelos más arenosos, menor disponibilidad de agua en algunas 
# áreas, mayor riesgo de sequía.
#     *   **Densidad Recomendada:** **280.000 - 320.000 pfl/ha**.
#     *   **Consideraciones:** Se recomienda utilizar variedades adaptadas a condiciones de menor humedad y con buena tolerancia a la sequía.  Es importante optimizar la fertilización nitrogenada.

# 2.  **Zona Central (Buenos Aires, parte de Santa Fe):**
#     *   **Condiciones:** Suelos más arcillosos y fértiles, mayor disponibilidad de agua en general.
#     *   **Densidad Recomendada:** **300.000 - 350.000 pfl/ha**.
#     *   **Consideraciones:** Se pueden utilizar variedades de alto potencial de rendimiento. Es importante controlar la maleza y optimizar la fertilización.

# 3.  **Zona Sur (Río Negro, Neuquén, sectores de Buenos Aires):**
#     *   **Condiciones:** Suelos más arcillosos y con buena retención de agua, clima más templado.
#     *   **Densidad Recomendada:** **320.000 - 350.000 pfl/ha**.
#     *   **Consideraciones:** Se pueden utilizar variedades con mayor resistencia a enfermedades.  La fertilización fósforo y potasio es importante.

# **Variaciones por Condiciones de Suelo:**

# 1.  **Suelos Arenosos:**
#     *   **Densidad Recomendada:** **280.000 - 310.000 pfl/ha**.
#     *   **Consideraciones:**  Se requiere una mayor disponibilidad de agua y nutrientes.  Se recomienda utilizar variedades con buen sistema radicular para aprovechar los recursos hídricos.  La fertilización nitrogenada debe ser cuidadosa para evitar pérdidas por lixiviación.

# 2.  **Suelos Arcillosos:**
#     *   **Densidad Recomendada:** **320.000 - 350.000 pfl/ha**.
#     *   **Consideraciones:**  Estos suelos retienen mejor el agua y los nutrientes.  Se pueden utilizar variedades de alto potencial de rendimiento.  La fertilización debe 
# ser equilibrada para evitar problemas de fitotoxicidad.

# 3.  **Suelos Limosos:**
#     *   **Densidad Recomendada:** **300.000 - 340.000 pfl/ha**.
#     *   **Consideraciones:**  Estos suelos presentan características intermedias entre los arenosos y los arcillosos.  La densidad de siembra debe ajustarse a las características específicas del suelo.

# **Factores Adicionales a Considerar:**

# *   **Variedad de Soja:**  Las variedades de soja modernas, especialmente las de alto 
# potencial de rendimiento, pueden tolerar densidades de siembra más altas.  Consultar las recomendaciones específicas del productor de la variedad.
# *   **Manejo de la Maleza:** Un buen control de la maleza es fundamental para maximizar el rendimiento en densidades altas.
# *   **Fertilización:**  La fertilización adecuada es esencial para apoyar el crecimiento de las plantas y alcanzar el potencial de rendimiento.
# *   **Condiciones Climáticas:**  En años con condiciones climáticas adversas (sequía, 
# exceso de humedad), puede ser necesario ajustar la densidad de siembra.
# *   **Tecnología de Siembra:**  El uso de tecnologías de siembra de precisión (sembradoras de alta precisión) permite una distribución más uniforme de las plantas y optimiza el rendimiento.

# **Recomendaciones Finales:**

# *   **Consultar con un técnico agrícola:**  Es fundamental consultar con un técnico agrícola local para obtener recomendaciones específicas para su campo, considerando las 
# condiciones locales y la variedad de soja que se utilizará.
# *   **Realizar ensayos de densidad:**  Realizar ensayos de densidad en su campo puede 
# ayudar a determinar la densidad óptima para su situación particular.
# *   **Monitorear el desarrollo de las plantas:**  Monitorear el desarrollo de las plantas durante la temporada de crecimiento puede ayudar a identificar problemas y ajustar el manejo.

# **Fuentes de Información:**

# *   **CINTRA (Confederación de la Industria de Semillas Argentinas):** [https://www.cintra.org.ar/](https://www.cintra.org.ar/)
# *   **INTA (Instituto Nacional de Tecnología Agropecuaria):** [https://www.inta.gob.ar/](https://www.inta.gob.ar/)
# *   **Universidades Agrarias:**  Las universidades agrarias de la región pampeana suelen tener información y recomendaciones sobre la siembra de soja.
# *   **Empresas de Semillas:**  Las empresas de semillas suelen proporcionar recomendaciones específicas para sus variedades.

# **Descargo de Responsabilidad:**

# Esta información se proporciona únicamente con fines informativos y no debe considerarse como asesoramiento profesional. Las recomendaciones de densidad de siembra pueden variar según las condiciones específicas de cada campo. Es importante consultar con un 
# técnico agrícola local antes de tomar cualquier decisión.

# System Prompt Especializado para Consultoría Agronómica

# Definimos el contexto profesional para el asistente de IA
system_prompt_agronomico = """
Eres un consultor agronómico con 20 años de experiencia especializado en la región pampeana argentina.
Tu expertise abarca:
- Cultivos extensivos (soja, maíz, trigo, girasol)
- Manejo integrado de plagas y enfermedades
- Nutrición vegetal y fertilización variable
- Tecnologías de precisión y agricultura digital
- Condiciones edafoclimáticas regionales
- Mercados agropecuarios y rentabilidad

Características de tus respuestas:
- Utiliza terminología técnica apropiada
- Incluye consideraciones económicas cuando sea relevante
- Referencias específicas a condiciones argentinas (suelos, clima, cultivares)
- Menciona tecnologías disponibles localmente
- Proporciona rangos de valores cuantitativos cuando sea apropiado

Si no tienes información específica sobre un tema, indica claramente esta limitación.
Responde siempre en español técnico profesional.
"""

# Consulta técnica sobre densidades de siembra
consulta_densidades = """
¿Cuáles son las densidades de siembra recomendadas para soja en la región pampeana argentina?
Incluir variaciones por zona geográfica, grupo de madurez y condiciones de suelo.
Considerar también el impacto económico de diferentes densidades.
"""

# Estructura del mensaje con system prompt
mensajes_consulta = [
    {"role": "system", "content": system_prompt_agronomico},
    {"role": "user", "content": consulta_densidades}
]

print("Ejecutando consulta con system prompt especializado...")
print(f"Modelo: {MODEL_NAME}")
print(f"Consulta: {consulta_densidades}")

# Llamada al modelo con contexto agronómico
response = chat(
    model=MODEL_NAME,
    messages=mensajes_consulta
)

# Extracción y presentación de la respuesta
respuesta_especializada = response.message.content
print("\n" + "="*80)
print("RESPUESTA DEL CONSULTOR AGRONÓMICO:")
print("="*80)
print(respuesta_especializada)

""" Resultado """

# Ejecutando consulta al modelo local...
# Consulta:  ¿Cuáles son las densidades de siembra recomendadas para soja en la región pampeana argentina?
#        Incluir variaciones por zona geográfica y condiciones de suelo.


# ================================================================================      
# RESPUESTA DEL MODELO:
# ================================================================================      
# ## Densidades de Siembra Recomendadas para Soja en la Región Pampeana Argentina (2024)
# Las densidades de siembra recomendadas para soja en la región pampeana argentina varían significativamente dependiendo de la zona geográfica, las condiciones del suelo, el 
# manejo del cultivo y las variedades de soja utilizadas.  A continuación, se presenta un resumen detallado, considerando estas variables:

# **Consideraciones Generales:**

# * **Tendencia Actual:** La tendencia actual es hacia densidades de siembra más altas, 
# aprovechando variedades con mejor capacidad de llenado de granos y mayor tolerancia a 
# la competencia.
# * **Variedad de Soja:**  La densidad óptima depende en gran medida de la variedad. Las variedades de maduración temprana suelen requerir densidades más bajas que las de maduración tardía.
# * **Condiciones Climáticas:**  En zonas con mayor riesgo de sequía, se pueden considerar densidades ligeramente más bajas para reducir la competencia por el agua.
# * **Manejo del Cultivo:**  El uso de herbicidas, fertilizantes y prácticas de manejo del suelo influyen en la densidad óptima.
# * **Análisis de Suelo:**  Un análisis de suelo es fundamental para determinar las necesidades nutricionales del cultivo y ajustar la densidad de siembra.

# **Densidades de Siembra Recomendadas por Zona Geográfica y Condiciones de Suelo:**    

# **1. Región Norte de la Pampa (Santiago del Estero, Tucumán, Salta):**

# * **Características:** Suelos generalmente más arcillosos, con menor disponibilidad de agua y mayor riesgo de sequía.  Clima más cálido.
# * **Densidad Recomendada:**
#     * **Suelo Fértil (buena disponibilidad de agua):** 280.000 - 320.000 plantas/ha.  
#     * **Suelo Semi-Fértil (disponibilidad moderada de agua):** 250.000 - 280.000 plantas/ha.
#     * **Suelo Poco Fértil (baja disponibilidad de agua):** 220.000 - 250.000 plantas/ha.
# * **Consideraciones:**  Priorizar variedades de maduración temprana y con buena tolerancia a la sequía.  Considerar el uso de técnicas de conservación de agua.

# **2. Región Central de la Pampa (Córdoba, La Pampa, Buenos Aires Norte):**

# * **Características:** Suelos más limosos o franco-limosos, con buena disponibilidad de agua en general.  Clima templado.
# * **Densidad Recomendada:**
#     * **Suelo Fértil (buena disponibilidad de agua):** 300.000 - 350.000 plantas/ha.  
#     * **Suelo Semi-Fértil (disponibilidad moderada de agua):** 280.000 - 320.000 plantas/ha.
#     * **Suelo Poco Fértil (baja disponibilidad de agua):** 260.000 - 300.000 plantas/ha.
# * **Consideraciones:**  Variedades de maduración media a tardía.  Optimizar la fertilización para maximizar el rendimiento.

# **3. Región Sur de la Pampa (Buenos Aires Sur, Santa Fe, Entre Ríos):**

# * **Características:** Suelos franco-arcillosos, con buena disponibilidad de agua en general.  Clima templado.
# * **Densidad Recomendada:**
#     * **Suelo Fértil (buena disponibilidad de agua):** 320.000 - 360.000 plantas/ha.  
#     * **Suelo Semi-Fértil (disponibilidad moderada de agua):** 300.000 - 340.000 plantas/ha.
#     * **Suelo Poco Fértil (baja disponibilidad de agua):** 280.000 - 320.000 plantas/ha.
# * **Consideraciones:**  Variedades de maduración tardía.  Prestar atención al manejo de malezas.

# **Variaciones por Tipo de Suelo:**

# * **Suelos Arcillosos:**  Generalmente requieren densidades más bajas (220.000 - 280.000 plantas/ha) debido a la menor aireación y drenaje.
# * **Suelos Limosos:**  Pueden soportar densidades más altas (280.000 - 350.000 plantas/ha) debido a su mejor drenaje y aireación.
# * **Suelos Franco-Limosos:**  Ofrecen un buen equilibrio y permiten densidades intermedias (260.000 - 330.000 plantas/ha).
# * **Suelos Arenosos:**  Requieren densidades más altas (280.000 - 350.000 plantas/ha) 
# para compensar la menor capacidad de retención de agua y nutrientes.

# **Recomendaciones Adicionales:**

# * **Uso de Software de Simulación:**  Utilizar software de simulación de cultivos para optimizar la densidad de siembra en función de las condiciones específicas del campo.* **Monitoreo del Cultivo:**  Realizar un monitoreo regular del cultivo para detectar 
# problemas de densidad y ajustar las prácticas de manejo.
# * **Consultar con Expertos:**  Consultar con técnicos agrónomos y empresas de semillas para obtener recomendaciones específicas para la variedad de soja y las condiciones del campo.
# * **Considerar la Rotación de Cultivos:** La rotación de cultivos puede mejorar la salud del suelo y reducir la incidencia de enfermedades, lo que puede influir en la densidad de siembra.

# **Fuentes de Información:**

# * **CIMSA (Consorcio de Investiga ción de Soja):**  [https://www.cimsa.com.ar/](https://www.cimsa.com.ar/)
# * **INTA (Instituto Nacional de Tecnología Agropecuaria):** [https://www.inta.gob.ar/](https://www.inta.gob.ar/)
# * **Universidades Agrarias:**  Muchas universidades agrícolas en la región pampeana publican información sobre soja y densidades de siembra.
# * **Empresas de Semillas:**  Las empresas de semillas suelen proporcionar recomendaciones específicas para sus variedades.

# **Importante:**  Esta información es una guía general.  Es fundamental consultar con un técnico agrónomo local para obtener recomendaciones personalizadas para su campo.  Las condiciones pueden variar significativamente de un lugar a otro, y la densidad óptima dependerá de una variedad de factores.

# Espero que esta información sea útil.  Recuerda que la optimización de la densidad de 
# siembra es una práctica clave para maximizar el rendimiento y la rentabilidad del cultivo de soja.

# Ejecutando consulta con system prompt especializado...
# Modelo: hf.co/unsloth/gemma-3n-E4B-it-GGUF:UD-Q4_K_XL
# Consulta:
# ¿Cuáles son las densidades de siembra recomendadas para soja en la región pampeana argentina?
# Incluir variaciones por zona geográfica, grupo de madurez y condiciones de suelo.     
# Considerar también el impacto económico de diferentes densidades.


# ================================================================================      
# RESPUESTA DEL CONSULTOR AGRONÓMICO:
# ================================================================================      
# ## Densidades de Siembra Recomendadas para Soja en la Región Pampeana Argentina: Un Análisis Detallado

# Estimado cliente,

# Como consultor agronómico con experiencia en la región pampeana, entiendo la importancia de optimizar la densidad de siembra en soja para maximizar la productividad y rentabilidad. A continuación, presento un análisis detallado de las densidades recomendadas, considerando variaciones geográficas, grupos de madurez y condiciones de suelo, junto con el impacto económico asociado.

# **Consideraciones Generales:**

# La densidad de siembra de la soja en Argentina ha experimentado una evolución significativa en los últimos años, pasando de densidades más altas a densidades más bajas, impulsadas por el desarrollo de nuevos cultivares y la mejora en las prácticas de manejo.  La tendencia actual favorece densidades más bajas, generalmente entre 280.000 y 350.000 plantas por hectárea (pp/ha), pero esta elección debe ser adaptada a las condiciones específicas de cada campo.

# **Variaciones por Zona Geográfica:**

# La región pampeana es diversa, con diferentes condiciones edafoclimáticas que influyen en la densidad óptima.

# *   **Zona Norte (Sistemas Agropecuarios de Desarrollo - SADE):**  En esta zona, caracterizada por suelos más arenosos y climas más cálidos, se suelen recomendar densidades de **300.000 a 330.000 pp/ha**.  La adaptación de cultivares tempranos y el manejo de la humedad del suelo son cruciales para el éxito.
# *   **Zona Central (SADE):**  Esta zona, con suelos más fértiles y climas moderados, permite densidades de siembra ligeramente más altas, generalmente entre **320.000 y 350.000 pp/ha**.  La elección de cultivares de madurez media es común.
# *   **Zona Sur (SADE):**  En esta zona, con suelos más arcillosos y climas más fríos, 
# se recomienda una densidad de siembra más baja, entre **280.000 y 310.000 pp/ha**.  La selección de cultivares de madurez variable o tardía es importante para asegurar la maduración completa en el corto período de crecimiento.

# **Variaciones por Grupo de Madurez:**

# La elección del grupo de madurez es un factor clave para optimizar la densidad de siembra.

# *   **Cultivares Tempranos (Grupo 0-2):**  Estos cultivares son ideales para zonas con estaciones de crecimiento cortas y/o con riesgo de heladas tardías.  Se pueden sembrar a densidades más altas, entre **320.000 y 340.000 pp/ha**, para maximizar la captación de recursos y compensar su menor potencial de rendimiento.
# *   **Cultivares de Madurez Media (Grupo 3-4):**  Estos cultivares son los más comunes en la región y ofrecen un buen equilibrio entre rendimiento y adaptación.  La densidad de siembra recomendada suele estar entre **300.000 y 330.000 pp/ha**.
# *   **Cultivares Tardíos (Grupo 5-6):**  Estos cultivares son más adecuados para zonas con estaciones de crecimiento largas y/o con mayor disponibilidad de agua.  Se pueden sembrar a densidades más bajas, entre **280.000 y 300.000 pp/ha**, para evitar problemas de llenado de grano.

# **Consideraciones de Suelo:**

# *   **Suelos Arenosos:**  En suelos arenosos, la capacidad de retención de agua es baja, por lo que se recomienda una densidad de siembra ligeramente más alta (hasta 330.000 pp/ha) para asegurar una cobertura adecuada y evitar la pérdida de nutrientes por lixiviación.
# *   **Suelos Arcillosos:**  En suelos arcillosos, la capacidad de retención de agua es alta, por lo que se puede utilizar una densidad de siembra ligeramente más baja (hasta 310.000 pp/ha) para evitar la competencia por recursos.
# *   **Suelos de Humus Alto:**  En suelos con alto contenido de materia orgánica, la densidad de siembra puede ser ligeramente más alta, ya que la materia orgánica mejora la disponibilidad de nutrientes y la capacidad de retención de agua.

# **Impacto Económico de Diferentes Densidades:**

# La densidad de siembra tiene un impacto directo en la rentabilidad de la soja.  En general, se observa una relación positiva entre la densidad de siembra y el rendimiento, 
# hasta un punto óptimo.  Más allá de ese punto, el aumento de la densidad puede generar una disminución del rendimiento debido a la competencia por recursos (luz, agua, nutrientes).

# *   **Densidades Bajas (Menos de 280.000 pp/ha):**  Generalmente, ofrecen menores rendimientos, pero pueden ser más rentables en condiciones de sequía o con limitaciones de nutrientes.
# *   **Densidades Óptimas (280.000 - 350.000 pp/ha):**  Ofrecen el mejor equilibrio entre rendimiento y rentabilidad, y son la opción más común en la región.
# *   **Densidades Altas (Más de 350.000 pp/ha):**  Pueden generar un aumento del rendimiento en condiciones de alta disponibilidad de agua y nutrientes, pero también pueden 
# aumentar el riesgo de fallas y reducir la rentabilidad.

# **Tecnologías Disponibles Localmente:**

# *   **Maquinaria de Siembra de Alta Precisión:**  Permite una distribución uniforme de las semillas y una densidad de siembra precisa.
# *   **Sistemas de Monitoreo de la Humedad del Suelo:**  Ayudan a determinar el momento óptimo de siembra y la densidad de siembra.
# *   **Software de Gestión Agrícola:**  Permite analizar datos históricos y simular diferentes escenarios de siembra para optimizar la densidad.

# **Limitaciones:**

# Es importante destacar que las densidades de siembra recomendadas son orientativas y pueden variar según las condiciones específicas de cada campo.  La elección de la densidad óptima debe basarse en un análisis integral de las condiciones edafoclimáticas, el grupo de madurez del cultivar, la disponibilidad de agua y nutrientes, y los objetivos de rentabilidad del productor.  Además, la disponibilidad de agua y las condiciones 
# climáticas durante la campaña son factores críticos que pueden influir en el rendimiento y la rentabilidad.

# **Recomendación:**

# Le recomiendo realizar un análisis de suelo y un monitoreo de la humedad del suelo antes de tomar una decisión sobre la densidad de siembra.  También le sugiero consultar con un especialista en agricultura digital para utilizar herramientas de simulación y optimización de la densidad.

# Espero que esta información le sea de utilidad.  Estoy a su disposición para cualquier consulta adicional.

# Atentamente,

# [Su Nombre]

# Consultor Agronómico Especializado en la Región Pampeana.


"""## Forzar un formato de salida (JSON)

Pedir al modelo que devuelva SOLO JSON facilita el parseo automático. Siempre indicar explícitamente: "Devuelve SOLO JSON, sin explicaciones adicionales". Aun así, el modelo puede añadir texto; por eso incluimos una heurística para extraer el JSON.

En entornos de producción podés validar la estructura con `jsonschema` o `pydantic`."""


# Extracción de Datos Estructurados: Análisis de Cosecha

def extract_json_from_text(text: str):
    """Extrae JSON válido de texto que puede contener explicaciones adicionales."""
    start = text.find('{')
    end = text.rfind('}')
    if start != -1 and end != -1 and end > start:
        candidate = text[start:end+1]
        try:
            return json.loads(candidate)
        except Exception:
            return None
    return None

# System prompt para análisis de datos agropecuarios
system_prompt_datos = """
Eres un analista de datos agropecuarios especializado en procesamiento de información de cosecha.
Extraes datos estructurados de reportes de campo para análisis posteriores.
Devuelve información en formato JSON válido con precisión técnica.
Incluye todos los parámetros productivos y económicos disponibles.
"""

# Reporte de cosecha real del campo La Esperanza
reporte_cosecha = """
REPORTE DE COSECHA 2024 - CAMPO LA ESPERANZA
Ubicación: Pergamino, Buenos Aires
Lote: 15-A
Superficie: 450 hectáreas
Cultivo: Soja DM4670 INTACTA RR2 PRO
Fecha de cosecha: 15/03/2024
Rendimiento promedio: 3,850 kg/ha
Humedad promedio: 12.8%
Proteína: 38.2%
Aceite: 19.1%
Peso de 1000 granos: 148.2 g
Precio estimado FOB: USD 425/tn
Costo directo total: USD 580/ha
Margen bruto estimado: USD 1,060/ha
Observaciones técnicas: Excelente llenado de granos pese a estrés hídrico en R3-R4.
Aplicación de fungicida en R5.1 con excelente timing.
"""

# Prompt para extracción estructurada
prompt_extraccion = f"""
Analiza el siguiente reporte de cosecha y extrae SOLO un JSON con la siguiente estructura:
{{
    "campo": "string",
    "ubicacion": "string",
    "lote": "string",
    "superficie_ha": float,
    "cultivo": "string",
    "fecha_cosecha": "string",
    "rendimiento_kg_ha": float,
    "humedad_pct": float,
    "proteina_pct": float,
    "aceite_pct": float,
    "peso_1000_granos_g": float,
    "precio_usd_tn": float,
    "costo_directo_usd_ha": float,
    "margen_bruto_usd_ha": float,
    "observaciones": "string"
}}

REPORTE A ANALIZAR:
{reporte_cosecha}

Devuelve SOLO el JSON, sin explicaciones adicionales.
"""

# Configurar mensajes
mensajes_extraccion = [
    {"role": "system", "content": system_prompt_datos},
    {"role": "user", "content": prompt_extraccion}
]

print("Procesando reporte de cosecha...")
print("Extrayendo datos estructurados con IA local...")

# Llamada al modelo
response = chat(model=MODEL_NAME, messages=mensajes_extraccion)

try:
    texto_respuesta = response.message.content
except Exception:
    texto_respuesta = str(response)

print('Respuesta del modelo:')
print(texto_respuesta)

# Extraer y procesar JSON
datos_estructurados = extract_json_from_text(texto_respuesta)
if datos_estructurados is None:
    print('\nNo se pudo extraer JSON válido del reporte.')
else:
    print('\n' + "="*60)
    print('DATOS DE COSECHA ESTRUCTURADOS:')
    print("="*60)
    print(json.dumps(datos_estructurados, indent=2, ensure_ascii=False))

    # Convertir a DataFrame para análisis
    df_cosecha = pd.DataFrame([datos_estructurados])
    print('\nDataFrame generado:')
    print(df_cosecha.to_string(index=False))

    # Cálculos adicionales de análisis económico
    produccion_total = datos_estructurados['superficie_ha'] * datos_estructurados['rendimiento_kg_ha'] / 1000
    ingreso_bruto_total = produccion_total * datos_estructurados['precio_usd_tn']
    margen_total = datos_estructurados['superficie_ha'] * datos_estructurados['margen_bruto_usd_ha']

    print(f'\n--- ANÁLISIS ECONÓMICO CONSOLIDADO ---')
    print(f'Producción total: {produccion_total:.1f} toneladas')
    print(f'Ingreso bruto total: USD {ingreso_bruto_total:,.0f}')
    print(f'Margen bruto total: USD {margen_total:,.0f}')

""" Resultado """

# Procesando reporte de cosecha...
# Extrayendo datos estructurados con IA local...
# Respuesta del modelo:
# ```json
# {
#   "campo": "LA ESPERANZA",
#   "ubicacion": "Pergamino, Buenos Aires",
#   "lote": "15-A",
#   "superficie_ha": 450.0,
#   "cultivo": "Soja DM4670 INTACTA RR2 PRO",
#   "fecha_cosecha": "15/03/2024",
#   "rendimiento_kg_ha": 3850.0,
#   "humedad_pct": 12.8,
#   "proteina_pct": 38.2,
#   "aceite_pct": 19.1,
#   "peso_1000_granos_g": 148.2,
#   "precio_usd_tn": 425.0,
#   "costo_directo_usd_ha": 580.0,
#   "margen_bruto_usd_ha": 1060.0,
#   "observaciones": "Excelente llenado de granos pese a estrés hídrico en R3-R4. Aplicación de fungicida en R5.1 con excelente timing."
# }
# ```

# ============================================================
# DATOS DE COSECHA ESTRUCTURADOS:
# ============================================================
# {
#   "campo": "LA ESPERANZA",
#   "ubicacion": "Pergamino, Buenos Aires",
#   "lote": "15-A",
#   "superficie_ha": 450.0,
#   "cultivo": "Soja DM4670 INTACTA RR2 PRO",
#   "fecha_cosecha": "15/03/2024",
#   "rendimiento_kg_ha": 3850.0,
#   "humedad_pct": 12.8,
#   "proteina_pct": 38.2,
#   "aceite_pct": 19.1,
#   "peso_1000_granos_g": 148.2,
#   "precio_usd_tn": 425.0,
#   "costo_directo_usd_ha": 580.0,
#   "margen_bruto_usd_ha": 1060.0,
#   "observaciones": "Excelente llenado de granos pese a estrés hídrico en R3-R4. Aplicación de fungicida en R5.1 con excelente timing."
# }

# DataFrame generado:
#        campo               ubicacion lote  superficie_ha                     cultivo fecha_cosecha  rendimiento_kg_ha  humedad_pct  proteina_pct  aceite_pct  peso_1000_granos_g  precio_usd_tn  costo_directo_usd_ha  margen_bruto_usd_ha
#                                                                              observaciones
# LA ESPERANZA Pergamino, Buenos Aires 15-A          450.0 Soja DM4670 INTACTA RR2 PRO  
#   15/03/2024             3850.0         12.8          38.2        19.1               148.2          425.0                 580.0               1060.0 Excelente llenado de granos pese a estrés hídrico en R3-R4. Aplicación de fungicida en R5.1 con excelente timing.

# --- ANÁLISIS ECONÓMICO CONSOLIDADO ---
# Producción total: 1732.5 toneladas
# Ingreso bruto total: USD 736,312
# Margen bruto total: USD 477,000

""" ## Pasar un archivo .txt y devolver un pandas.DataFrame

Flujo recomendado:
1. Leer el archivo localmente en Python (si es muy grande, enviar un extracto o resumirlo).
2. Pedir al modelo que devuelva un JSON array donde cada elemento sea un objeto con las columnas deseadas.
3. Parsear el JSON en Python y construir un `pandas.DataFrame`.

A continuación hay un ejemplo completo. Cambiá `FILEPATH` por el archivo que quieras usar. Si el archivo no existe, se crea un ejemplo pequeño para que la celda sea reproducible. """

