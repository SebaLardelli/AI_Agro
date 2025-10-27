# Dockerfile simplificado para el servicio analyzer agrícola
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar requirements.txt e instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar solo los archivos Python necesarios
COPY analizador_agricola_modular.py .
COPY app_flask.py .
COPY modules/ ./modules/

# Crear directorio de salida
RUN mkdir -p /app/output

# Exponer puerto
EXPOSE 5000

# Comando por defecto
CMD ["python", "app_flask.py"]