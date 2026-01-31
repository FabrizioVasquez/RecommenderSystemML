# Usamos una imagen base MUY ligera para ahorrar RAM en Render
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar dependencias del sistema mínimas
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias de Python
COPY requirements.txt .
# Asegúrate de que en requirements.txt esté: dvc[s3]
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código
COPY . .

# Copiar el script de entrada y darle permisos
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

# Puerto de Streamlit
EXPOSE 8501

# --- EL CAMBIO CLAVE ---
# Usamos el script como Entrypoint. 
# Esto significa que cada vez que arranque, ejecutará entrypoint.sh primero
ENTRYPOINT ["./entrypoint.sh"]

# El comando final que ejecutará el entrypoint
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]