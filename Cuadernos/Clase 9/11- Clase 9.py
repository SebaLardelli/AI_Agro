import requests 

# Configuración del modelo base
LM_STUDIO_URL = "http://127.0.0.1:1234/"

import requests

LM_STUDIO_URL = "http://127.0.0.1:1234/v1/chat/completions"
headers = {"Authorization": "Bearer lm-studio"}  # LM Studio lo acepta así

payload = {
    "model": "NombreExactoDelModeloEnLMStudio",  # tal cual aparece en LM Studio
    "messages": [
        {"role": "system", "content": "Eres un consultor agronómico..."},
        {"role": "user", "content": "¿Cuáles son las densidades de siembra...?"}
    ]
}

r = requests.post(LM_STUDIO_URL, headers=headers, json=payload, timeout=60)
r.raise_for_status()
print(r.json()["choices"][0]["message"]["content"])

print("Configuración completada. Entorno listo para implementación de IA local.")


# Definición de la consulta técnica
consulta_tecnica = """ ¿Cuáles son las densidades de siembra recomendadas para soja en la región pampeana argentina?
       Incluir variaciones por zona geográfica y condiciones de suelo.
       """

# Estructura del mensaje para el modelo
mensaje_consulta = {
    "prompt": consulta_tecnica
}

print("Ejecutando consulta al modelo local...")
print(f"Consulta: {consulta_tecnica}")

# Llamada al modelo LM Studio
response = requests.post(LM_STUDIO_URL + "api/chat", json=mensaje_consulta)

# Extracción y presentación de la respuesta
respuesta_modelo = response.json().get('response', 'No se recibió respuesta del modelo')
print("\n" + "="*80)
print("RESPUESTA DEL MODELO:")
print("="*80)
print(respuesta_modelo)

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
print(f"Consulta: {consulta_densidades}")

response = requests.post(LM_STUDIO_URL + "api/chat", json={"messages": mensajes_consulta})


# Extracción y presentación de la respuesta
respuesta_especializada = response.json().get('response', 'No se recibió respuesta del modelo')
print("\n" + "="*80)
print("RESPUESTA DEL CONSULTOR AGRONÓMICO:")
print("="*80)
print(respuesta_especializada)


#RESPUESTA 

"""
¡Hola! Como consultor agronómico, entiendo que necesitas información sobre densidades de siembra. Es una pregunta fundamental en la agricultura y depende de muchos factores. Para darte una respuesta precisa y útil, necesito un poco más de información. Sin embargo, te puedo proporcionar una guía general y 
luego te haré preguntas para afinar la respuesta.

**En términos generales, la densidad de siembra se refiere al número de plantas que se siembran por unidad de superficie (por ejemplo, plantas por metro cuadrado o plantas por hectárea).**  La densidad óptima varía enormemente dependiendo del cultivo, la variedad, el sistema de siembra, las condiciones climáticas y los objetivos del agricultor.

Aquí te dejo una tabla con **densidades de siembra aproximadas para algunos cultivos comunes**:       

| Cultivo       | Densidad de Siembra (aproximada) | Notas
                          |
|----------------|-----------------------------------|----------------------------------------------------------------------------|
| **Maíz**         | 25-30 plantas/m²                 | Depende de la variedad, siembra directa o convencional.                   |
| **Soja**          | 500-700 plantas/m²                | Varía según la variedad y el sistema de siembra.                          |
| **Trigo**        | 125-150 plantas/m²                | Depende del tipo de trigo (invierno o primavera) y la variedad.           |
| **Cebada**       | 150-200 plantas/m²                | Similar al trigo, depende del tipo y variedad.                            |
| **Arroz**        | 100-200 plantas/m²                 | Varía según la variedad y el sistema de siembra (inundación o seco).   |
| **Frijol**       | 15-30 plantas/m²                  | Depende de la variedad, siembra directa o en 
bancales.                   |
| **Calabaza**     | 2-4 plantas/m²                    | Espacio amplio requerido para el desarrollo de las plantas.               |
| **Tomate**       | 2-3 plantas/m²                    | Depende del sistema de cultivo (en línea, en 
cámara).                       |
| **Lechuga**      | 10-20 plantas/m²                   | Depende del tamaño de la planta y el método 
de siembra.                  |

**Factores que influyen en la densidad de siembra:**

*   **Cultivo específico:** Cada cultivo tiene sus propias necesidades óptimas de densidad para maximizar el rendimiento.
*   **Variedad:** Diferentes variedades dentro de un mismo cultivo pueden tener diferentes requerimientos de espacio. Algunas variedades son más altas o tienen sistemas de raíces más extensos que otras.  
*   **Sistema de siembra:**  Siembra directa, en bancales, en línea... cada sistema impacta la densidad óptima.
*   **Disponibilidad de nutrientes:** En suelos ricos en nutrientes, se puede usar una mayor densidad 
de siembra.
*   **Disponibilidad de agua:** En condiciones de sequía, es mejor reducir la densidad para evitar el 
estrés hídrico.
*   **Control de malezas:** Una mayor densidad de siembra puede ayudar a suprimir las malezas.        
*   **Clima:**  El clima (temperatura, humedad, luz solar) también influye en la densidad óptima.     
*   **Objetivos del agricultor:** ¿Se busca un alto rendimiento por hectárea? ¿O se prioriza la calidad de los frutos?

**Para poder ayudarte mejor, necesito que me digas:**

1.  **¿Qué cultivo estás considerando sembrar?**
2.  **¿En qué región o país te encuentras?** (Esto es importante para considerar las condiciones climáticas locales).
3.  **¿Qué variedad del cultivo planeas utilizar?** (Si la conoces).
4.  **¿Cuál es el sistema de siembra que vas a emplear?** (Siembra directa, en bancales, en línea...) 
5.  **¿Cuáles son tus objetivos principales?** (Maximizar el rendimiento, mejorar la calidad, etc.)   

Con esta información, podré darte recomendaciones más específicas y precisas sobre la densidad de siembra óptima para tu situación particular. También puedo sugerirte recursos adicionales, como publicaciones técnicas o contactos con especialistas en el cultivo que te interesa.

Configuración completada. Entorno listo para implementación de IA local.
Ejecutando consulta al modelo local...""" 