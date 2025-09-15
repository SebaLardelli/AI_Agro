import torch
torch.__version__
import chromadb
from chromadb.utils import embedding_functions


torch.cuda.is_available()

client = chromadb.Client()

client.list_collections()

# Cargamos un modelo que entiende mejor el español técnico
modelo_multilenguaje = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="intfloat/multilingual-e5-large"
)

# Creamos nuestra primera colección para consultas agrícolas
collection = client.create_collection(
    name="ConsultasAgricolas",
)

client.list_collections()

# Consultas técnicas reales de productores argentinos
consultas_productores = [
    "Mi maíz tiene las hojas amarillas y no sé si es falta de nitrógeno o exceso de agua.",
    "¿Cuándo es el mejor momento para aplicar herbicida en soja en la zona núcleo?",
    "Los rindes de trigo están siendo muy bajos esta campaña, ¿puede ser por la sequía?",
    "Necesito saber si conviene hacer un análisis de suelo antes de la siembra."
]

# ChromaDB convierte automáticamente cada consulta en vectores
collection.add(
    documents=consultas_productores,
    metadatas=[{"region": "zona-nucleo"}, {"region": "zona-nucleo"}, {"region": "pampa-humeda"}, {"region": "general"}],
    ids=["consulta1", "consulta2", "consulta3", "consulta4"],
)

print("Cantidad de consultas:", collection.count())
print("Consultas guardadas:", collection.get())
print("Consultas guardadas 2:", collection.get('doc2'))

""" Respuesta """

# Cantidad de consultas: 4
# Consultas guardadas: {'ids': ['consulta1', 'consulta2', 'consulta3', 'consulta4'], 'embeddings': None, 'documents': ['Mi maíz tiene las hojas amarillas y no sé si es falta 
# de nitrógeno o exceso de agua.', '¿Cuándo es el mejor momento para aplicar herbicida en soja en la zona núcleo?', 'Los rindes de trigo están siendo muy bajos esta campaña, 
# ¿puede ser por la sequía?', 'Necesito saber si conviene hacer un análisis de suelo antes de la siembra.'], 'uris': None, 'included': ['metadatas', 'documents'], 'data': None, 'metadatas': [{'region': 'zona-nucleo'}, {'region': 'zona-nucleo'}, {'region': 'pampa-humeda'}, {'region': 'general'}]}
# Consultas guardadas 2: {'ids': [], 'embeddings': None, 'documents': [], 'uris': None, 
# 'included': ['metadatas', 'documents'], 'data': None, 'metadatas': []}


# Búsqueda inteligente: encuentra consultas similares por significado
pregunta_nueva = "Mi trigo está rindiendo poco, ¿será por falta de lluvia?"

results = collection.query(
    query_texts=[pregunta_nueva],
    n_results=3,
)

print("CONSULTA:", pregunta_nueva)
print("\nCONSULTAS SIMILARES ENCONTRADAS:")
for i, doc in enumerate(results['documents'][0]):
    print(f"{i+1}. {doc}")

results

""" Respuesta """

# CONSULTA: Mi trigo está rindiendo poco, ¿será por falta de lluvia?

# CONSULTAS SIMILARES ENCONTRADAS:
# 1. Los rindes de trigo están siendo muy bajos esta campaña, ¿puede ser por la sequía? 
# 2. Mi maíz tiene las hojas amarillas y no sé si es falta de nitrógeno o exceso de agua.
# 3. ¿Cuándo es el mejor momento para aplicar herbicida en soja en la zona núcleo?  


collection.get(where_document={"$contains": "trigo"})

"""### 4. Agregar más consultas de productores

Simulemos que llegan más consultas técnicas y veamos cómo mejora nuestro sistema."""

nuevas_consultas = [
    "La soja está con hojas amarillentas, puede ser deficiencia nutricional?",
    "En qué momento del cultivo de maíz es mejor aplicar los agroquímicos?",
    "Este año mi cosecha de trigo fue muy mala, creo que fue por la falta de precipitaciones.",
    "¿Vale la pena hacer estudios de tierra antes de plantar?",
    "El maíz no está creciendo bien, las hojas se ven pálidas, ¿puede ser falta de fertilizante?"
]

def preparar_nuevas_consultas(consultas, region, cantidad_actual):
    """Función para organizar las nuevas consultas antes de guardarlas"""
    metadatos = [{"region": region} for _ in consultas]
    nuevos_ids = [f"consulta{cantidad_actual + i + 1}" for i in range(len(consultas))]

    return {
        "documents": consultas,
        "metadatas": metadatos,
        "ids": nuevos_ids
    }


cantidad_actual = collection.count()
print(cantidad_actual)

nuevas_organizadas = preparar_nuevas_consultas(
    nuevas_consultas, "pampa-humeda", cantidad_actual
)

result = collection.add(**nuevas_organizadas)
print("Resultado de la adición:", result)

todos_los_docs = collection.get()
print("Todos los documentos:", todos_los_docs)


""" Respuesta """

# Resultado de la adición: None
# Todos los documentos: {'ids': ['consulta1', 'consulta2', 'consulta3', 'consulta4', 'consulta5', 'consulta6', 'consulta7', 'consulta8', 'consulta9'], 'embeddings': None, 'documents': ['Mi maíz tiene las hojas amarillas y no sé si es falta de nitrógeno o exceso de agua.', '¿Cuándo es el mejor momento para aplicar herbicida en soja en la zona núcleo?', 'Los rindes de trigo están siendo muy bajos esta campaña, ¿puede ser por la sequía?', 'Necesito saber si conviene hacer un análisis de suelo antes de la siembra.', 
# 'La soja está con hojas amarillentas, puede ser deficiencia nutricional?', 'En qué momento del cultivo de maíz es mejor aplicar los agroquímicos?', 'Este año mi cosecha de 
# trigo fue muy mala, creo que fue por la falta de precipitaciones.', '¿Vale la pena hacer estudios de tierra antes de plantar?', 'El maíz no está creciendo bien, las hojas se ven pálidas, ¿puede ser falta de fertilizante?'], 'uris': None, 'included': ['metadatas', 'documents'], 'data': None, 'metadatas': [{'region': 'zona-nucleo'}, {'region': 
# 'zona-nucleo'}, {'region': 'pampa-humeda'}, {'region': 'general'}, {'region': 'pampa-humeda'}, {'region': 'pampa-humeda'}, {'region': 'pampa-humeda'}, {'region': 'pampa-humeda'}, {'region': 'pampa-humeda'}]} 

pregunta_nueva = "Mi cultivo tiene problemas de nutrición, las plantas se ven débiles"

results = collection.query(
    query_texts=[pregunta_nueva],
    n_results=3
)

print("NUEVA CONSULTA:", pregunta_nueva)
print("\nCONSULTAS SIMILARES ENCONTRADAS:")
for i, doc in enumerate(results['documents'][0]):
    print(f"{i+1}. {doc}")

print("\n--- RESULTADOS COMPLETOS ---")
print(results)

print("BÚSQUEDA POR PALABRAS EXACTAS:")
# Buscamos por palabras específicas
where_document={"$or": [{"$contains": "nutrición"}, {"$contains": "fertilizante"}]}

print(collection.get(where_document=where_document))

""" Respuesta """

# --- RESULTADOS COMPLETOS ---
# {'ids': [['consulta5', 'consulta6', 'consulta1']], 'embeddings': None, 'documents': [['La soja está con hojas amarillentas, puede ser deficiencia nutricional?', 'En qué momento del cultivo de maíz es mejor aplicar los agroquímicos?', 'Mi maíz tiene las hojas amarillas y no sé si es falta de nitrógeno o exceso de agua.']], 'uris': None, 'included': ['metadatas', 'documents', 'distances'], 'data': None, 'metadatas': [[{'region': 'pampa-humeda'}, {'region': 'pampa-humeda'}, {'region': 'zona-nucleo'}]], 'distances': [[0.6771029233932495, 0.8585242033004761, 0.8751293420791626]]}
# BÚSQUEDA POR PALABRAS EXACTAS:
# {'ids': ['consulta9'], 'embeddings': None, 'documents': ['El maíz no está creciendo bien, las hojas se ven pálidas, ¿puede ser falta de fertilizante?'], 'uris': None, 'included': ['metadatas', 'documents'], 'data': None, 'metadatas': [{'region': 'pampa-humeda'}]}

"""### 5. Modelo de Embeddings Multilenguaje

El modelo `multilingual-e5-large` entiende 94 idiomas diferentes, incluido 
el español y sus variantes técnicas. Esto significa que podrá 
entender mejor términos como "sequía", "rinde", "siembra", etc."""


collection_mejorada = client.get_or_create_collection(
    "ConsultasAgricolasMultilenguaje",
    embedding_function=modelo_multilenguaje,
    metadata={"hnsw:space": "cosine"}  # Mejor métrica para comparar significados
)

print(client.list_collections())

# Cargamos todas las consultas en la nueva colección mejorada
collection_mejorada.add(
    documents=consultas_productores,
    metadatas=[{"region": "zona-nucleo"}, {"region": "zona-nucleo"}, {"region": "pampa-humeda"}, {"region": "general"}],
    ids=["consulta1", "consulta2", "consulta3", "consulta4"],
)

collection_mejorada.add(
    documents=nuevas_consultas,
    metadatas=[{"region": "pampa-humeda"}, {"region": "pampa-humeda"}, {"region": "pampa-humeda"}, {"region": "pampa-humeda"}, {"region": "pampa-humeda"}],
    ids=["consulta5", "consulta6", "consulta7", "consulta8", "consulta9"],
)

print(client.list_collections())

pregunta_test = "Mi cultivo no está creciendo bien, puede ser falta de fertilización?"

results = collection_mejorada.query(
    query_texts=[pregunta_test],
    n_results=3
)

print("CONSULTA DE PRUEBA:", pregunta_test)
print("\nCONSULTAS MÁS SIMILARES:")
for i, doc in enumerate(results['documents'][0]):
    print(f"{i+1}. {doc}")

print(results)

""" Respuesta """

# [Collection(name=ConsultasAgricolas), Collection(name=ConsultasAgricolasMultilenguaje)]
# [Collection(name=ConsultasAgricolas), Collection(name=ConsultasAgricolasMultilenguaje)]
# CONSULTA DE PRUEBA: Mi cultivo no está creciendo bien, puede ser falta de fertilización?

# CONSULTAS MÁS SIMILARES:
# 1. El maíz no está creciendo bien, las hojas se ven pálidas, ¿puede ser falta de fertilizante?
# 2. La soja está con hojas amarillentas, puede ser deficiencia nutricional?
# 3. Los rindes de trigo están siendo muy bajos esta campaña, ¿puede ser por la sequía? 
# {'ids': [['consulta9', 'consulta5', 'consulta3']], 'embeddings': None, 'documents': [['El maíz no está creciendo bien, las hojas se ven pálidas, ¿puede ser falta de fertilizante?', 'La soja está con hojas amarillentas, puede ser deficiencia nutricional?', 'Los rindes de trigo están siendo muy bajos esta campaña, ¿puede ser por la sequía?']], 
# 'uris': None, 'included': ['metadatas', 'documents', 'distances'], 'data': None, 'metadatas': [[{'region': 'pampa-humeda'}, {'region': 'pampa-humeda'}, {'region': 'pampa-humeda'}]], 'distances': [[0.0603029727935791, 0.10883581638336182, 0.1181328296661377]]}

# Para la próxima clase: ejemplo simple de cómo será RAG

def ejemplo_rag_simple(consulta_productor):
    """Esta función muestra cómo funcionará RAG completo la próxima semana"""

    print("=== SIMULACIÓN RAG ===")
    print(f"Consulta del productor: {consulta_productor}")

    # PASO 1: RECUPERAR (lo que ya sabemos hacer)
    print("\n1. RECUPERANDO información similar...")
    results = collection_mejorada.query(
        query_texts=[consulta_productor],
        n_results=2
    )

    contexto = results['documents'][0]
    print(f"Consultas similares encontradas: {len(contexto)}")
    for i, doc in enumerate(contexto):
        print(f"   - {doc}")

    # PASO 2: GENERAR (próxima semana aprenderemos esto)
    print("\n2. GENERANDO respuesta personalizada...")
    print("   (Próxima clase: usaremos OpenAI/Claude con este contexto)")
    print("   Respuesta automática basada en casos similares")

    return contexto

# Probemos el concepto
ejemplo_rag_simple("¿Cuándo debo aplicar fertilizante a mi cultivo de maíz?")

""" Respuesta """

# === SIMULACIÓN RAG ===
# Consulta del productor: ¿Cuándo debo aplicar fertilizante a mi cultivo de maíz?       

# 1. RECUPERANDO información similar...
# Consultas similares encontradas: 2
#    - En qué momento del cultivo de maíz es mejor aplicar los agroquímicos?
#    - El maíz no está creciendo bien, las hojas se ven pálidas, ¿puede ser falta de fertilizante?

# 2. GENERANDO respuesta personalizada...
#    (Próxima clase: usaremos OpenAI/Claude con este contexto)
#    Respuesta automática basada en casos similares