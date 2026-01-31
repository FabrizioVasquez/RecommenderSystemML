FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# 1. Instalar git
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# 2. Copiar requirements
COPY requirements.txt .

# 3. Instalar pathspec PRIMERO (evita que DVC instale versión rota)
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir "pathspec==0.11.2"

# 4. Instalar DVC con la versión de pathspec ya fijada
RUN pip install --no-cache-dir "dvc[s3]==3.37.0"

# 5. Instalar el resto
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copiar código
COPY . .

# 7. Git init
RUN git init && \
    git config user.email "deploy@render.com" && \
    git config user.name "Render Deploy" && \
    git add . && \
    git commit -m "Init for DVC"

# 8. Permisos
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

EXPOSE 8501

ENTRYPOINT ["./entrypoint.sh"]
CMD ["sh", "-c", "streamlit run app.py --server.port=${PORT:-8501} --server.address=0.0.0.0"]