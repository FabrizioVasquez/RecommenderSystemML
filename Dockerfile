# Usamos slim para ahorrar espacio y RAM
FROM python:3.10-slim

# Evita que Python genere archivos .pyc y buffer de salida
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar git (necesario para DVC) y limpiar caché apt para reducir peso
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar
COPY requirements.txt .
# Asegúrate de que en requirements NO esté 'dvc[s3]' si da problemas, 
# pero aquí sí necesitamos instalarlo para que funcione el entrypoint.
# RECOMENDACIÓN: Usa 'pip install dvc[s3]' explícito aquí si lo quitaste del txt.
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir "dvc[s3]"

# Copiar el código de la app
COPY . .

# Copiar y dar permisos al entrypoint
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

# Render ignora EXPOSE, pero es buena documentación
EXPOSE 8501

# Definimos el script que gestiona la descarga de datos
ENTRYPOINT ["./entrypoint.sh"]

# --- EL CAMBIO CRÍTICO PARA RENDER ---
# Usamos 'sh -c' para que pueda leer la variable de entorno $PORT que Render inyecta.
# Si $PORT no existe (en local), usa 8501 por defecto.
CMD ["sh", "-c", "streamlit run app.py --server.port=${PORT:-8501} --server.address=0.0.0.0"]