# Imagen base ligera
FROM python:3.10-slim

# Evitar archivos basura de python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar dependencias del sistema (gcc a veces es necesario para ciertas libs)
RUN apt-get update && apt-get install -y --no-install-recommends gcc && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Instalar librerías Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente
COPY . .

# NOTA: Los modelos .pkl deben estar ya en la carpeta artifacts/
# GitHub Actions se encarga de ponerlos ahí con 'dvc pull' antes de este paso.

# Exponer el puerto de Streamlit
EXPOSE 8501

# Chequeo de salud (Opcional, ayuda a AWS a saber si la app vive)
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Comando de arranque
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]