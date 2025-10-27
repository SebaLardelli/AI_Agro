#!/usr/bin/env python3
"""
analizador_agricola_modular.py

Analizador visual agrícola MODULARIZADO para control de calidad de granos / semillas.
Mantiene exactamente la misma interfaz que el original pero organizado en módulos.

Funcionalidad idéntica al original:
- Detecta especie del grano (maíz, sorgo, arroz, trigo pan, soja, cebada, centeno, avena, girasol, poroto, colza, maní).
- Detecta el estado del grano (sano, roto/quebrado, moho/pudrición).
- Detecta plagas vivas chicas (gusano, larva, gorgojo, insecto, polilla).
- Detecta fauna contaminante grande (rata, ratón, paloma, ave).
- Detecta hongos / moho / pudrición.
- Detecta maleza (material vegetal extraño).

Devuelve:
- Bounding boxes por objeto (cada gusano separado del maíz).
- Métricas cuantitativas por especie y estado.
- Diagnóstico técnico corto (riesgo sanitario / comercial).
- Diagnóstico agronómico global en español argentino (causa + impacto).
- Imagen debug con bounding boxes.

Arquitectura modular:
- modules/detection/gemini_detector.py: Detección con Gemini
- modules/analysis/metrics_calculator.py: Cálculo de métricas y diagnósticos
- modules/utils/: Utilidades (validación, geometría, imagen)
"""

import os
import io
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

from PIL import Image, ImageDraw

# Importar módulos
try:
    from modules.detection.gemini_detector import GeminiDetector
    from modules.analysis.metrics_calculator import (
        calcular_metricas, 
        armar_diagnostico, 
        armar_data_momento
    )
    from modules.utils.image_utils import generar_imagen_bbox
    from modules.utils.geometry import fusionar_granos, nms_by_label
    MODULES_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Módulos no disponibles: {e}")
    MODULES_AVAILABLE = False


class AnalizadorAgricola:
    """
    Analizador agrícola modularizado.
    Mantiene exactamente la misma interfaz que el original.
    """
    
    def __init__(self):
        """Inicializa el analizador con la misma lógica que el original"""
        if MODULES_AVAILABLE:
            self.detector = GeminiDetector()
            self.gemini_disponible = self.detector.gemini_disponible
            self.cliente = self.detector.cliente
        else:
            # Fallback al comportamiento original si los módulos no están disponibles
            self.gemini_disponible = False
            self.cliente = None
            print("⚠️ Usando modo fallback (módulos no disponibles)")

        # Carpeta salida debug (igual que el original)
        self.output_dir = Path("./output")
        self.output_dir.mkdir(exist_ok=True)

    # ==========================================================
    #   FUNCIÓN PRINCIPAL: esto es lo que llama Flask
    # ==========================================================

    def analizar_imagen(self, imagen_bytes: bytes) -> Dict[str, Any]:
        """
        Función principal idéntica al original.
        - Llama detección espacial granular
        - Filtro/confianza + firewall + fusión de cajas
        - Zoom local para plagas
        - Dibuja bounding boxes
        - Calcula métricas
        - Genera diagnóstico técnico y diagnóstico agronómico global
        - Devuelve payload para que n8n lo mande al agente
        """

        # 1. abrir imagen y reducir tamaño (igual que el original)
        img = Image.open(io.BytesIO(imagen_bytes)).convert("RGB")
        img.thumbnail([1024, 1024], Image.Resampling.LANCZOS)
        W, H = img.size

        # 2. detección espacial con Gemini (cajas)
        detecciones = []
        if self.gemini_disponible and MODULES_AVAILABLE:
            try:
                detecciones = self.detector.detectar_con_gemini(img)
            except Exception as e:
                print(f"⚠️ Error en Gemini (spatial): {e}")
        else:
            print("⚠️ Gemini no disponible, detecciones vacías.")

        # 2.1 Zoom de refuerzo: buscar larvas/gusanos en zonas con moho
        try:
            sospechosas = [
                d for d in detecciones
                if (
                    d["categoria"] == "grano"
                    and d.get("estado_grano") == "moho"
                )
                or d["categoria"] == "hongo"
                or ("moho" in d["label"].lower() or "pudric" in d["label"].lower())
            ]
            if sospechosas and self.gemini_disponible and MODULES_AVAILABLE:
                plagas_extra = self.detector.second_pass_plagas(img, sospechosas)
                if plagas_extra:
                    # combinar detecciones base + nuevas plagas y filtrar duplicados
                    detecciones = nms_by_label(detecciones + plagas_extra, iou_thr=0.6)
        except Exception as e:
            print(f"⚠️ Error en second-pass plagas: {e}")

        # 2.2 Fusión de granos contiguos (reduce spam de cajitas)
        try:
            if MODULES_AVAILABLE:
                detecciones = fusionar_granos(detecciones, iou_thr=0.5)
        except Exception as e:
            print(f"⚠️ Error fusionar_granos: {e}")

        # 3. imagen debug con bounding boxes
        if MODULES_AVAILABLE:
            bbox_path = generar_imagen_bbox(img, detecciones, str(self.output_dir))
        else:
            bbox_path = self._generar_imagen_bbox_fallback(img, detecciones)

        # 4. métricas cuantitativas
        if MODULES_AVAILABLE:
            metricas = calcular_metricas(detecciones)
        else:
            metricas = self._calcular_metricas_fallback(detecciones)

        # 5. diagnóstico técnico resumido
        if MODULES_AVAILABLE:
            diagnostico_texto = armar_diagnostico(metricas)
        else:
            diagnostico_texto = self._armar_diagnostico_fallback(metricas)

        # 6. diagnóstico agronómico global estilo "Gemini común" en ESPAÑOL ARG
        if MODULES_AVAILABLE and self.gemini_disponible:
            diagnostico_global = self.detector.analisis_agronomico_global(img)
        else:
            diagnostico_global = self._analisis_agronomico_global_fallback(img)

        # 7. bloque estructurado para el agente (con hallazgos_clave)
        if MODULES_AVAILABLE:
            data_momento = armar_data_momento(metricas)
        else:
            data_momento = self._armar_data_momento_fallback(metricas)

        return {
            "timestamp": datetime.now().isoformat(),
            "tipo_imagen": metricas.get("tipo_imagen", "desconocido"),
            "objetos_detectados": detecciones,
            "metricas": metricas,
            "diagnostico_texto": diagnostico_texto,
            "diagnostico_global": diagnostico_global,
            "data_momento": data_momento,
            "imagen_bbox_path": bbox_path,
        }

    # ==========================================================
    #   MÉTODOS FALLBACK (para cuando los módulos no están disponibles)
    # ==========================================================

    def _generar_imagen_bbox_fallback(self, imagen_pil: Image.Image, detecciones: List[Dict[str, Any]]) -> str:
        """Fallback para generar imagen debug"""
        draw_img = imagen_pil.copy()
        draw = ImageDraw.Draw(draw_img)
        W, H = draw_img.size

        for det in detecciones:
            box = det.get("box_2d", None)
            label = det.get("label", "objeto")
            if not box or len(box) != 4:
                continue

            y1n, x1n, y2n, x2n = box
            x1 = int((x1n / 1000.0) * W)
            y1 = int((y1n / 1000.0) * H)
            x2 = int((x2n / 1000.0) * W)
            y2 = int((y2n / 1000.0) * H)

            draw.rectangle([x1, y1, x2, y2], outline="red", width=2)
            txt = f"{label}"[:40]
            draw.rectangle([x1, y1 - 14, x1 + (len(txt) * 6), y1], fill="red")
            draw.text((x1 + 2, y1 - 12), txt, fill="white")

        ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        out_path = self.output_dir / f"debug_{ts}.jpg"
        draw_img.save(out_path, format="JPEG", quality=90)
        return str(out_path)

    def _calcular_metricas_fallback(self, detecciones: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Fallback para calcular métricas"""
        return {
            "total_objetos": len(detecciones),
            "categorias_detectadas": {},
            "tipo_imagen": "fallback",
            "total_granos": 0,
            "granos_por_especie": {},
            "porcentaje_grano_con_moho": 0.0,
            "plagas_detectadas": 0,
            "fauna_riesgo_detectada": 0,
            "hongos_detectados_sueltos": 0,
            "maleza_detectada": 0,
            "riesgo_sanitario": "DESCONOCIDO",
            "riesgo_comercial": "DESCONOCIDO",
            "especies_top5": [],
            "tiene_plaga_viva": False,
            "tiene_fauna_grande": False,
            "tiene_hongo_suelto": False,
            "tiene_maleza": False,
        }

    def _armar_diagnostico_fallback(self, metricas: Dict[str, Any]) -> str:
        """Fallback para diagnóstico técnico"""
        return "Análisis en modo fallback - módulos no disponibles"

    def _analisis_agronomico_global_fallback(self, imagen_pil: Image.Image) -> str:
        """Fallback para análisis agronómico"""
        return "No se pudo generar análisis global (módulos no disponibles)"

    def _armar_data_momento_fallback(self, metricas: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback para data momento"""
        return {
            "tipo_imagen": "fallback",
            "riesgo_sanitario": "DESCONOCIDO",
            "riesgo_comercial": "DESCONOCIDO",
            "total_granos": 0,
            "porcentaje_grano_con_moho": 0.0,
            "granos_por_especie": {},
            "contaminacion": {
                "plagas_insectos": 0,
                "fauna_riesgo_roedor_ave": 0,
                "hongos_areas_sueltas": 0,
                "maleza": 0,
            },
            "hallazgos_clave": ["análisis en modo fallback"],
            "timestamp_captura": datetime.now().isoformat()
        }


# Función de compatibilidad para el código existente
def create_analizador() -> AnalizadorAgricola:
    """Crea una instancia del analizador (para compatibilidad)"""
    return AnalizadorAgricola()


if __name__ == "__main__":
    # Prueba básica del analizador
    print("🧪 Probando Analizador Agrícola Modularizado...")
    
    analizador = AnalizadorAgricola()
    
    print(f"✅ Analizador inicializado")
    print(f"   - Módulos disponibles: {'✅' if MODULES_AVAILABLE else '❌'}")
    print(f"   - Gemini disponible: {'✅' if analizador.gemini_disponible else '❌'}")
    
    print("✅ Prueba completada")
