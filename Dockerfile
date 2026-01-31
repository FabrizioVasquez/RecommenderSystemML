FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# 1. Instalar herramientas del sistema
# Agregamos 'wget' para poder descargar el instalador de DVC
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    wget \
    && rm -rf /var/lib/apt/lists/*

# 2. INSTALACIÓN DE DVC AISLADA (La Clave del Éxito)
# Bajamos el paquete oficial y lo instalamos. 
# Esto incluye sus propias librerías y NO se pelea con boto3/mlflow.
RUN wget -qO dvc.deb https://dvc.org/download/linux-deb/dvc.deb && \
    apt-get install -y ./dvc.deb && \
    rm dvc.deb

# 3. Instalar TUS dependencias de Python
# Como DVC ya está instalado por fuera, pip instala boto3/mlflow rápido y sin errores.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copiar código
COPY . .

# 5. Inicializar Git falso (Necesario para que DVC corra en Docker)
RUN git init && \
    git config user.email "deploy@render.com" && \
    git config user.name "Render Deploy" && \
    git add . && \
    git commit -m "Dummy commit for DVC"

# 6. Permisos y Arranque
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

EXPOSE 8501

ENTRYPOINT ["./entrypoint.sh"]
CMD ["sh", "-c", "streamlit run app.py --server.port=${PORT:-8501} --server.address=0.0.0.0"]