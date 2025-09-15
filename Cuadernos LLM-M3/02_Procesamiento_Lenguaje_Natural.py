import os
from dotenv import load_dotenv  
from google import genai
from google.genai import types
from rich.console import Console
from rich.markdown import Markdown

load_dotenv() 

console = Console()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

cliente = genai.Client(api_key=GOOGLE_API_KEY)

MODEL_ID = "gemini-2.5-pro" # @param ["gemini-2.5-pro", "gemini-2.5-flash", "gemini-2.5-flash-lite"] {"allow-input":true, isTemplate: true}

# reporte_campo = """REPORTE QUINCENAL DE CAMPO - ESTABLECIMIENTO LA PAMPA
# Fecha: 15/01/2024
# Responsable: Ing. Agr. Carlos Mendoza
# Ubicación: Pergamino, Buenos Aires

# LOTE 15-A (Soja DM4670): Excelente desarrollo vegetativo en V8. Se observa
# presencia de chinche verde en borduras (2.1 chinches/metro lineal), por encima
# del umbral económico. Requiere monitoreo intensivo y probable aplicación de
# insecticida en los próximos 3-5 días si la población se mantiene.

# LOTE 22-C (Maíz DK692): Estado R2 (ampollado). Buen llenado de grano pese a
# estrés hídrico leve en diciembre. Aplicación de fungicida preventiva realizada
# el 10/01. No se observan síntomas de roya del maíz hasta el momento.

# CONDICIONES METEOROLÓGICAS: Temperaturas altas (32-35°C) con alta humedad
# relativa (78%). Pronóstico indica lluvias para el fin de semana (15-25mm).
# Condiciones favorables para desarrollo de enfermedades foliares.

# RECOMENDACIONES: Acelerar monitoreo fitosanitario. Evaluar aplicación preventiva
# en maíz si persiste alta humedad. Considerar cosecha temprana en lotes de soja
# que alcancen R7 antes de febrero."""

# print("\nReporte agronómico definido para demostrar Gemini API.")

reporte_campo = """REPORTE QUINCENAL DE CAMPO – PROVINCIA DE SANTA FE

Fecha: 13/09/2025
Responsable Técnico: Ing. Agr. Juan Pérez
Ubicación: Departamento Castellanos, Santa Fe

El Lote 15-A de soja grupo IV DM 4670 se encuentra en estado fenológico R5 inicio de llenado de grano.
Presenta un desarrollo vegetativo uniforme con buen cierre de entresurco.
En borduras de este lote se detecta chinche verde Nezara viridula con un promedio de 2.8 individuos por metro lineal, superando el umbral económico.

El Lote 22-C de maíz híbrido DK 7210 se encuentra en estado fenológico R3 grano lechoso.
El cultivo presenta buen potencial de rendimiento.
En el sector sur de este lote se registran síntomas iniciales de roya común Puccinia sorghi en hojas del tercio medio con una afectación leve menor al cinco por ciento del área foliar.

Las condiciones meteorológicas indican una temperatura media de 29 grados con máximas de 33 grados.
La humedad relativa fue del 75 por ciento y las precipitaciones acumuladas de 12 milímetros en la última semana.
El pronóstico anuncia lluvias aisladas de entre 10 y 20 milímetros en los próximos cinco días.

Se recomienda intensificar el monitoreo de chinches en el lote 15-A de soja y considerar aplicación de insecticida si la población se mantiene o aumenta.
En el lote 22-C de maíz evaluar la necesidad de fungicida en función de la evolución de la roya y las condiciones de humedad.
Mantener control de malezas en ambos lotes y planificar una cosecha escalonada en soja si se acelera el avance a R7."""

""" Resumen Ejecutivo de Reportes """

# pregunta = f"""Como agrónomo senior, resumí este reporte de campo en 2 oraciones ejecutivas
# para el gerente de producción:

# Reporte: {reporte_campo}
# """

# respuesta = cliente.models.generate_content(
#     model=MODEL_ID,
#     contents=[pregunta] # Pasa la pregunta como contenido
# )
# console.print(Markdown(respuesta.text))

""" Respuesta """

#     Reporte agronómico definido para demostrar Gemini API.
# Aquí tienes dos opciones, ambas directas y enfocadas en la acción y el riesgo:

# Opción 1 (Directa): El lote de soja requiere una aplicación inminente de insecticida por superar el   
# umbral de chinche, mientras que el maíz, aunque en buen estado, enfrenta un alto riesgo de
# enfermedades foliares por las condiciones de humedad y las próximas lluvias.

# Opción 2 (Ligeramente más detallada): Detectamos una plaga de chinche en soja que ya justifica una    
# aplicación para proteger el rinde, y debemos mantener máxima alerta en el maíz, ya que su buen        
# potencial está en riesgo por las condiciones climáticas favorables a enfermedades.

""" Evaluacion de Riesgo  Agronómico """

# pregunta = f"""Evaluá el nivel de riesgo de este reporte agronómico:
# Opciones: BAJO, MEDIO, ALTO

# Incluí las razones técnicas de tu evaluación.

# Reporte: {reporte_campo}
# """

# respuesta = cliente.models.generate_content(
#     model=MODEL_ID,
#     contents=[pregunta] # Pasa la pregunta como contenido
# )

# console.print(Markdown(respuesta.text))

""" Respuesta """

#     Reporte agronómico definido para demostrar Gemini API.
# Claro, aquí está la evaluación del reporte agronómico.

# ──────────────────────────────────────────────────────────────────────────────────────────────────────                                        Nivel de Riesgo: MEDIO

# ──────────────────────────────────────────────────────────────────────────────────────────────────────                                  Razones Técnicas de la Evaluación:

# El nivel de riesgo se clasifica como MEDIO debido a la combinación de un problema fitosanitario ya    
# presente y por encima del umbral de daño, junto con condiciones meteorológicas muy favorables para el 
# desarrollo de nuevas amenazas que requieren gestión activa e inmediata.

# A continuación, el desglose técnico por punto:

# 1. Presencia de Plaga por Encima del Umbral de Daño Económico (UDE) en Soja (Factor de Riesgo Alto    
# para este lote):

#  • Plaga y Nivel: La detección de "chinche verde (2.1 chinches/metro lineal)" en el lote de soja está 
#    por encima de los umbrales de daño económico comúnmente aceptados para esta etapa del cultivo (que 
#    suelen rondar entre 1 y 2 chinches/metro, dependiendo del estado fenológico).
#  • Impacto Potencial: La chinche verde (principalmente Nezara viridula) es un insecto picador-suctor  
#    que, en las etapas reproductivas de la soja (a las que se aproxima el cultivo en V8), causa un daño   directo a las vainas y granos. Este daño resulta en:
#     • Merma de rendimiento: Por aborto de vainas o granos mal llenados.
#     • Pérdida de calidad: Granos "chuzados" o manchados que afectan el poder germinativo y el valor   
#       comercial.
#  • Acción Requerida: El reporte indica correctamente la necesidad de una "probable aplicación de      
#    insecticida". Esto significa que ya existe una situación que probablemente requerirá un costo de   
#    control para evitar una pérdida económica mayor.

# 2. Condiciones Meteorológicas Predisponentes (Factor de Riesgo General Elevado):

#  • "Caldo de Cultivo": La combinación de temperaturas altas (32-35°C), alta humedad relativa (78%) y  
#    lluvias pronosticadas es el escenario ideal para la proliferación de enfermedades fúngicas foliares   en ambos cultivos.
#  • Enfermedades en Maíz: Aunque se aplicó un fungicida preventivo, estas condiciones de alta presión  
#    pueden superar la residualidad del producto o favorecer patógenos no cubiertos. El maíz en R2      
#    (ampollado) es muy susceptible a enfermedades como la Roya común del maíz (Puccinia sorghi) y el   
#    Tizón del norte (Exserohilum turcicum), que afectan el área foliar y, por ende, el llenado de      
#    grano.
#  • Enfermedades en Soja: Para la soja, estas condiciones favorecen el desarrollo de Mancha Ojo de Rana   (Cercospora sojina) y enfermedades de fin de ciclo, que podrían impactar significativamente el     
#    rendimiento si no se controlan a tiempo.

# 3. Estado del Cultivo de Maíz (Factor de Riesgo Controlado pero Latente):

#  • Punto a Favor: El maíz presenta un "buen llenado de grano" y ya recibió una aplicación preventiva  
#    de fungicida. Esto reduce el riesgo inmediato.
#  • Punto de Atención: El "estrés hídrico leve en diciembre" pudo haber sensibilizado al cultivo,      
#    haciéndolo potencialmente más susceptible a nuevas amenazas si las condiciones se vuelven adversas.   El estado R2 es crítico para la definición del rendimiento, por lo que cualquier nuevo estrés      
#    (biótico o abiótico) tendría un impacto considerable.

#                                      Conclusión de la Evaluación:

# El riesgo no es BAJO porque hay un problema concreto y cuantificado (chinches) que ya superó el umbraleconómico y exige una intervención.

# El riesgo no es ALTO (todavía) porque los problemas están identificados, el maíz está preventivamente 
# protegido y existen recomendaciones claras para mitigar las amenazas. La situación es manejable con   
# las acciones correctas y oportunas.

# Por lo tanto, el riesgo es MEDIO: existen amenazas reales e inminentes que, si no se gestionan de     
# forma proactiva y eficaz en los próximos días, tienen un alto potencial de causar pérdidas económicas 
# significativas.


""" Extracción de Datos Técnicos """

# prompt = f"""Extraé los siguientes datos técnicos del reporte:
# - Cultivos y variedades
# - Estados fenológicos
# - Plagas/enfermedades detectadas
# - Umbrales económicos
# - Fechas importantes
# - Ubicaciones geográficas

# Reporte: {reporte_campo}
# """

# respuesta = cliente.models.generate_content(
#     model=MODEL_ID,
#     contents=[prompt] # Pasa la pregunta como contenido
# )

# console.print(Markdown(respuesta.text))

""" Respuesta """

#     Reporte agronómico definido para demostrar Gemini API.
# Claro, aquí están los datos técnicos extraídos del reporte:

# Cultivos y variedades:

#  • Soja: Variedad DM4670
#  • Maíz: Variedad DK692

# Estados fenológicos:

#  • Soja (Lote 15-A): V8 (desarrollo vegetativo)
#  • Maíz (Lote 22-C): R2 (ampollado)

# Plagas/enfermedades detectadas:

#  • Chinche verde: Presencia en borduras del lote de soja (2.1 chinches/metro lineal).
#  • Roya del maíz: Se menciona como una enfermedad a monitorear, pero no se observan síntomas hasta el 
#    momento.

# Umbrales económicos:

#  • Chinche verde en soja: El reporte indica que la población actual (2.1 chinches/metro lineal) está  
#    por encima del umbral económico.

# Fechas importantes:

#  • 10/01/2024: Aplicación de fungicida preventivo en maíz.
#  • 15/01/2024: Fecha del reporte.
#  • Próximos 3-5 días (aprox. 18-20 de enero): Plazo para una posible aplicación de insecticida en     
#    soja.
#  • Fin de semana (posterior al 15/01): Pronóstico de lluvias.
#  • Antes de febrero: Plazo a considerar para la cosecha temprana de soja.

# Ubicaciones geográficas:

#  • Establecimiento "La Pampa".
#  • Pergamino, Buenos Aires.

""" Consultas Específicas sobre el reporte """

# pregunta = "¿Qué lotes requieren acción inmediata y por qué?"
# contexto = reporte_campo

# prompt = f"""Respondé la siguiente consulta técnica basada en el reporte:

# Reporte: {contexto}
# Consulta: {pregunta}
# """

# respuesta = cliente.models.generate_content(
#     model=MODEL_ID,
#     contents=[contexto, pregunta] # Pasa la pregunta como contenido
# )
# console.print(Markdown(respuesta.text))

""" Respuesta """

# Reporte agronómico definido para demostrar Gemini API.
# Según el reporte, el lote que requiere acción inmediata es el Lote 15-A (Soja).

# ¿Por qué?

#  • Plaga por encima del umbral: Se detectó una población de chinche verde de 2.1 individuos por metro 
#    lineal, lo cual está por encima del umbral económico. Esto significa que la plaga ya se encuentra  
#    en un nivel que puede causar pérdidas económicas significativas en el cultivo.
#  • Acción recomendada a corto plazo: El reporte indica la necesidad de un "monitoreo intensivo" y una 
#    "probable aplicación de insecticida en los próximos 3-5 días", lo que confirma la urgencia de la   
#    situación.

""" Recomendaciones Priorizadas """

# prompt = f"""Generá 3 recomendaciones técnicas priorizadas basadas en este reporte:

# Reporte: {reporte_campo}

# Formato:
# 1. [URGENTE/MEDIA/BAJA] - Acción específica
# """

# respuesta = cliente.models.generate_content(
#     model=MODEL_ID,
#     contents=[prompt] # Pasa la pregunta como contenido
# )
# console.print(Markdown(respuesta.text))

""" Respuesta """

# Reporte agronómico definido para demostrar Gemini API.
# Aquí tenés 3 recomendaciones técnicas priorizadas, basadas en el reporte y en el formato solicitado:  

#  1 [URGENTE] - Realizar la aplicación de un insecticida selectivo en el Lote 15-A (Soja) para el      
#    control de chinche verde dentro de las próximas 72 horas, priorizando las borduras que es donde se 
#    concentra la plaga. La población ya supera el umbral de daño económico y el estado V8 es crítico.  
#  2 [MEDIA] - Intensificar el monitoreo de enfermedades foliares (ej. roya, tizón) en el Lote 22-C     
#    (Maíz) inmediatamente después de las lluvias pronosticadas. Las condiciones de alta temperatura y  
#    humedad son extremadamente favorables para su desarrollo, y el estado R2 es clave para el llenado  
#    de grano.
#  3 [BAJA] - Planificar un re-muestreo de plagas en el Lote 15-A (Soja) 3-4 días después de la
#    aplicación del insecticida para evaluar la eficacia del control y decidir sobre la necesidad de    
#    futuras acciones.

""" Traducción para Exportadores """

# prompt = f"""Traducí al inglés este resumen técnico para el reporte del comprador internacional:

# Extrae solo la información de calidad y estado de cultivos:

# Reporte: {reporte_campo}
# """

# respuesta = cliente.models.generate_content(
#     model=MODEL_ID,
#     contents=[prompt] # Pasa la pregunta como contenido
# )

# console.print(Markdown(respuesta.text))

""" Respuesta """

# ──────────────────────────────────────────────────────────────────────────────────────────────────────Technical Summary: Crop Quality & Status

# Lot 15-A (Soybean DM4670):

#  • Excellent vegetative development, currently at the V8 stage.
#  • Pest pressure from green stink bugs has been detected on field borders (2.1 bugs/linear meter),    
#    exceeding the economic threshold. This poses a risk to crop quality if not managed.

# Lot 22-C (Corn DK692):

#  • The crop is at the R2 (blister) growth stage.
#  • Grain fill is good, despite mild water stress experienced in December.
#  • The crop is currently free of common rust symptoms following a preventive fungicide application on 
#    January 10th.

# General Conditions:

#  • Current weather conditions (high heat and humidity) are favorable for the development of foliar    
#    diseases, posing a potential risk to overall plant health.

""" Comunicación con Productores"""

# prompt = f"""Basado en este reporte técnico, redactá un WhatsApp breve (máximo 3 líneas)
# para el productor explicando la situación y próximos pasos:

# Reporte: {reporte_campo}

# Tono: Profesional pero accesible, sin jerga excesiva.
# """

# respuesta = cliente.models.generate_content(
#     model=MODEL_ID,
#     contents=[prompt] # Pasa la pregunta como contenido
# )

# console.print(Markdown(respuesta.text))

""" Respuesta """

#     Reporte agronómico definido para demostrar Gemini API.
# Hola. Detectamos chinche verde en la soja (15-A) por encima de lo recomendado; el maíz viene bien.    
# Vamos a monitorear la plaga de cerca en los próximos 3-5 días. Según la evolución, definiremos si es  
# necesaria una aplicación. Te mantengo al tanto.

""" Clasificación de Alertas Fitosanitarias """

# categorias = ["sin_accion", "monitoreo_intensivo", "aplicacion_inmediata", "emergencia_fitosanitaria"]

# prompt = f"""Clasificá este reporte según el nivel de respuesta requerido:
# Categorías: {', '.join(categorias)}

# Justificá tu elección con criterios técnicos.

# Reporte: {reporte_campo}
# """

# respuesta = cliente.models.generate_content(
#     model=MODEL_ID,
#     contents=[prompt] # Pasa la pregunta como contenido
# )

# console.print(Markdown(respuesta.text))

""" Respuesta """

# Reporte agronómico definido para demostrar Gemini API.
# Claro, aquí está la clasificación y la justificación técnica del reporte.

# ──────────────────────────────────────────────────────────────────────────────────────────────────────                                  Clasificación: monitoreo_intensivo

#                                         Justificación Técnica

# La elección de monitoreo_intensivo se basa en la combinación de una amenaza fitosanitaria que ha      
# superado un umbral crítico con una recomendación profesional que, si bien anticipa una acción
# correctiva, aún deja un margen para la observación y la toma de decisiones en el cortísimo plazo.     

# Los criterios técnicos son los siguientes:

#  1 Superación del Umbral de Daño Económico (UDE): El punto más crítico del reporte es la detección de 
#    "2.1 chinches/metro lineal" en el lote de soja, un valor que se declara explícitamente "por encima 
#    del umbral económico". Técnicamente, esto significa que el costo del daño potencial causado por la 
#    plaga ya es mayor que el costo de su control. Este hecho por sí solo descarta la categoría
#    sin_accion.
#  2 La Acción Recomendada no es Inmediata, sino Inminente: A pesar de haber superado el UDE, la        
#    recomendación del Ing. Agrónomo no es una aplicación instantánea, sino "monitoreo intensivo y      
#    probable aplicación de insecticida en los próximos 3-5 días". Esta redacción es clave:
#     • "Monitoreo intensivo" es la acción primaria y urgente. Se necesita verificar si la población    
#       sigue activa, si se desplaza desde las borduras hacia el interior del lote o si factores        
#       naturales (como predadores) la están controlando.
#     • "Probable aplicación" indica una alta posibilidad, pero no una certeza absoluta. La decisión    
#       final se tomará en base a los resultados del monitoreo intensificado.
#     • El plazo de "3-5 días" define una ventana de acción crítica, pero no una emergencia que requiera      pulverizar en las próximas 24 horas. Esto diferencia la situación de una aplicacion_inmediata.  
#  3 Condiciones Ambientales como Factor de Riesgo Agravante: El reporte indica "temperaturas altas con 
#    alta humedad relativa" y pronóstico de lluvias. Estas son condiciones predisponentes para el       
#    desarrollo de enfermedades fúngicas (como la roya en el maíz) y pueden acelerar los ciclos de los  
#    insectos. Esto refuerza la necesidad de "acelerar el monitoreo fitosanitario" en todos los lotes,  
#    no solo en el afectado por chinches.
#  4 Ausencia de Carácter de Emergencia: La situación, aunque grave para el lote 15-A, involucra una    
#    plaga común (Chinche verde) en un área localizada (borduras). No se trata de una plaga
#    cuarentenaria, de una dispersión masiva e incontrolable, ni de un evento que requiera la
#    intervención de organismos estatales, lo que descarta por completo la categoría de
#    emergencia_fitosanitaria.

# En resumen, el reporte describe una situación de alta criticidad que ha cruzado un umbral técnico de  
# daño. Sin embargo, la acción recomendada para el momento actual es la intensificación de la vigilanciapara confirmar la necesidad y optimizar el momento de una intervención química que se considera muy   
# probable y cercana en el tiempo. Por lo tanto, monitoreo_intensivo es la categoría que mejor describe 
# el nivel de respuesta requerido.


""" EJERCICIO PRÁCTICO """

"""Creá tu propio reporte de campo con:
- 2 lotes diferentes (cultivo, estado, observaciones)
- Al menos 1 problema fitosanitario
- Condiciones meteorológicas
- Recomendaciones

Luego usá Gemini API para:
1. Generar un resumen ejecutivo
2. Extraer datos técnicos estructurados  
3. Clasificar el nivel de riesgo
4. Crear recomendaciones priorizadas

**Objetivo**: Practicar la integración de Gemini API con datos agronómicos reales."""

# instrucciones = [
#     "Como agrónomo senior, resumí este reporte de campo en 2 oraciones ejecutivas para el gerente de producción. \n\n",

#     """Extraé los siguientes datos técnicos del reporte:
#     - Cultivos y variedades
#     - Estados fenológicos
#     - Plagas/enfermedades detectadas
#     - Umbrales económicos
#     - Fechas importantes
#     - Ubicaciones geográficas \n\n""",

#     """Evaluá el nivel de riesgo de este reporte agronómico:
#     Opciones: BAJO, MEDIO, ALTO

#     Incluí las razones técnicas de tu evaluación \n\n""",

#     """Generá 3 recomendaciones técnicas priorizadas basadas en este reporte:

#     Formato:
#     1. [URGENTE/MEDIA/BAJA] - Acción específica \n\n""",
    
#     f"Reporte: {reporte_campo}"
# ]

# respuesta = cliente.models.generate_content(
#     model=MODEL_ID,
#     contents=[("user", instr) for instr in instrucciones]  # se transforma en tuplas automáticamente
# )

# console.print(Markdown(respuesta.text))


"""" Respuesta """

# Claro, aquí está el análisis completo del reporte agronómico.

#                                           Resumen Ejecutivo

# El lote de soja requiere una aplicación inmediata de insecticida para controlar una plaga de chinches 
# que ya supera el umbral de daño económico. Por otro lado, el maíz presenta un buen potencial pero debeser monitoreado de cerca por un brote inicial de roya, cuyas condiciones de propagación son favorablessegún el pronóstico.

# ──────────────────────────────────────────────────────────────────────────────────────────────────────                                     Extracción de Datos Técnicos

#  • Cultivos y variedades:
#     • Soja: Grupo IV, variedad DM 4670.
#     • Maíz: Híbrido DK 7210.
#  • Estados fenológicos:
#     • Soja: R5 (inicio de llenado de grano).
#     • Maíz: R3 (grano lechoso).
#  • Plagas/enfermedades detectadas:
#     • Chinche verde (Nezara viridula) en soja.
#     • Roya común (Puccinia sorghi) en maíz.
#  • Umbrales económicos:
#     • Superado en soja para chinche verde (población de 2.8 individuos/metro lineal).
#  • Fechas importantes:
#     • Fecha del reporte: 13/09/2025.
#     • Pronóstico de lluvias: Próximos 5 días.
#  • Ubicaciones geográficas:
#     • Departamento Castellanos, Santa Fe.
#     • Lote 15-A (soja).
#     • Lote 22-C (maíz).

# ──────────────────────────────────────────────────────────────────────────────────────────────────────                                    Evaluación de Nivel de Riesgo

# MEDIO

# Razones técnicas:

#  1 Daño económico activo: La población de chinche verde en soja (Lote 15-A) ya superó el umbral       
#    económico. Esto significa que el cultivo está sufriendo una pérdida de rendimiento cuantificable en   este momento. La etapa R5 (llenado de grano) es un período crítico donde el daño de la chinche     
#    tiene un impacto directo en el peso y la calidad del grano.
#  2 Condiciones predisponentes para enfermedad: El maíz (Lote 22-C) presenta síntomas iniciales de roya   en una etapa crítica (R3), y las condiciones meteorológicas pronosticadas (alta humedad,
#    temperaturas cálidas y lluvias) son altamente favorables para una rápida propagación de la
#    enfermedad. Si no se monitorea, la situación puede escalar rápidamente a un nivel de daño
#    económico.

# El riesgo no es "ALTO" porque el problema del maíz es aún incipiente y controlable, pero tampoco es   
# "BAJO" debido a la pérdida de rendimiento activa en la soja.

# ──────────────────────────────────────────────────────────────────────────────────────────────────────                                 Recomendaciones Técnicas Priorizadas

#  1 [URGENTE] - Realizar una aplicación inmediata de insecticida específico para el control de chinches   en el Lote 15-A (soja), debido a que la población actual de 2.8 individuos/metro supera el umbral  
#    económico en la etapa crítica de llenado de grano (R5).
#  2 [MEDIA] - Intensificar el monitoreo de la severidad de Roya Común en el Lote 22-C (maíz). Dada la  
#    etapa R3 y el pronóstico de lluvias y humedad, se debe estar preparado para una aplicación de      
#    fungicida si la enfermedad avanza y supera el 5% de afectación en las hojas superiores al tercio   
#    medio.
#  3 [BAJA] - Programar una nueva recorrida de campo en los lotes, con especial foco en el Lote 22-C    
#    (maíz), dentro de los próximos 5-7 días (post-lluvias pronosticadas) para re-evaluar la evolución  
#    de la Roya y el estado general del cultivo.