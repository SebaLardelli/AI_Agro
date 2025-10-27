"""
Utilidades de Validación
========================

Funciones de validación extraídas del analizador_agricola.py original.
"""

# Constantes del código original
ESPECIES_VALIDAS = {
    "maíz", "maiz",
    "sorgo",
    "arroz",
    "trigo",
    "soja",
    "cebada",
    "centeno",
    "avena",
    "girasol",
    "poroto",
    "colza",
    "maní", "mani"
}

PALABRAS_EXTRA_VALIDAS = [
    "gusano", "larva", "gorgojo", "insecto", "polilla",
    "rata", "ratón", "raton", "paloma", "ave",
    "moho", "pudrición", "hongo", "maleza",
    "pudricion", "hongos", "pudricion fungica",
    "pudrición fúngica", "hongo superficial", "moho en grano"
]


def label_valida(label_str: str) -> bool:
    """
    Firewall: sólo dejamos pasar cosas que:
    - mencionan especies válidas O
    - son plagas/fauna/moho/maleza.
    También evita inventos tipo 'Granos masivos 80' que no sirven.
    """
    l = label_str.lower()
    # ¿contiene especie válida?
    for esp in ESPECIES_VALIDAS:
        if esp in l:
            return True
    # ¿contiene palabra clave aceptada?
    for palabra in PALABRAS_EXTRA_VALIDAS:
        if palabra in l:
            return True
    return False


def clasificar_label(label: str):
    """
    Ej:
    "maíz con moho" -> categoria="grano", especie="maiz", estado="moho"
    "gusano"        -> categoria="plaga", especie=None, estado=None
    "paloma"        -> categoria="fauna_riesgo", especie=None, estado=None
    "moho en grano" -> categoria="hongo", especie=None, estado=None
    """
    
    # Mapeo de especies del código original
    map_especie = {
        "maíz": "maiz", "maiz": "maiz", "corn": "maiz",
        "sorgo": "sorgo", "sorghum": "sorgo",
        "arroz": "arroz", "rice": "arroz",
        "trigo": "trigo", "trigo pan": "trigo", "wheat": "trigo",
        "soja": "soja", "soybean": "soja", "soy": "soja",
        "cebada": "cebada", "barley": "cebada",
        "centeno": "centeno", "rye": "centeno",
        "avena": "avena", "oat": "avena", "oats": "avena",
        "girasol": "girasol", "sunflower": "girasol",
        "poroto": "poroto", "bean": "poroto",
        "colza": "colza", "canola": "colza", "rapeseed": "colza",
        "maní": "mani", "mani": "mani", "peanut": "mani",
    }

    # Palabras clave para estado del grano
    estado_palabras = {
        "sano": [
            "sano", "entero", "normal", "intacto", "bueno", "comercial"
        ],
        "roto": [
            "roto", "quebrado", "fracturado", "partido"
        ],
        "moho": [
            "moho", "mohoso", "fungal", "hongo", "pudrido",
            "pudrición", "pudricion", "podrido", "descomposición", "descompuesto"
        ],
    }

    # Plaga chica: insectos / larvas / gusanos que comen grano
    key_plaga = [
        "gusano", "larva", "gorgojo", "insecto", "polilla",
        "beetle", "weevil", "moth", "bug", "plaga"
    ]

    # Fauna grande contaminante: roedor / ave de silo
    key_fauna_riesgo = [
        "rata", "ratón", "raton", "mouse", "rat",
        "paloma", "pájaro", "ave", "bird", "pigeon"
    ]

    # Hongos / moho
    key_hongo = [
        "hongo", "fungus", "moho", "mold", "pudrición",
        "pudricion", "rot", "descomposición", "decomposition", "podrido"
    ]

    # Maleza
    key_maleza = [
        "maleza", "yuyo", "weed"
    ]

    l = label.lower()

    # especie de grano
    especie_detectada = None
    for palabra, especie_canon in map_especie.items():
        if palabra in l:
            especie_detectada = especie_canon
            break

    # estado del grano
    estado_detectado = None
    for estado, keywords in estado_palabras.items():
        if any(k in l for k in keywords):
            estado_detectado = estado
            break

    # categoría general
    if especie_detectada is not None:
        categoria = "grano"
    elif any(k in l for k in key_plaga):
        categoria = "plaga"
    elif any(k in l for k in key_fauna_riesgo):
        categoria = "fauna_riesgo"
    elif any(k in l for k in key_hongo):
        categoria = "hongo"
    elif any(k in l for k in key_maleza):
        categoria = "maleza"
    else:
        categoria = "otro"

    # si dice hongo y es grano, forzamos estado "moho"
    if especie_detectada and any(k in l for k in key_hongo):
        estado_detectado = "moho"

    return categoria, especie_detectada, estado_detectado
