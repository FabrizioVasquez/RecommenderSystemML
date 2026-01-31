# app.py
import streamlit as st
import requests
import os
import logging
from dotenv import load_dotenv

# Importamos la clase directamente (Monolito Modular)
# Esto evita tener que levantar un segundo servidor para la API
from src.pipeline.predict import MovieRecommender

# =========================
# Configuración
# =========================
# Configurar logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("StreamlitApp")

# Cargar variables (En Render fallará silenciosamente, en local carga .env)
load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")

# =========================
# Función para obtener posters
# =========================


def fetch_poster(movie_id):
    if not API_KEY:
        # Placeholder si no hay API Key
        return "https://via.placeholder.com/500x750?text=ApiKeyMissing"

    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
        # Timeout para no colgar la app
        response = requests.get(url, timeout=2)

        if response.status_code != 200:
            return "https://via.placeholder.com/500x750?text=ErrorAPI"

        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path

    except Exception as e:
        logger.error(f"Error fetching poster for {movie_id}: {e}")
        pass

    return "https://via.placeholder.com/500x750?text=No+Image"

# =========================
# Carga del Modelo (CRÍTICO PARA RENDER)
# =========================
# Usamos cache_resource para cargar el modelo UNA sola vez en memoria.
# Si no usas esto, Render explotará por falta de RAM cada vez que des clic.


@st.cache_resource
def load_recommender():
    return MovieRecommender()


# Intentar cargar la lógica
try:
    recommender = load_recommender()
except Exception as e:
    st.error(
        f"Error crítico: No se pudieron cargar los modelos .pkl. \nDetalle: {e}")
    st.stop()

# =========================
# Interfaz Gráfica (UI)
# =========================
st.title("Sistema de Recomendación de Películas")
st.caption("Machine Learning Portfolio | Desplegado en Render")

# Selector de películas (usando la lista cargada del modelo)
movie_list = recommender.get_movie_list()
selected_movie = st.selectbox(
    'Selecciona una película que te guste:',
    movie_list
)

if st.button('Obtener Recomendaciones'):
    if not selected_movie:
        st.warning("Por favor selecciona una película.")
    else:
        with st.spinner('Analizando gustos...'):
            # Llamada DIRECTA a la clase (sin requests.post)
            names, ids = recommender.recommend(selected_movie)

        if names:
            cols = st.columns(5)
            for i, col in enumerate(cols):
                if i < len(names):
                    with col:
                        st.image(fetch_poster(ids[i]), use_column_width=True)
                        st.caption(names[i])
        else:
            st.warning("No se encontraron recomendaciones para esta película.")
