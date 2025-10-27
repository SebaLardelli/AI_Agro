"""
Utilidades Geométricas
======================

Funciones geométricas extraídas del analizador_agricola.py original.
"""

from typing import List, Dict, Any


def iou_boxes(b1: List[int], b2: List[int]) -> float:
    """
    IOU entre dos cajas en coords normalizadas [y1,x1,y2,x2] (0..1000).
    Devuelve valor entre 0 y 1.
    """
    y1a, x1a, y2a, x2a = b1
    y1b, x1b, y2b, x2b = b2

    inter_x1 = max(x1a, x1b)
    inter_y1 = max(y1a, y1b)
    inter_x2 = min(x2a, x2b)
    inter_y2 = min(y2a, y2b)

    inter_w = max(0, inter_x2 - inter_x1)
    inter_h = max(0, inter_y2 - inter_y1)
    inter_area = inter_w * inter_h

    area_a = max(0, x2a - x1a) * max(0, y2a - y1a)
    area_b = max(0, x2b - x1b) * max(0, y2b - y1b)
    union_area = area_a + area_b - inter_area
    if union_area <= 0:
        return 0.0
    return inter_area / union_area


def merge_boxes(boxes: List[List[int]]) -> List[int]:
    """
    Dada una lista de cajas [y1,x1,y2,x2], devuelve una caja envolvente.
    """
    ys1 = [b[0] for b in boxes]
    xs1 = [b[1] for b in boxes]
    ys2 = [b[2] for b in boxes]
    xs2 = [b[3] for b in boxes]
    return [min(ys1), min(xs1), max(ys2), max(xs2)]


def nms_by_label(dets: List[Dict[str, Any]], iou_thr: float = 0.7) -> List[Dict[str, Any]]:
    """
    Non-Max Suppression simple por etiqueta:
    - Para cada label, quedate con las cajas más confiables y eliminá
      las muy superpuestas.
    """
    resultado = []
    # agrupar por label
    labels = {}
    for d in dets:
        lbl = d.get("label", "desconocido")
        labels.setdefault(lbl, []).append(d)

    for lbl, grupo in labels.items():
        # ordenar por score desc
        grupo_sorted = sorted(grupo, key=lambda x: x.get("score", 0), reverse=True)
        kept = []
        for cand in grupo_sorted:
            keep_it = True
            for prev in kept:
                if iou_boxes(cand["box_2d"], prev["box_2d"]) > iou_thr:
                    keep_it = False
                    break
            if keep_it:
                kept.append(cand)
        resultado.extend(kept)

    return resultado


def fusionar_granos(dets: List[Dict[str, Any]], iou_thr: float = 0.5) -> List[Dict[str, Any]]:
    """
    Une cajas de granos contiguos para reducir spam de mil cajitas.
    Lógica:
    - Filtramos objetos categoria == "grano".
    - Hacemos clusters por solapamiento IOU.
    - Cada cluster se vuelve una sola caja grande.
    - El label final del cluster prioriza el peor estado:
        'maíz con moho' / '... pudrición' gana sobre 'maíz sano'.
    """
    granos = [d for d in dets if d.get("categoria") == "grano"]
    otros  = [d for d in dets if d.get("categoria") != "grano"]

    if not granos:
        return dets  # nada que fusionar

    clusters: List[List[Dict[str, Any]]] = []
    for g in granos:
        asignado = False
        for cluster in clusters:
            # si este grano se solapa con CUALQUIERA del cluster, se mete ahí
            if any(iou_boxes(g["box_2d"], c["box_2d"]) >= iou_thr for c in cluster):
                cluster.append(g)
                asignado = True
                break
        if not asignado:
            clusters.append([g])

    fusionados: List[Dict[str, Any]] = []
    for cluster in clusters:
        # caja merge
        cajas = [c["box_2d"] for c in cluster]
        box_big = merge_boxes(cajas)

        # label final: priorizamos moho/pudrición > roto > sano
        label_candidates = [c["label"].lower() for c in cluster]
        final_label = None
        prioridad = [
            "pudrición", "pudricion", "pudrición fúngica", "pudricion fungica",
            "moho", "hong", "pudri",  # moho/pudrición
            "roto", "quebrado", "fracturado", "partido",
            "sano", "entero", "intacto", "normal"
        ]
        # elegimos la primera palabra de prioridad que aparezca en algún label
        for p in prioridad:
            if any(p in lbl for lbl in label_candidates):
                final_label = p
                break
        # fallback si nada matcheó
        if not final_label:
            final_label = "sano"

        # especie: tomamos la primera especie detectada
        especie_cluster = None
        for c in cluster:
            if c.get("especie"):
                especie_cluster = c["especie"]
                break

        # armamos label humano amigable
        if especie_cluster == "maiz":
            if "moho" in final_label or "pudri" in final_label or "hong" in final_label:
                label_texto = "maíz con moho"
                estado_grano = "moho"
            elif "roto" in final_label or "quebrado" in final_label or "fracturado" in final_label or "partido" in final_label:
                label_texto = "maíz roto"
                estado_grano = "roto"
            else:
                label_texto = "maíz sano"
                estado_grano = "sano"
        else:
            # especie distinta a maíz o desconocida
            if "moho" in final_label or "pudri" in final_label or "hong" in final_label:
                label_texto = f"{especie_cluster or 'grano'} con moho"
                estado_grano = "moho"
            elif "roto" in final_label or "quebrado" in final_label or "fracturado" in final_label or "partido" in final_label:
                label_texto = f"{especie_cluster or 'grano'} roto"
                estado_grano = "roto"
            else:
                label_texto = f"{especie_cluster or 'grano'} sano"
                estado_grano = "sano"

        # score promedio del cluster
        avg_score = sum(c.get("score", 1.0) for c in cluster) / max(1, len(cluster))

        fusionados.append({
            "label": label_texto,
            "categoria": "grano",
            "especie": especie_cluster,
            "estado_grano": estado_grano,
            "box_2d": box_big,
            "score": round(float(avg_score), 3),
            "fuente_modelo": "fusion_cluster"
        })

    # sacar duplicados de fusionados también por NMS
    fusionados = nms_by_label(fusionados, iou_thr=0.7)

    # otros (plagas, hongo suelto, fauna riesgo, maleza) + fusionados
    final_list = fusionados + [o for o in otros]
    # una última pasada de NMS general por etiqueta
    final_list = nms_by_label(final_list, iou_thr=0.7)
    return final_list
