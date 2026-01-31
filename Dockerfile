FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# 1. Instalar git (DVC lo necesita)
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# 2. Copiar requirements PRIMERO (para aprovechar cache de Docker)
COPY requirements.txt .

# 3. Instalar DVC + tus dependencias EN UNA SOLA CAPA
# Esto evita conflictos de versiones
RUN pip install --no-cache-dir \
    "dvc[s3]==3.56.0" \
    -r requirements.txt

# 4. Copiar código
COPY . .

# 5. Configurar Git (DVC lo requiere)
RUN git init && \
    git config user.email "deploy@render.com" && \
    git config user.name "Render Deploy" && \
    git add . && \
    git commit -m "Init for DVC"

# 6. Permisos
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

EXPOSE 8501

ENTRYPOINT ["./entrypoint.sh"]
CMD ["sh", "-c", "streamlit run app.py --server.port=${PORT:-8501} --server.address=0.0.0.0"]