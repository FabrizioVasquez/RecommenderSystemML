# Usamos Python 3.10 Slim (más ligero que la imagen completa)
FROM python:3.10-slim

# Evita archivos temporales y logs en buffer
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo
WORKDIR /app

# 1. Instalar dependencias del sistema y librerías Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2. Descargar corpora de NLTK (solución al error común de "Resource not found")
RUN python -m nltk.downloader punkt stopwords wordnet

# 3. Copiar código y datos
# NOTA: Docker necesita los CSV para entrenar. Asegúrate de que no estén en .dockerignore
COPY . .

# 4. ENTRENAMIENTO AUTOMÁTICO (Build-time training)
# Esto crea los .pkl dentro de la imagen
RUN python src/models/train.py

# 5. Configuración de Streamlit
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]