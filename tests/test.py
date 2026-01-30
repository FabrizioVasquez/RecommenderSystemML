# tests/test.py
from src.pipeline.predict import MovieRecommender
import pytest
import os
import sys

# Asegurar que Python encuentre la carpeta src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def test_model_loading():
    # Solo corremos el test si existen los archivos (para evitar fallos en GitHub si no hay DVC configurado aún)
    if os.path.exists("artifacts/movie_list.pkl"):
        rec = MovieRecommender()
        assert len(rec.get_movie_list()) > 0

# Este test simula una recomendación real


def test_recommendation_logic():
    if os.path.exists("artifacts/movie_list.pkl"):
        rec = MovieRecommender()
        # Asegúrate que "Avatar" exista en tu dataset o usa otro
        names, ids = rec.recommend("Avatar")
        assert len(names) == 5
        assert len(ids) == 5
