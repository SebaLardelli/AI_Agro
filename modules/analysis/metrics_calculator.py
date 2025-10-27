"""
Módulo de Análisis y Métricas
==============================

Funciones de análisis extraídas del analizador_agricola.py original.
"""

from collections import defaultdict, Counter
from datetime import datetime
from typing import List, Dict, Any, Tuple


def calcular_metricas(detecciones: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Recorre detecciones con claves esperadas:
      - categoria ∈ {"grano","plaga","fauna_riesgo","hongo","maleza"}
      - especie   (p.ej. "maiz","soja","trigo","paloma","rata","gorgojo"...)
      - estado_grano ∈ {"sano","roto","moho"} (sólo cuando categoria == "grano")

    Devuelve métricas agregadas listas para UI/Agente:
      - conteos por especie/estado
      - % grano con moho
      - flags sanitarios
      - tipo_imagen inferido
    """
    
    # ---- Helpers
    def norm_str(x: Any) -> str:
        return str(x).strip().lower() if x is not None else ""

    # ---- Acumuladores
    granos_por_especie: Dict[str, Dict[str, int]] = defaultdict(lambda: {"sano": 0, "roto": 0, "moho": 0})
    especies_counter = Counter()
    categorias_counter = Counter()

    total_granos = 0
    total_granos_moho = 0
    total_plaga = 0
    total_fauna = 0
    total_hongo = 0
    total_maleza = 0

    # ---- Loop principal (tolerante a faltantes)
    for det in detecciones or []:
        cat = norm_str(det.get("categoria"))
        esp = norm_str(det.get("especie"))
        est = norm_str(det.get("estado_grano"))

        if cat:
            categorias_counter[cat] += 1

        if cat == "grano":
            total_granos += 1
            if esp:
                especies_counter[esp] += 1

            if est in ("sano", "roto", "moho"):
                granos_por_especie[esp][est] += 1
                if est == "moho":
                    total_granos_moho += 1
            else:
                # si no hay estado, lo contamos como sano (decisión conservadora)
                granos_por_especie[esp]["sano"] += 1

        elif cat == "plaga":
            total_plaga += 1
            if esp:
                especies_counter[esp] += 1

        elif cat == "fauna_riesgo":
            total_fauna += 1
            if esp:
                especies_counter[esp] += 1

        elif cat == "hongo":
            total_hongo += 1
            if esp:
                especies_counter[esp] += 1

        elif cat == "maleza":
            total_maleza += 1
            if esp:
                especies_counter[esp] += 1

    # ---- Derivados
    porc_grano_infectado = round((total_granos_moho / total_granos) * 100.0, 2) if total_granos else 0.0

    # Heurística simple para tipo de imagen
    # (prioriza fauna > granos > maleza; si no hay nada -> desconocido)
    if total_fauna > 0:
        tipo_imagen = "fauna_en_muestra"
    elif total_granos > 0:
        tipo_imagen = "muestra_granos"
    elif total_maleza > 0:
        tipo_imagen = "lote_con_maleza"
    elif total_hongo > 0:
        tipo_imagen = "muestra_hongos"
    else:
        tipo_imagen = "desconocido"

    # Nivel de riesgo
    riesgo_sanitario, riesgo_comercial = nivel_riesgo(
        total_plaga,
        total_fauna,
        porc_grano_infectado,
    )

    # Top especies detectadas (útil para UI y prompts)
    top_especies = especies_counter.most_common(5)

    metricas: Dict[str, Any] = {
        # resumen general
        "total_objetos": sum(categorias_counter.values()),
        "categorias_detectadas": dict(categorias_counter),

        # grano
        "tipo_imagen": tipo_imagen,
        "total_granos": total_granos,
        "granos_por_especie": dict(granos_por_especie),  # defaultdict -> dict
        "porcentaje_grano_con_moho": porc_grano_infectado,

        # riesgo/flags
        "plagas_detectadas": total_plaga,
        "fauna_riesgo_detectada": total_fauna,
        "hongos_detectados_sueltos": total_hongo,
        "maleza_detectada": total_maleza,
        "riesgo_sanitario": riesgo_sanitario,
        "riesgo_comercial": riesgo_comercial,

        # extras útiles
        "especies_top5": top_especies,  # [(especie, conteo), ...]
        "tiene_plaga_viva": total_plaga > 0,
        "tiene_fauna_grande": total_fauna > 0,
        "tiene_hongo_suelto": total_hongo > 0,
        "tiene_maleza": total_maleza > 0,
    }

    return metricas


def nivel_riesgo(total_plaga: int, total_roedor_ave: int, porc_grano_infectado: float) -> Tuple[str, str]:
    """
    Define riesgo_sanitario y riesgo_comercial como texto.
    """
    # Sanitario alto si hay roedores/aves o mucho moho
    if total_roedor_ave > 0 or porc_grano_infectado >= 5.0:
        riesgo_sanitario = "ALTO"
    elif total_plaga > 0 or porc_grano_infectado > 0:
        riesgo_sanitario = "MEDIO"
    else:
        riesgo_sanitario = "BAJO"

    # Comercial comprometido si hay moho significativo
    if porc_grano_infectado >= 5.0:
        riesgo_comercial = "COMPROMETIDO"
    else:
        riesgo_comercial = "ACEPTABLE"

    return riesgo_sanitario, riesgo_comercial


def armar_diagnostico(metricas: Dict[str, Any]) -> str:
    """
    Diagnóstico técnico de control: números + riesgo + acción.
    """

    partes = []

    # contexto general
    if metricas["tipo_imagen"] == "fauna_en_muestra":
        partes.append(
            "Se detectó presencia de fauna contaminante (roedor/ave) en contacto con el material."
        )
    elif metricas["tipo_imagen"] == "muestra_granos":
        partes.append(
            "La imagen corresponde a una muestra de granos/semillas."
        )
    elif metricas["tipo_imagen"] == "lote_con_maleza":
        partes.append(
            "Se observó vegetación/maleza no correspondiente al cultivo objetivo."
        )
    else:
        partes.append(
            "No se pudo determinar claramente el tipo de muestra."
        )

    # resumen granos
    partes.append(
        f"Total de granos detectados: {metricas['total_granos']}."
    )

    if metricas["granos_por_especie"]:
        partes.append("Detalle por especie:")
        for especie, estados in metricas["granos_por_especie"].items():
            sano = estados["sano"]
            roto = estados["roto"]
            moho = estados["moho"]
            partes.append(
                f" - {especie}: sano={sano}, roto/quebrado={roto}, con moho/pudrición={moho}."
            )

    # contaminantes
    if metricas["plagas_detectadas"] > 0:
        partes.append(
            f"Plagas/insectos detectados: {metricas['plagas_detectadas']} objeto(s)."
        )
    if metricas["fauna_riesgo_detectada"] > 0:
        partes.append(
            f"Fauna de riesgo (roedor/paloma/ave) detectada: {metricas['fauna_riesgo_detectada']} objeto(s)."
        )
    if metricas["hongos_detectados_sueltos"] > 0:
        partes.append(
            f"Áreas con posible hongo/moho independientes: {metricas['hongos_detectados_sueltos']}."
        )
    if metricas["maleza_detectada"] > 0:
        partes.append(
            f"Maleza/material vegetal extraño detectado: {metricas['maleza_detectada']}."
        )

    # riesgo
    partes.append(
        f"Riesgo sanitario: {metricas['riesgo_sanitario']}. "
        f"Riesgo comercial: {metricas['riesgo_comercial']}."
    )

    partes.append(
        "Porcentaje de granos con moho/hongo visible: "
        f"{metricas['porcentaje_grano_con_moho']}%."
    )

    # recomendación inmediata
    if metricas["riesgo_sanitario"] == "ALTO":
        partes.append(
            "Acción recomendada: separar la partida, no mezclar con stock sano, "
            "revisar condiciones de almacenamiento y vectores (aves/roedores)."
        )
    elif metricas["riesgo_sanitario"] == "MEDIO":
        partes.append(
            "Acción recomendada: monitorear evolución de moho y controlar plagas."
        )
    else:
        partes.append(
            "Acción recomendada: seguir controlando sin urgencia inmediata."
        )

    return "\n".join(partes)


def armar_data_momento(metricas: Dict[str, Any]) -> Dict[str, Any]:
    """
    Payload estructurado que después vos mandás al agente RAG / mensaje Telegram.
    Agregamos hallazgos_clave para que el agente pueda armar la explicación natural.
    """

    hallazgos = []

    # moho?
    if metricas["porcentaje_grano_con_moho"] > 0:
        hallazgos.append("presencia de moho/pudrición en granos")

    # plaga?
    if metricas["plagas_detectadas"] > 0:
        hallazgos.append("plaga viva (gusano/larva/insecto) activa")

    # roedor/ave?
    if metricas["fauna_riesgo_detectada"] > 0:
        hallazgos.append("contacto con fauna contaminante (roedor/ave)")

    # maleza?
    if metricas["maleza_detectada"] > 0:
        hallazgos.append("material vegetal extraño / maleza en la muestra")

    if not hallazgos:
        hallazgos.append("sin contaminantes críticos visibles")

    return {
        "tipo_imagen": metricas["tipo_imagen"],
        "riesgo_sanitario": metricas["riesgo_sanitario"],
        "riesgo_comercial": metricas["riesgo_comercial"],
        "total_granos": metricas["total_granos"],
        "porcentaje_grano_con_moho": metricas["porcentaje_grano_con_moho"],
        "granos_por_especie": metricas["granos_por_especie"],
        "contaminacion": {
            "plagas_insectos": metricas["plagas_detectadas"],
            "fauna_riesgo_roedor_ave": metricas["fauna_riesgo_detectada"],
            "hongos_areas_sueltas": metricas["hongos_detectados_sueltos"],
            "maleza": metricas["maleza_detectada"],
        },
        "hallazgos_clave": hallazgos,
        "timestamp_captura": datetime.now().isoformat()
    }