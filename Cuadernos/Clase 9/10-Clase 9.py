import json  
import os   
import pandas as pd
import datetime
import gradio as gr

from pathlib import Path
from io import StringIO
from ollama import chat  

MODEL_NAME = "hf.co/unsloth/gemma-3n-E4B-it-GGUF:UD-Q4_K_XL"

# PRIMERA CONSULTA

# Definición de la consulta técnica
# consulta_tecnica = """ ¿Cuáles son las densidades de siembra recomendadas para soja en la región pampeana argentina?
#        Incluir variaciones por zona geográfica y condiciones de suelo.
#        """
# # Estructura del mensaje para el modelo
# mensaje_consulta = [
#        {
#               "role": "user",
#               "content": consulta_tecnica
#               }
#               ]

# print("Ejecutando consulta al modelo local...")
# print(f"Consulta: {consulta_tecnica}")

# # Llamada al modelo Ollama

# response = chat(
#        model=MODEL_NAME,
#        messages=mensaje_consulta
#        )

# # Extracción y presentación de la respuesta
# respuesta_modelo = response.message.content
# print("\n" + "="*80)
# print("RESPUESTA DEL MODELO:")
# print("="*80)
# print(respuesta_modelo)

# Primera Prueba con Ollama y Gemma-3n-E4B-it-GGUF:UD-Q4_K_XL

"""Ejecutando consulta al modelo local...
Consulta:  ¿Cuáles son las densidades de siembra recomendadas para soja en la región pampeana argentina?
       Incluir variaciones por zona geográfica y condiciones de suelo.


================================================================================       
RESPUESTA DEL MODELO:
================================================================================       
## Densidades de Siembra Recomendadas para Soja en la Región Pampeana Argentina: Variaciones por Zona y Condiciones de Suelo

La densidad de siembra de la soja en la Región Pampeana Argentina es un factor crítico 
para optimizar el rendimiento y la rentabilidad. No existe una única densidad "correcta", ya que varía significativamente según la zona geográfica, las condiciones del suelo, el tipo de variedad de soja y las prácticas de manejo.

A continuación, se presenta un resumen detallado de las densidades de siembra recomendadas, considerando las diferentes variables:

**1. Densidades de Siembra Generales (Tendencias Actuales):**

*   **Rango General:** La densidad de siembra más común en la Región Pampeana actualmente se encuentra entre **280.000 y 350.000 plantas por hectárea (p.h.)**.
*   **Tendencia a Aumentar:**  En los últimos años, se ha observado una tendencia a aumentar la densidad de siembra, especialmente en zonas con buena disponibilidad de agua y suelos fértiles. Esto se debe a que las variedades modernas de soja son más susceptibles a la alta densidad y pueden aprovechar mejor los recursos disponibles.

**2. Variaciones por Zona Geográfica:**

La Región Pampeana se divide en diferentes zonas con características agroclimáticas distintas, lo que influye en la densidad de siembra óptima:

*   **Zona Norte (Entre Ríos, Corrientes):**
    *   **Condiciones:** Clima más cálido y húmedo, con mayor riesgo de enfermedades. Suelos generalmente arcillosos.
    *   **Densidad Recomendada:** **280.000 - 320.000 p.h.**  Se recomienda una densidad ligeramente menor para reducir el riesgo de enfermedades fúngicas.
*   **Zona Central (Santa Fe, Buenos Aires):**
    *   **Condiciones:** Clima templado, con precipitaciones moderadas. Suelos más diversos, desde arcillosos hasta arenosos.
    *   **Densidad Recomendada:** **300.000 - 340.000 p.h.**  Esta zona permite densidades más altas debido a la menor incidencia de enfermedades y la mayor disponibilidad de agua.
*   **Zona Sur (Córdoba, La Pampa):**
    *   **Condiciones:** Clima más frío y seco, con mayor riesgo de heladas. Suelos más arenosos y con menor capacidad de retención de agua.
    *   **Densidad Recomendada:** **260.000 - 300.000 p.h.**  Se recomienda una densidad ligeramente menor para asegurar una mejor germinación y desarrollo de las plantas, especialmente en suelos con baja capacidad de retención de agua.

**3. Variaciones por Condiciones de Suelo:**

La fertilidad del suelo y su capacidad de retención de agua son factores clave para determinar la densidad de siembra:

*   **Suelos Fértiles (Alto contenido de materia orgánica, buena capacidad de retención de agua):**
    *   **Densidad Recomendada:** **320.000 - 350.000 p.h.**  Estos suelos pueden soportar densidades más altas, lo que permite obtener mayores rendimientos.
*   **Suelos Pobres (Bajo contenido de materia orgánica, baja capacidad de retención de agua):**
    *   **Densidad Recomendada:** **260.000 - 300.000 p.h.**  Se recomienda una densidad más baja para evitar la competencia por los recursos y asegurar una mejor germinación y desarrollo de las plantas.
*   **Suelos Arenosos:**
    *   **Densidad Recomendada:** **260.000 - 300.000 p.h.**  Debido a la baja capacidad de retención de agua, se recomienda una densidad más baja para evitar el estrés hídrico.
*   **Suelos Arcillosos:**
    *   **Densidad Recomendada:** **280.000 - 340.000 p.h.**  Estos suelos tienen una mayor capacidad de retención de agua, lo que permite densidades más altas.

**4. Consideraciones Adicionales:**

*   **Variedad de Soja:** Las variedades de soja modernas, especialmente las variedades con tolerancia a la sequía y a enfermedades, pueden tolerar densidades más altas.     
*   **Prácticas de Manejo:** El uso de fertilizantes, la gestión del agua y el control 
de malezas pueden influir en la densidad de siembra óptima.
*   **Análisis de Suelo:** Realizar un análisis de suelo es fundamental para determinar la fertilidad del suelo y la capacidad de retención de agua, lo que permite ajustar la densidad de siembra de manera precisa.
*   **Experiencia Local:** Consultar con técnicos agrícolas locales y basarse en la experiencia de otros productores de la zona es una práctica recomendable.

**Tabla Resumen (aproximada):**

| Zona Geográfica | Tipo de Suelo | Densidad Recomendada (p.h.) |
|-----------------|----------------|---------------------------------|
| Norte           | Arcilloso      | 280.000 - 320.000               |
| Norte           | Arenoso        | 260.000 - 300.000               |
| Central         | Arcilloso      | 300.000 - 340.000               |
| Central         | Arenoso        | 280.000 - 320.000               |
| Sur             | Arcilloso      | 260.000 - 300.000               |
| Sur             | Arenoso        | 260.000 - 300.000               |

**Recomendaciones Finales:**

*   **Realizar un análisis de suelo:** Es fundamental para determinar la fertilidad del suelo y la capacidad de retención de agua.
*   **Consultar con técnicos agrícolas:** Obtener asesoramiento de técnicos agrícolas locales es una práctica recomendable.
*   **Considerar la variedad de soja:** Las variedades modernas pueden tolerar densidades más altas.
*   **Adaptar la densidad de siembra a las condiciones locales:**  La densidad de siembra óptima varía según la zona geográfica y las condiciones del suelo.
*   **Monitorear el desarrollo de las plantas:**  Realizar un monitoreo regular del desarrollo de las plantas permite ajustar las prácticas de manejo y optimizar el rendimiento.

**Fuentes de Información:**

*   **INTA (Instituto Nacional de Tecnología Agropecuaria):** [https://www.inta.gob.ar/](https://www.inta.gob.ar/)
*   **CCTA (Cámara de Comerciantes de Títulos Agropecuarios):** [https://ccta.com.ar/](https://ccta.com.ar/)
*   **Universidades Agrarias:**  Las universidades agroarias de la región suelen tener 
información y recomendaciones sobre la siembra de soja.
*   **Asociaciones de Productores:** Las asociaciones de productores de soja pueden brindar información y asesoramiento sobre las mejores prácticas de manejo.

**Importante:** Esta información es una guía general. Es fundamental consultar con técnicos agrícolas locales y adaptar las prácticas de manejo a las condiciones específicas 
de cada campo."""






# SEGUNDA CONSULTA

# # Definimos el contexto profesional para el asistente de IA
# system_prompt_agronomico = """
# Eres un consultor agronómico con 20 años de experiencia especializado en la región pampeana argentina.
# Tu expertise abarca:
# - Cultivos extensivos (soja, maíz, trigo, girasol)
# - Manejo integrado de plagas y enfermedades
# - Nutrición vegetal y fertilización variable
# - Tecnologías de precisión y agricultura digital
# - Condiciones edafoclimáticas regionales
# - Mercados agropecuarios y rentabilidad

# Características de tus respuestas:
# - Utiliza terminología técnica apropiada
# - Incluye consideraciones económicas cuando sea relevante
# - Referencias específicas a condiciones argentinas (suelos, clima, cultivares)
# - Menciona tecnologías disponibles localmente
# - Proporciona rangos de valores cuantitativos cuando sea apropiado

# Si no tienes información específica sobre un tema, indica claramente esta limitación.
# Responde siempre en español técnico profesional.
# Pero no como una persona, sino como un modelo de lenguaje avanzado entrenado en datos agronómicos.
# """

# # Consulta técnica sobre densidades de siembra
# consulta_densidades = """
# ¿Cuáles son las densidades de siembra recomendadas para soja en la región pampeana argentina?
# Incluir variaciones por zona geográfica, grupo de madurez y condiciones de suelo.
# Considerar también el impacto económico de diferentes densidades.
# """

# # Estructura del mensaje con system prompt
# mensajes_consulta = [
#     {"role": "system", "content": system_prompt_agronomico},
#     {"role": "user", "content": consulta_densidades}
# ]

# print("Ejecutando consulta con system prompt especializado...")
# print(f"Modelo: {MODEL_NAME}")
# print(f"Consulta: {consulta_densidades}")

# # Llamada al modelo con contexto agronómico
# response = chat(
#     model=MODEL_NAME,
#     messages=mensajes_consulta
# )

# # Extracción y presentación de la respuesta
# respuesta_especializada = response.message.content
# print("\n" + "="*80)
# print("RESPUESTA DEL CONSULTOR AGRONÓMICO:")
# print("="*80)
# print(respuesta_especializada)






#Tercera Consulta - En campo en totoras santa fe

# # Extracción de Datos Estructurados: Análisis de Cosecha

# def extract_json_from_text(text: str):
#     """Extrae JSON válido de texto que puede contener explicaciones adicionales."""
#     start = text.find('{')
#     end = text.rfind('}')
#     if start != -1 and end != -1 and end > start:
#         candidate = text[start:end+1]
#         try:
#             return json.loads(candidate)
#         except Exception:
#             return None
#     return None

# # System prompt para análisis de datos agropecuarios
# system_prompt_datos = """
# Eres un analista de datos agropecuarios especializado en procesamiento de información de cosecha.
# Extraes datos estructurados de reportes de campo para análisis posteriores.
# Devuelve información en formato JSON válido con precisión técnica.
# Incluye todos los parámetros productivos y económicos disponibles.
# """

# # Reporte de cosecha real del campo La Esperanza
# reporte_cosecha = """
# REPORTE DE COSECHA 2025 - CAMPO LA FORTALEZA
# Ubicación: Totoras, Santa Fe, Argentina
# Lote: 22-B
# Superficie: 55 hectáreas
# Cultivo: Soja STS 6.8i RSF IPRO
# Fecha de cosecha: 20/03/2025
# Rendimiento promedio: 4,120 kg/ha
# Humedad promedio: 13.1%
# Proteína: 37.8%
# Aceite: 19.5%
# Peso de 1000 granos: 152.5 g
# Precio estimado FOB: USD 435/tn
# Costo directo total: USD 605/ha
# Margen bruto estimado: USD 1,188/ha
# Observaciones técnicas: Excelente llenado de granos pese a estrés hídrico en R3-R4. 
# Aplicación de fungicida en R5.1 con excelente timing.
# """

# # Prompt para extracción estructurada
# prompt_extraccion = f"""
# Analiza el siguiente reporte de cosecha y extrae SOLO un JSON con la siguiente estructura:
# {{
#     "campo": "string",
#     "ubicacion": "string", 
#     "lote": "string",
#     "superficie_ha": float,
#     "cultivo": "string",
#     "fecha_cosecha": "string",
#     "rendimiento_kg_ha": float,
#     "humedad_pct": float,
#     "proteina_pct": float,
#     "aceite_pct": float,
#     "peso_1000_granos_g": float,
#     "precio_usd_tn": float,
#     "costo_directo_usd_ha": float,
#     "margen_bruto_usd_ha": float,
#     "observaciones": "string"
# }}

# REPORTE A ANALIZAR:
# {reporte_cosecha}

# Devuelve SOLO el JSON, sin explicaciones adicionales.
# """

# # Configurar mensajes
# mensajes_extraccion = [
#     {"role": "system", "content": system_prompt_datos},
#     {"role": "user", "content": prompt_extraccion}
# ]

# print("Procesando reporte de cosecha...")
# print("Extrayendo datos estructurados con IA local...")

# # Llamada al modelo
# response = chat(model=MODEL_NAME, messages=mensajes_extraccion)

# try:
#     texto_respuesta = response.message.content
# except Exception:
#     texto_respuesta = str(response)

# print('Respuesta del modelo:')
# print(texto_respuesta)

# # Extraer y procesar JSON
# datos_estructurados = extract_json_from_text(texto_respuesta)
# if datos_estructurados is None:
#     print('\nNo se pudo extraer JSON válido del reporte.')
# else:
#     print('\n' + "="*60)
#     print('DATOS DE COSECHA ESTRUCTURADOS:')
#     print("="*60)
#     print(json.dumps(datos_estructurados, indent=2, ensure_ascii=False))
    
#     # Convertir a DataFrame para análisis
#     df_cosecha = pd.DataFrame([datos_estructurados])
#     print('\nDataFrame generado:')
#     print(df_cosecha.to_string(index=False))
    
#     # Cálculos adicionales de análisis económico
#     produccion_total = datos_estructurados['superficie_ha'] * datos_estructurados['rendimiento_kg_ha'] / 1000
#     ingreso_bruto_total = produccion_total * datos_estructurados['precio_usd_tn']
#     margen_total = datos_estructurados['superficie_ha'] * datos_estructurados['margen_bruto_usd_ha']
    

#     print(f'\n--- ANÁLISIS ECONÓMICO CONSOLIDADO ---')
#     print(f'Producción total: {produccion_total:.1f} toneladas')
#     print(f'Ingreso bruto total: USD {ingreso_bruto_total:,.0f}')
#     print(f'Margen bruto total: USD {margen_total:,.0f}')





# Cuarta Consulta

# Pasar un archivo .txt y devolver un pandas.DataFrame

"""Flujo recomendado:
1. Leer el archivo localmente en Python (si es muy grande, enviar un extracto o resumirlo).
2. Pedir al modelo que devuelva un JSON array donde cada elemento sea un objeto con las columnas deseadas.
3. Parsear el JSON en Python y construir un `pandas.DataFrame`.

A continuación hay un ejemplo completo. Cambiá `FILEPATH` por el archivo que quieras usar. Si el archivo no existe, se crea un ejemplo pequeño para que la celda sea reproducible."""


# DATA_DIR = Path("datos_fitosanitarios")
# TXT_PATH = DATA_DIR / "reporte_fitosanitario.txt"
# CSV_PATH = DATA_DIR / "analisis_fitosanitario.csv"

# def preparar_ambiente(reporte_texto: str):
#     # 1) Crear carpeta si no existe
#     if not DATA_DIR.exists():
#         DATA_DIR.mkdir(parents=True, exist_ok=True)
#         print(f"✓ Carpeta creada: {DATA_DIR.resolve()}")
#     else:
#         print(f"✓ Carpeta existente: {DATA_DIR.resolve()}")

#     # 2) Crear TXT adentro si no existe
#     if not TXT_PATH.exists():
#         TXT_PATH.write_text(reporte_texto, encoding="utf-8")
#         print(f"✓ Archivo TXT creado: {TXT_PATH.name}")
#     else:
#         print(f"✓ Archivo TXT existente: {TXT_PATH.name}")

#     # 3) Avisar si ya hay un CSV previo
#     if CSV_PATH.exists():
#         print(f"• Aviso: ya existe un CSV previo: {CSV_PATH.name}")


# # Creamos un reporte fitosanitario de ejemplo Con Santa Fe
# reporte_fitosanitario_stafe = """
# Fecha: 15 de Marzo de 2025
# Responsable Técnico: Ing. Agr. Carlos Mendoza
# Región: Centro-Norte de Santa Fe (Dpto. San Cristóbal)
# Estación: Fin de ciclo de soja, inicio de cosecha gruesa

# LOTE 5-C - SOJA DM 50i52 IPRO (R6 - Madurez de grano)
# Superficie: 320 hectáreas
# Fecha de siembra: 15 de Noviembre de 2024

# Monitoreo de plagas y enfermedades:

# Chinche de la soja (Piezodorus guildinii y Nezara viridula)
# Densidad promedio: 4.5 chinches/m lineal (muestreo con paño vertical)
# Umbral de daño económico en R6: 2.0 chinches/m lineal
# Distribución: Plaga generalizada en el lote, con focos de alta densidad en el cuadrante NE
# Comentario: Riesgo alto de "Granos Verdes" y "Granos Afectados". Aplicación inmediata requerida previo a la cosecha, respetando los tiempos de carencia.

# Enfermedades de fin de ciclo (Mancha Ojo de Rana - MOR)
# Incidencia: 60% de plantas con síntomas
# Severidad: 20-25% de área foliar afectada en plantas infectadas
# Comentario: Condiciones de rocío y temperaturas templadas favorecieron el avance. Se recomienda evaluar potencial de rendimiento y considerar fungicida de acción antiespórica.

# LOTE 3-B - MAÍZ TARDÍO DK 72-30 VT3P (R2 - Floración)
# Superficie: 180 hectáreas
# Fecha de siembra: 10 de Diciembre de 2024

# Monitoreo de plagas:

# Cogollero (Spodoptera frugiperda)
# Infestación: 18% de plantas con presencia (huevos y larvas pequeñas)
# Severidad: 8% de plantas con daño >20% foliar
# Umbral de daño económico en vegetativo: 20% de plantas con daño
# Comentario: Presión por debajo del umbral, pero con posturas nuevas. Monitoreo intensivo cada 48 horas recomendado. Posible aplicación biológica con Bacillus thuringiensis o insecticidas selectivos si se supera el umbral.

# Arañuela roja (Tetranychus urticae)
# Presencia: Focos detectados en borduras y zonas con estrés hídrico
# Nivel: Incipiente, en aumento
# Comentario: Estrés térmico e hídrico favorece el crecimiento poblacional. Recomendación: aplicación localizada con acaricida específico.

# Condiciones meteorológicas (últimos 7 días)
# Temperatura máxima promedio: 30 °C
# Temperatura mínima promedio: 18 °C
# Humedad relativa: 65% (con rocíos nocturnos abundantes)
# Precipitaciones acumuladas: 5 mm (déficit hídrico leve)
# Pronóstico: tiempo estable, sin lluvias significativas y temperaturas en aumento

# Observaciones generales
# Presencia de insectos benéficos (vaquitas de San Antonio y crisopas) en el lote de maíz.
# Se recomienda programar la cosecha del lote de soja (5-C) en 15-20 días, sujeto a humedad del grano.
# Próximo monitoreo: 22 de Marzo de 2025
# """

# # System prompt especializado en análisis fitosanitario
# system_prompt_fitosanitario = """
# Eres un ingeniero agrónomo especialista en fitopatología y entomología agrícola con 15 años de experiencia en el centro-norte de Argentina. Tu expertise abarca manejo integrado de plagas (MIP), enfermedades de fin de ciclo y malezas resistentes.

# Procesa reportes fitosanitarios para generar:
# - Diagnóstico preciso de problemas sanitarios
# - Evaluación de niveles poblacionales vs. umbrales de daño económico
# - Análisis de condiciones predisponentes (ambientales, fenológicas)
# - Recomendaciones técnicas prioritizadas por urgencia e impacto económico
# - Planes de acción con productos, dosis y momentos de aplicación óptimos
# - Consideraciones sobre resistencia y preservación de fauna benéfica

# Formato de respuesta requerido:
# - JSON estructurado con metadatos del reporte
# - Clasificación por lote y cultivo
# - Niveles de alerta (bajo, medio, alto, crítico)
# - Recomendaciones específicas con fundamentación técnica
# - Proyección de evolución esperada

# Mantén rigor científico citando patógenos con nombre binomial completo y umbrales actualizados para la región pampeana. Prioriza soluciones sustentables y economicamente viables.
# """

# # Prompt para extracción de datos fitosanitarios
# prompt_fitosanitario = f"""
# Analiza el siguiente reporte fitosanitario y extrae la información en formato JSON.
# Estructura requerida:
# {{
#     "fecha_reporte": "string",
#     "responsable": "string", 
#     "lotes": [
#         {{
#             "identificador": "string",
#             "cultivo": "string",
#             "superficie_ha": float,
#             "fecha_siembra": "string",
#             "estado_fenologico": "string",
#             "plagas": [
#                 {{
#                     "nombre_comun": "string",
#                     "nombre_cientifico": "string",
#                     "densidad_observada": float,
#                     "unidad_medida": "string",
#                     "umbral_economico": float,
#                     "superado_umbral": boolean,
#                     "recomendacion": "string",
#                     "prioridad": "string"
#                 }}
#             ]
#         }}
#     ],
#     "condiciones_meteorologicas": {{
#         "temperatura_max": float,
#         "humedad_relativa": float,
#         "precipitaciones_mm": float
#     }}
# }}

# Reporte a analizar:
# {reporte_fitosanitario_stafe}

# Devuelve SOLO el JSON válido, sin texto adicional
# """



# # Configurar mensajes
# mensajes_fitosanitarios = [
#     {"role": "system", "content": system_prompt_fitosanitario},
#     {"role": "user", "content": prompt_fitosanitario}
# ]

# print("Procesando reporte fitosanitario...")
# print("Analizando umbrales de daño económico y recomendaciones...")

# # Si el archivo no existe, creamos el reporte de ejemplo
# preparar_ambiente(reporte_fitosanitario_stafe)

# # Procesamiento con IA local
# response = chat(model=MODEL_NAME, messages=mensajes_fitosanitarios)

# try:
#     texto_respuesta = response.message.content
# except Exception:
#     texto_respuesta = str(response)

# print('Respuesta del modelo:')
# print(texto_respuesta[:500] + "..." if len(texto_respuesta) > 500 else texto_respuesta)


# # Extraer JSON y crear análisis
# def extract_json_array(text: str):
#     start = text.find('{')
#     end = text.rfind('}')
#     if start != -1 and end != -1 and end > start:
#         candidate = text[start:end+1]
#         try:
#             return json.loads(candidate)
#         except Exception:
#             return None
#     return None

# datos_fitosanitarios = extract_json_array(texto_respuesta)
# if not datos_fitosanitarios:
#     print('\nError en extracción JSON. Mostrando respuesta original.')
# else:
#     print('\n' + "="*70)
#     print('ANÁLISIS FITOSANITARIO ESTRUCTURADO:')
#     print("="*70)

# # Crear DataFrame consolidado de plagas
#     plagas_consolidadas = []
#     for lote in datos_fitosanitarios['lotes']:
#         for plaga in lote['plagas']:
#             plagas_consolidadas.append({
#                 'lote': lote['identificador'],
#                 'cultivo': lote['cultivo'],
#                 'superficie_ha': lote['superficie_ha'],
#                 'plaga': plaga['nombre_comun'],
#                 'densidad': plaga['densidad_observada'],
#                 'umbral': plaga['umbral_economico'],
#                 'requiere_tratamiento': plaga['superado_umbral'],
#                 'prioridad': plaga['prioridad']
#             })
    
#     df_plagas = pd.DataFrame(plagas_consolidadas)
#     print('\nRESUMEN DE MONITOREO:')
#     print(df_plagas.to_string(index=False))
    
#     # Análisis de prioridades de tratamiento
#     tratamientos_requeridos = df_plagas[df_plagas['requiere_tratamiento'] == True]
#     superficie_total_tratamiento = tratamientos_requeridos['superficie_ha'].sum()
    
#     print(f'\n--- PLAN DE ACCIÓN FITOSANITARIO ---')
#     print(f'Superficie que requiere tratamiento: {superficie_total_tratamiento} hectáreas')
#     print(f'Número de focos de alto riesgo: {len(tratamientos_requeridos)}')
    
#     if len(tratamientos_requeridos) > 0:
#         print('\nTRATAMIENTOS PRIORITARIOS:')
#         for _, fila in tratamientos_requeridos.iterrows():
#             print(f'• {fila["lote"]} ({fila["cultivo"]}): {fila["plaga"]} - {fila["prioridad"]} prioridad')
    
#     # Guardar datos para análisis posterior
#     df_plagas.to_csv(CSV_PATH, index=False, encoding='utf-8')
#     print(f'\n✓ Datos guardados en: {CSV_PATH.resolve()}')



# Quinta Consulta - Interfaz Gradio

## Herramienta de Procesamiento Agropecuario: Democratización del Acceso a IA

# La siguiente interfaz está diseñada para **democratizar el acceso a IA en equipos agropecuarios**, permitiendo que profesionales sin conocimientos técnicos de programación puedan procesar:

# - **Reportes de campo**: Monitoreos, aplicaciones, observaciones técnicas
# - **Análisis de laboratorio**: Suelos, granos, forrajes, agua
# - **Informes técnicos**: Asesorías, recomendaciones, planes de manejo

# ### Características técnicas:
# - **Procesamiento local**: Sin dependencia de conectividad externa
# - **Múltiples formatos**: TXT, CSV, PDF (texto plano)
# - **Análisis estructurado**: Extracción automática de datos técnicos
# - **Interfaz intuitiva**: Diseñada para usuarios no técnicos
# - **Exportación estándar**: Resultados en formato CSV para análisis posterior


def procesar_documento_agropecuario(archivo_subido, tipo_analisis):
    """
    Procesa documentos agropecuarios utilizando IA local especializada.
    
    Parámetros:
    - archivo_subido: Documento a procesar (TXT, CSV)
    - tipo_analisis: Tipo de análisis a realizar
    """
    
    if archivo_subido is None:
        return pd.DataFrame([{"Error": "No se ha subido ningún archivo"}]), None
    
    try:
        # 1. Leer el contenido del archivo
        with open(archivo_subido.name, 'r', encoding='utf-8') as f:
            contenido_documento = f.read()
        
        # 2. Configurar el system prompt según el tipo de análisis
        system_prompts = {
            "Reporte de Campo": """
            Eres un especialista en análisis de reportes de campo agropecuarios.
            Extraes información estructurada sobre: lotes, cultivos, fechas, observaciones,
            aplicaciones, condiciones meteorológicas y recomendaciones técnicas.
            """,
            "Análisis de Laboratorio": """  
            Eres un especialista en interpretación de análisis de laboratorio agropecuario.
            Procesas resultados de: análisis de suelos, calidad de granos, forrajes,
            agua de riego y parámetros nutricionales.
            """,
            "Informe Técnico": """
            Eres un consultor agronómico especializado en informes técnicos.
            Analizas recomendaciones de manejo, planes de fertilización,
            estrategias de control sanitario y evaluaciones económicas.
            """,
            "Monitoreo Fitosanitario": """
            Eres un especialista en protección vegetal y manejo integrado de plagas.
            Procesas monitoreos de plagas, enfermedades, malezas,
            umbrales económicos y recomendaciones de tratamiento.
            """
        }
        
        # 3. Configurar el prompt específico
        system_prompt = system_prompts.get(tipo_analisis, system_prompts["Reporte de Campo"])
        
        user_prompt = f"""
        Analiza el siguiente documento agropecuario y extrae la información en formato CSV.
        
        IMPORTANTE:
        - Primera fila: nombres de columnas separados por comas
        - Filas siguientes: datos correspondientes a cada registro
        - Usar punto y coma (;) si hay comas en los datos
        - Incluir todas las variables técnicas relevantes
        - Mantener precisión en valores numéricos
        
        DOCUMENTO A PROCESAR:
        {contenido_documento}
        
        Devuelve ÚNICAMENTE el contenido CSV, sin explicaciones adicionales.
        """
        
        # 4. Llamar al modelo Ollama
        respuesta = chat(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        
        csv_resultado = respuesta.message.content
        
        # 5. Procesar y validar el resultado CSV
        try:
            # Intentar leer el CSV generado
            df_resultado = pd.read_csv(StringIO(csv_resultado))
            
            # Agregar metadatos del procesamiento
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f"procesamiento_agropecuario_{timestamp}.csv"
            
            # 6. Guardar archivo de salida
            with open(nombre_archivo, 'w', encoding='utf-8') as f:
                f.write(csv_resultado)
            
            # 7. Crear reporte de procesamiento
            info_procesamiento = pd.DataFrame([{
                "Archivo procesado": archivo_subido.name,
                "Tipo de análisis": tipo_analisis,
                "Registros extraídos": len(df_resultado),
                "Columnas identificadas": len(df_resultado.columns),
                "Fecha de procesamiento": datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
            }])
            
            return df_resultado, nombre_archivo, info_procesamiento
            
        except Exception as e:
            # Si falla el parsing CSV, mostrar el resultado crudo
            df_error = pd.DataFrame([{
                "Resultado del procesamiento": csv_resultado[:1000] + "..." if len(csv_resultado) > 1000 else csv_resultado
            }])
            return df_error, None, pd.DataFrame([{"Error": f"Error en formato CSV: {str(e)}"}])
            
    except Exception as e:
        error_df = pd.DataFrame([{"Error": f"Error en procesamiento: {str(e)}"}])
        return error_df, None, error_df

# Crear interfaz profesional para equipos agropecuarios
with gr.Blocks(
    title="Procesador Agropecuario con IA Local",
    theme=gr.themes.Soft()
) as interfaz_agropecuaria:
    
    gr.Markdown("""
    # 🌾 Procesador de Documentos Agropecuarios
    ### Análisis Inteligente con IA Local para Equipos Técnicos
    
    Esta herramienta permite procesar automáticamente documentos técnicos agropecuarios 
    utilizando inteligencia artificial ejecutada localmente, garantizando la **confidencialidad** 
    de datos sensibles del establecimiento.
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            archivo_entrada = gr.File(
                label="📄 Subir Documento",
                file_types=[".txt", ".csv"],
                file_count="single"
            )
            
            tipo_procesamiento = gr.Dropdown(
                choices=[
                    "Reporte de Campo",
                    "Análisis de Laboratorio", 
                    "Informe Técnico",
                    "Monitoreo Fitosanitario"
                ],
                label="🔬 Tipo de Análisis",
                value="Reporte de Campo"
            )
            
            btn_procesar = gr.Button(
                "⚡ Procesar con IA Local",
                variant="primary",
                size="lg"
            )
        
        with gr.Column(scale=2):
            info_procesamiento = gr.Dataframe(
                label="ℹ️ Información del Procesamiento",
                interactive=False
            )
    
    with gr.Row():
        vista_previa = gr.Dataframe(
            label="📊 Vista Previa de Datos Extraídos",
            interactive=False,
            wrap=True
        )
    
    with gr.Row():
        archivo_descarga = gr.File(
            label="💾 Descargar Resultado en CSV",
            interactive=False
        )
    
    # Configurar la acción del botón
    btn_procesar.click(
        fn=procesar_documento_agropecuario,
        inputs=[archivo_entrada, tipo_procesamiento],
        outputs=[vista_previa, archivo_descarga, info_procesamiento]
    )
    
    gr.Markdown("""
    ---
    **🔒 Características de Seguridad:**
    - Procesamiento 100% local, sin envío de datos a servidores externos
    - Confidencialidad garantizada para información sensible del establecimiento
    - Compatible con normativas de protección de datos agropecuarios
    
    **📈 Casos de Uso Típicos:**
    - Digitalización de reportes de monitoreo de campo
    - Procesamiento de resultados de análisis de laboratorio
    - Extracción de datos de informes técnicos de asesores
    - Sistematización de registros fitosanitarios
    """)

# Ejecutar la interfaz
print("Iniciando herramienta de procesamiento agropecuario...")
print("Democratizando el acceso a IA para equipos técnicos del sector...")

# Lanzar interfaz (en producción usar share=False por seguridad)
interfaz_agropecuaria.launch(
    server_name="127.0.0.1",  # Solo acceso local por seguridad
    server_port=7860,
    share=False,  # Sin compartir públicamente 
    quiet=False
)