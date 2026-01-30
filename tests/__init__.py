# tests/test_recommender.py
import pytest
import os
import sys

# Asegurar que Python encuentre la carpeta src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.pipeline.predict import MovieRecommender

# Este test verifica si el sistema carga sin explotar
def test_model_loading():
    # Solo corremos el test si existen los archivos (para evitar fallos en GitHub si no hay DVC configurado aún)
    if os.path.exists("artifacts/movie_list.pkl"):
        rec = MovieRecommender()
        assert len(rec.get_movie_list()) > 0

# Este test simula una recomendación real
def test_recommendation_logic():
    if os.path.exists("artifacts/movie_list.pkl"):
        rec = MovieRecommender()
        names, ids = rec.recommend("Avatar") # Asegúrate que "Avatar" exista en tu dataset o usa otro
        assert len(names) == 5
        assert len(ids) == 5