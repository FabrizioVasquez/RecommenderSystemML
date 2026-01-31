# app.py
import streamlit as st
import requests
import os
from dotenv import load_dotenv

# =========================
# Cargar variables de entorno
# =========================
load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")

# URL del microservicio de ML
# En local: http://localhost:8000/predict
# En AWS: https://tu-api-ml.com/predict
ML_API_URL = os.getenv("ML_API_URL", "http://localhost:8000/predict")

# =========================
# Función para obtener posters
# =========================

def fetch_poster(movie_id):
    if not API_KEY:
        return "https://via.placeholder.com/500x750?text=ApiKeyMissing"
    try:
        url = (
            f"https://api.themoviedb.org/3/movie/{movie_id}"
            f"?api_key={API_KEY}&language=en-US"
        )
        response = requests.get(url, timeout=5)
        data = response.json()
        poster_path = data.get("poster_path")

        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
    except Exception:
        pass

    return "https://via.placeholder.com/500x750?text=No+Image"

# =========================
# UI Streamlit
# =========================
st.title("🎬 Sistema de Recomendación (Microservicios)")

movie_input = st.text_input("Escribe una película:")

if st.button("Recomendar"):
    if not movie_input.strip():
        st.warning(" Escribe el nombre de una película.")
        st.stop()

    try:
        # Llamada al microservicio ML
        response = requests.post(
            ML_API_URL,
            json={"movie_title": movie_input},
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()

            names = data.get("recommendations", [])
            ids = data.get("ids", [])

            if not names:
                st.error("No se encontraron recomendaciones.")
                st.stop()

            cols = st.columns(5)
            for i, col in enumerate(cols):
                if i < len(names):
                    with col:
                        st.text(names[i])
                        st.image(fetch_poster(ids[i]))

        else:
            st.error("❌ La API de recomendación falló.")

    except requests.exceptions.ConnectionError:
        st.error(
            " No se puede conectar con el Servicio de Inteligencia Artificial.\n\n"
            "¿Está levantado el backend ML?"
        )
    except requests.exceptions.Timeout:
        st.error(" El servicio de ML tardó demasiado en responder.")
