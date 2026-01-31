FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar git (necesario para DVC)
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# --- CORRECCIÓN DE DEPENDENCIAS ---
# Instalamos dvc[s3] Y los requirements AL MISMO TIEMPO.
# Esto permite que pip resuelva el conflicto de versiones de botocore automáticamente.
RUN pip install --no-cache-dir "dvc[s3]" -r requirements.txt

COPY . .

# --- CORRECCIÓN DEL ERROR "NOT A GIT REPOSITORY" ---
# Inicializamos un git vacío DENTRO de la imagen para que DVC no falle.
# No necesitamos la historia, solo la estructura .git
RUN git init && \
    git config user.email "you@example.com" && \
    git config user.name "Your Name" && \
    git add . && \
    git commit -m "Dummy commit for DVC"

# Preparar script de arranque
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

EXPOSE 8501

ENTRYPOINT ["./entrypoint.sh"]
CMD ["sh", "-c", "streamlit run app.py --server.port=${PORT:-8501} --server.address=0.0.0.0"]