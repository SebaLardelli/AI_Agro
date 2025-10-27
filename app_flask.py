#!/usr/bin/env python3
"""
app_flask.py

Servicio HTTP que consume n8n:
- n8n (Telegram) manda imagen binaria vía POST /analizar
- respondemos JSON listo para el agente

Devuelve:
 - data_momento (estructura para RAG)
 - diagnostico_texto (riesgo y métricas)
 - diagnostico_global (explicación agronómica humana, en español argentino)
 - metricas granulares
 - objetos_detectados individuales (maíz con moho, gusano, paloma, etc.)
 - ruta imagen_debug con bounding boxes dibujados
"""

import os
from flask import Flask, request, jsonify
from analizador_agricola_modular import AnalizadorAgricola

app = Flask(__name__)

analizador = AnalizadorAgricola()


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "ok": True,
        "service": "agro-analyzer",
        "gemini_disponible": analizador.gemini_disponible
    })


@app.route("/analizar", methods=["POST"])
def analizar():
    """
    Espera multipart/form-data con key 'image'
    """
    try:
        if "image" not in request.files:
            return jsonify({
                "ok": False,
                "error": "Falta campo 'image'. Enviá la imagen como form-data con la key 'image'."
            }), 400

        archivo = request.files["image"]
        if archivo.filename == "":
            return jsonify({
                "ok": False,
                "error": "Archivo vacío."
            }), 400

        raw_bytes = archivo.read()

        # correr analizador
        resultado = analizador.analizar_imagen(raw_bytes)

        return jsonify({
            "ok": True,
            "timestamp": resultado["timestamp"],
            "tipo_imagen": resultado["tipo_imagen"],
            "data_momento": resultado["data_momento"],
            "diagnostico_texto": resultado["diagnostico_texto"],
            "diagnostico_global": resultado["diagnostico_global"],
            "metricas": resultado["metricas"],
            "objetos_detectados": resultado["objetos_detectados"],
            "imagen_debug": resultado["imagen_bbox_path"]
        }), 200

    except Exception as e:
        return jsonify({
            "ok": False,
            "error": f"Error interno: {str(e)}"
        }), 500


@app.route("/debug", methods=["GET"])
def debug():
    return jsonify({
        "gemini_disponible": analizador.gemini_disponible,
        "GOOGLE_API_KEY_cargada": bool(os.getenv("GOOGLE_API_KEY")),
        "SUPABASE_URL_cargada": bool(os.getenv("SUPABASE_URL")),
        "output_dir_existe": os.path.exists("./output")
    })


if __name__ == "__main__":
    print("🚀 Flask en 0.0.0.0:5000")
    print("  GET  /health")
    print("  GET  /debug")
    print("  POST /analizar  <-- n8n manda la imagen acá (campo 'image')")
    app.run(host="0.0.0.0", port=5000, debug=True)
