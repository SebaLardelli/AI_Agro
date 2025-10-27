"""
Utilidades de Imagen
====================

Funciones de procesamiento de imagen extraídas del analizador_agricola.py original.
"""

import os
import io
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

from PIL import Image, ImageDraw


def generar_imagen_bbox(imagen_pil: Image.Image, detecciones: List[Dict[str, Any]], output_dir: str = "./output") -> str:
    """
    Dibuja bounding boxes rojas con la etiqueta arriba.
    Guarda ./output/debug_<timestamp>.jpg
    Coords Gemini vienen en [y1,x1,y2,x2] con rango 0..1000 relativo.
    """
    
    # Crear directorio si no existe
    os.makedirs(output_dir, exist_ok=True)
    
    draw_img = imagen_pil.copy()
    draw = ImageDraw.Draw(draw_img)

    W, H = draw_img.size

    for det in detecciones:
        box = det.get("box_2d", None)
        label = det.get("label", "objeto")

        if not box or len(box) != 4:
            continue

        y1n, x1n, y2n, x2n = box  # y1,x1,y2,x2 en 0..1000

        x1 = int((x1n / 1000.0) * W)
        y1 = int((y1n / 1000.0) * H)
        x2 = int((x2n / 1000.0) * W)
        y2 = int((y2n / 1000.0) * H)

        # caja
        draw.rectangle([x1, y1, x2, y2], outline="red", width=2)

        # etiqueta sobre la caja
        txt = f"{label}"[:40]
        draw.rectangle(
            [x1, y1 - 14, x1 + (len(txt) * 6), y1],
            fill="red"
        )
        draw.text((x1 + 2, y1 - 12), txt, fill="white")

    ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    out_path = Path(output_dir) / f"debug_{ts}.jpg"
    draw_img.save(out_path, format="JPEG", quality=90)

    return str(out_path)