# app.py
import streamlit as st
import requests
import os
from dotenv import load_dotenv
from src.pipeline.predict import MovieRecommender

# Cargar variables de entorno (seguridad)
load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")

# Función auxiliar solo para imágenes
def fetch_poster(movie_id):
    if not API_KEY:
        return "https://via.placeholder.com/500x750?text=ApiKeyMissing"
    
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
        data = requests.get(url, timeout=5).json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "http://image.tmdb.org/t/p/w500/" + poster_path
    except Exception:
        pass
    return "https://via.placeholder.com/500x750?text=No+Image"

# Instanciar lógica
try:
    recommender = MovieRecommender()
except Exception as e:
    st.error("Error cargando modelos. ¿Ejecutaste el entrenamiento?")
    st.stop()

st.header("Sistema de recomendación de películas")

selected_movie = st.selectbox(
    'Selecciona una película:',
    recommender.get_movie_list()
)

if st.button('Recomendar'):
    names, ids = recommender.recommend(selected_movie)
    
    cols = st.columns(5)
    for i, col in enumerate(cols):
        with col:
            st.text(names[i])
            st.image(fetch_poster(ids[i]))