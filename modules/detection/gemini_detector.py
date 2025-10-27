"""
Detector Gemini
===============

Módulo de detección extraído del analizador_agricola.py original.
"""

import os
import json
from typing import List, Dict, Any

from PIL import Image

# Gemini SDK
try:
    from google import genai
    from google.genai import types
    GEMINI_OK = True
except ImportError:
    GEMINI_OK = False

from ..utils.validation import label_valida, clasificar_label
from ..utils.geometry import nms_by_label


class GeminiDetector:
    """Detector de objetos usando Google Gemini Vision"""
    
    def __init__(self):
        self.gemini_disponible = False
        self.cliente = None
        if GEMINI_OK:
            self._configurar_gemini()

    def _configurar_gemini(self):
        """Configura el cliente Gemini usando GOOGLE_API_KEY."""
        api_key = os.getenv("GOOGLE_API_KEY")
        
        # Si no está en variables de entorno, intentar con una API key hardcodeada (solo para testing)
        if not api_key:
            # ⚠️ IMPORTANTE: Reemplaza con tu API key real
            api_key = "TU_API_KEY_AQUI"  # Reemplaza esto con tu API key real
            
        if not api_key or api_key == "TU_API_KEY_AQUI":
            self.gemini_disponible = False
            self.cliente = None
            print("⚠️ GOOGLE_API_KEY no seteada. Gemini deshabilitado.")
            print("💡 Configura la API key en variable de entorno GOOGLE_API_KEY o en el código.")
            return
        try:
            self.cliente = genai.Client(api_key=api_key)
            self.gemini_disponible = True
            print("✅ Gemini configurado")
        except Exception as e:
            print(f"❌ No se pudo inicializar Gemini: {e}")
            self.cliente = None
            self.gemini_disponible = False

    def detectar_con_gemini(self, imagen_pil: Image.Image) -> List[Dict[str, Any]]:
        """
        Pide a Gemini que devuelva SOLO objetos individuales relevantes.
        Cada objeto debe tener su propia caja:
        - el maíz dañado/mohoso es una caja,
        - el gusano es otra caja,
        - la paloma es otra caja, etc.

        Incluye "score" (0..1) por objeto y se filtra por confianza + validez.
        """

        prompt = (
            "Sos inspector de calidad de granos y sanidad postcosecha.\n"
            "Tu trabajo es detectar TODO riesgo visual en la imagen.\n\n"

            "TENÉS QUE DEVOLVER EXCLUSIVAMENTE OBJETOS VISUALES INDIVIDUALES QUE AFECTAN:\n"
            "- Calidad comercial del grano / semilla.\n"
            "- Sanidad / inocuidad (riesgo biológico).\n"
            "- Contaminación (material extraño o contacto de animales).\n\n"

            "⚠ REGLAS CRÍTICAS (SEGUÍ ESTO AL PIE DE LA LETRA):\n"
            "1. CADA OBJETO SE DEVUELVE POR SEPARADO en el array.\n"
            "   EJEMPLO REAL: si hay un gusano adentro de un grano de maíz con moho,\n"
            "   ESO SON DOS OBJETOS DISTINTOS:\n"
            "   {\"label\": \"maíz con moho\" ...}\n"
            "   {\"label\": \"gusano\" ...}\n"
            "   NUNCA combines cosas en un solo label tipo \"gusano sobre maíz con moho\".\n"
            "   SIEMPRE SEPARADOS.\n\n"

            "2. IDENTIFICÁ EL CULTIVO/GRANO/SEMILLA PRINCIPAL.\n"
            "   SOLO PODÉS USAR EXACTAMENTE uno de estos nombres:\n"
            "   \"maíz\", \"sorgo\", \"arroz\", \"trigo\", \"soja\",\n"
            "   \"cebada\", \"centeno\", \"avena\", \"girasol\",\n"
            "   \"poroto\", \"colza\", \"maní\".\n\n"
            "   Elegí el que MEJOR COINCIDA. Si no estás seguro, usá \"maíz\" si es\n"
            "   una mazorca amarilla con granos grandes en hileras pegados al marlo.\n"
            "   NO inventes nombres nuevos.\n"
            "   NO USES una palabra fuera de esa lista.\n"
            "   NO USES \"arroz\" si los granos están pegados formando una mazorca grande.\n\n"
            "   Cuando etiquetás el grano, agregá estado si aplica:\n"
            "     \"maíz sano\"\n"
            "     \"maíz roto\"\n"
            "     \"maíz con moho\"\n"
            "     \"maíz con pudrición\"\n"
            "   Elegí la más directa y específica.\n\n"

            "2.1 AGRUPACIÓN DE GRANOS:\n"
            "   Si varios granos/semillas iguales están pegados físicamente formando parte\n"
            "   de la misma estructura (por ejemplo muchos granos de maíz en la misma mazorca),\n"
            "   NO hagas muchas cajas pequeñas separadas.\n\n"
            "   En ese caso HACÉ UNA SOLA CAJA MÁS GRANDE que cubra toda esa zona continua,\n"
            "   y poné un solo label representativo tipo:\n"
            "   \"maíz sano\" / \"maíz con moho\" / \"maíz con pudrición\".\n\n"
            "   SOLO hacé cajas individuales cuando sea realmente un objeto distinto\n"
            "   (por ejemplo una larva/gusano, una rata, una paloma, etc.).\n\n"

            "3. PLAGAS VIVAS / INSECTOS / LARVAS / GUSANOS.\n"
            "   CADA plaga visible VA COMO OBJETO PROPIO con un label corto:\n"
            "   \"gusano\", \"larva\", \"gorgojo\", \"insecto\", \"polilla\".\n\n"
            "   SI VES un agujero en el grano con forma alargada, cuerpo segmentado\n"
            "   o un organismo similar a una larva alimentándose dentro del grano,\n"
            "   AUNQUE ESTÉ SOLO PARCIALMENTE VISIBLE,\n"
            "   IGUAL TENÉS QUE DEVOLVER UN OBJETO CON label \"gusano\"\n"
            "   y su propia caja \"box_2d\".\n\n"
            "   JAMÁS mezcles la larva/gusano con el maíz en una sola etiqueta.\n\n"

            "4. CONTAMINACIÓN DE FAUNA MAYOR.\n"
            "   SI ves presencia física o rastros claros de animales de almacenaje:\n"
            "   - roedor (rata, ratón)\n"
            "   - ave de silo (paloma, pájaro)\n\n"
            "   DEVOLVÉ cada uno como objeto separado con label literal:\n"
            "   \"rata\", \"ratón\", \"paloma\", \"ave\".\n\n"

            "5. HONGO / MOHO / PUDRICIÓN / DESCOMPOSICIÓN.\n"
            "   CADA área visible de moho, micelio fúngico, pudrición, descomposición\n"
            "   VA COMO OBJETO PROPIO con label corto tipo:\n"
            "   \"moho en grano\", \"pudrición fúngica\", \"hongo superficial\".\n\n"
            "6. MALEZA / MATERIAL VEGETAL EXTRAÑO.\n"
            "   Si hay restos vegetales que no son parte del cultivo objetivo (yuyos,\n"
            "   maleza de campo), devolvé como objeto con label \"maleza\".\n\n"

            "7. FORMATO DE SALIDA FINAL (OBLIGATORIO):\n"
            "   RESPUESTA = SOLO un array JSON (sin texto extra, sin ```).\n"
            "   Cada elemento del array tiene EXACTAMENTE:\n"
            "   {\n"
            "     \"label\": \"maíz con moho\",\n"
            "     \"box_2d\": [y1,x1,y2,x2],\n"
            "     \"score\": 0.92\n"
            "   }\n\n"
            "   - \"label\" es texto corto en español (de la lista o de plaga/fauna/hongo/maleza).\n"
            "   - \"box_2d\" son 4 ENTEROS [y1,x1,y2,x2] en coordenadas relativas 0 a 1000\n"
            "     donde (0,0) es esquina superior izquierda y (1000,1000) es esquina inferior derecha.\n"
            "   - \"score\" es tu confianza (0..1). Si dudás, usá score bajo.\n\n"

            "8. EJEMPLO (NO LO REPITAS SI NO APLICA A ESTA IMAGEN):\n"
            "[\n"
            "  {\"label\": \"maíz con moho\", \"box_2d\": [120,200,880,780], \"score\": 0.95},\n"
            "  {\"label\": \"gusano\", \"box_2d\": [430,480,560,610], \"score\": 0.86}\n"
            "]\n\n"

            "DEVOLVÉ AHORA SÓLO EL ARRAY JSON COMO DESCRIBÍ ARRIBA."
        )

        system_inst = (
            "Respondé SOLO con un array JSON de objetos con 'label', 'box_2d' y 'score'. "
            "NO incluyas markdown. NO expliques nada más."
        )

        config_seguridad = [
            types.SafetySetting(
                category="HARM_CATEGORY_DANGEROUS_CONTENT",
                threshold="BLOCK_ONLY_HIGH",
            ),
        ]

        resp = self.cliente.models.generate_content(
            model="gemini-2.5-flash",
            contents=[prompt, imagen_pil],
            config=types.GenerateContentConfig(
                system_instruction=system_inst,
                temperature=0.1,
                safety_settings=config_seguridad,
            )
        )

        bruto = resp.text or "[]"
        objetos_brutos = self._parsear_respuesta_json(bruto)

        # ---------- Filtro de confianza + firewall de etiquetas ----------
        objetos_filtrados = []
        for obj in objetos_brutos:
            if "label" not in obj or "box_2d" not in obj:
                continue
            score = obj.get("score", 1.0)
            if not isinstance(score, (int, float)):
                continue
            if score < 0.6:
                continue
            label_str = str(obj["label"]).strip()
            if not label_valida(label_str):
                # bloqueamos inventos o etiquetas fuera de dominio
                continue
            objetos_filtrados.append(obj)

        # ---------- Normalización ----------
        normalizados: List[Dict[str, Any]] = []
        for obj in objetos_filtrados:
            label_str = str(obj["label"]).strip()
            categoria, especie, estado = clasificar_label(label_str)
            score = float(obj.get("score", 1.0))

            normalizados.append({
                "label": label_str,
                "categoria": categoria,        # grano / plaga / fauna_riesgo / hongo / maleza / otro
                "especie": especie,            # "maiz", "soja", etc o None
                "estado_grano": estado,        # "sano", "roto", "moho" o None
                "box_2d": obj["box_2d"],       # [y1,x1,y2,x2] 0..1000
                "score": round(score, 3),
                "fuente_modelo": "gemini_spatial_2d"
            })

        # ---------- NMS ligero para duplicados de misma etiqueta ----------
        normalizados = nms_by_label(normalizados, iou_thr=0.7)

        return normalizados

    def _parsear_respuesta_json(self, bruto: str) -> List[Dict[str, Any]]:
        """
        Limpia ```json ...``` si viene con fences y lo parsea a lista.
        """
        texto = bruto.strip()
        if texto.startswith("```"):
            partes = texto.split("```")
            candidatos = [p for p in partes if "[" in p and "]" in p]
            if candidatos:
                texto = candidatos[0]
        try:
            data = json.loads(texto)
            if isinstance(data, list):
                return data
            return []
        except Exception as e:
            print(f"⚠️ No pude parsear JSON del modelo: {e}")
            return []

    def second_pass_plagas(self, img: Image.Image, sospechosas: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Recorre las zonas con moho/daño y corre un pass enfocado SOLO en plagas.
        Devuelve detecciones adicionales mapeadas al sistema de coords global (0..1000).
        """
        if not self.gemini_disponible:
            return []

        W, H = img.size
        extras: List[Dict[str, Any]] = []

        for det in sospechosas:
            y1n, x1n, y2n, x2n = det["box_2d"]  # 0..1000
            # Convertir a píxeles (global)
            x1 = max(0, int(x1n / 1000 * W))
            y1 = max(0, int(y1n / 1000 * H))
            x2 = min(W, int(x2n / 1000 * W))
            y2 = min(H, int(y2n / 1000 * H))

            # expandir un poco el crop (10%) para no cortar al gusano
            pad_x = max(2, int((x2 - x1) * 0.1))
            pad_y = max(2, int((y2 - y1) * 0.1))
            x1e = max(0, x1 - pad_x)
            y1e = max(0, y1 - pad_y)
            x2e = min(W, x2 + pad_x)
            y2e = min(H, y2 + pad_y)

            crop = img.crop((x1e, y1e, x2e, y2e))

            # pedir SOLO plagas
            prompt = (
                "Buscá SOLO plagas vivas en este recorte (gusano, larva, gorgojo, insecto, polilla).\n"
                "Devolvé un array JSON con objetos:\n"
                "{ \"label\": \"gusano\" | \"larva\" | \"gorgojo\" | \"insecto\" | \"polilla\",\n"
                "  \"box_2d\": [y1,x1,y2,x2],\n"
                "  \"score\": 0..1 }\n"
                "Si no hay plagas, devolvé []. Coordenadas relativas 0..1000."
            )

            system_inst = (
                "Respondé SOLO con un array JSON de objetos con 'label', 'box_2d' y 'score'. "
                "NO incluyas markdown. NO expliques nada más."
            )

            resp = self.cliente.models.generate_content(
                model="gemini-2.5-flash",
                contents=[prompt, crop],
                config=types.GenerateContentConfig(
                    system_instruction=system_inst,
                    temperature=0.1,
                    safety_settings=[
                        types.SafetySetting(
                            category="HARM_CATEGORY_DANGEROUS_CONTENT",
                            threshold="BLOCK_ONLY_HIGH",
                        ),
                    ],
                )
            )

            lista = self._parsear_respuesta_json(resp.text or "[]")
            if not lista:
                continue

            # mapear coords locale -> global
            cw = x2e - x1e
            ch = y2e - y1e

            for obj in lista:
                label = str(obj.get("label", "")).lower()
                if label not in {"gusano", "larva", "gorgojo", "insecto", "polilla"}:
                    continue

                score = obj.get("score", 1.0)
                if not isinstance(score, (int, float)):
                    continue
                if score < 0.55:
                    continue

                if "box_2d" not in obj or len(obj["box_2d"]) != 4:
                    continue

                cy1n, cx1n, cy2n, cx2n = obj["box_2d"]

                # píxeles dentro del crop
                cx1 = x1e + int((cx1n / 1000) * cw)
                cy1 = y1e + int((cy1n / 1000) * ch)
                cx2 = x1e + int((cx2n / 1000) * cw)
                cy2 = y1e + int((cy2n / 1000) * ch)

                # normalizar a 0..1000 globales
                gx1n = int((cx1 / W) * 1000)
                gy1n = int((cy1 / H) * 1000)
                gx2n = int((cx2 / W) * 1000)
                gy2n = int((cy2 / H) * 1000)

                label_str = "gusano" if "gusano" in label or "larva" in label else label

                categoria, especie, estado = clasificar_label(label_str)

                extras.append({
                    "label": label_str,
                    "categoria": categoria,        # esperado "plaga"
                    "especie": especie,            # None casi siempre acá
                    "estado_grano": estado,        # None
                    "box_2d": [gy1n, gx1n, gy2n, gx2n],
                    "score": round(float(score), 3),
                    "fuente_modelo": "gemini_spatial_2d_zoom"
                })

        # NMS entre plagas detectadas localmente
        extras = nms_by_label(extras, iou_thr=0.6)
        return extras

    def analisis_agronomico_global(self, imagen_pil: Image.Image) -> str:
        """
        Le pide a Gemini una explicación técnica entendible por productor.
        Español argentino forzado. 5-8 líneas, causa e impacto comercial/sanitario.
        """

        if not self.gemini_disponible:
            return "No se pudo generar diagnóstico global (Gemini no disponible)."

        prompt_global = (
            "Sos un técnico agrónomo especializado en postcosecha y almacenamiento de granos.\n"
            "Analizá la imagen y explicá claramente qué está pasando con el material observado.\n\n"
            "REQUISITOS DE RESPUESTA:\n"
            "- RESPONDÉ EN ESPAÑOL ARGENTINO, lenguaje claro, directo.\n"
            "- Describí qué cultivo o material se ve (por ejemplo 'mazorca de maíz').\n"
            "- Indicá si hay germinación prematura en la espiga, daño físico, ataque de larvas/gusanos,\n"
            "  presencia de moho u hongos, pudrición o descomposición.\n"
            "- Explicá impacto comercial: ¿esto sirve para vender / almacenar o está comprometido?\n"
            "- Explicá riesgo sanitario / inocuidad: ¿riesgo de hongos tóxicos, contaminación por plaga viva,\n"
            "  contacto con roedores o palomas, etc.?\n"
            "- Respondé en un párrafo de 5 a 8 líneas máximo, sin viñetas."
        )

        resp = self.cliente.models.generate_content(
            model="gemini-2.5-flash",
            contents=[prompt_global, imagen_pil],
            config=types.GenerateContentConfig(
                temperature=0.2,
                safety_settings=[
                    types.SafetySetting(
                        category="HARM_CATEGORY_DANGEROUS_CONTENT",
                        threshold="BLOCK_ONLY_HIGH",
                    ),
                ],
            )
        )

        texto = resp.text or ""
        return texto.strip()