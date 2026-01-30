# src/pipeline/predict.py
import os
import pickle
import logging

# Configurar logs (Esto es lo que verás en AWS CloudWatch o Grafana)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

class MovieRecommender:
    def __init__(self):
        # Rutas relativas para que funcione en Docker y Local
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.artifacts_path = os.path.join(base_path, 'artifacts')
        self._load_models()

    def _load_models(self):
        try:
            self.movies = pickle.load(open(os.path.join(self.artifacts_path, 'movie_list.pkl'), 'rb'))
            self.similarity = pickle.load(open(os.path.join(self.artifacts_path, 'similarity.pkl'), 'rb'))
            logger.info("Modelos cargados correctamente.")
        except FileNotFoundError:
            logger.error("No se encontraron los modelos. Verifica DVC.")
            raise

    def get_movie_list(self):
        return self.movies['title'].values

    def recommend(self, movie_title):
        if movie_title not in self.movies['title'].values:
            return [], []
        
        # Lógica de recomendación
        idx = self.movies[self.movies['title'] == movie_title].index[0]
        distances = sorted(list(enumerate(self.similarity[idx])), reverse=True, key=lambda x: x[1])
        
        names = []
        ids = []
        for i in distances[1:6]:
            movie_id = self.movies.iloc[i[0]].movie_id
            names.append(self.movies.iloc[i[0]].title)
            ids.append(movie_id)
        
        # LOG PARA MONITOREO: Registramos la predicción
        logger.info(f"PREDICCIÓN | Input: {movie_title} | Output: {names}")
        return names, ids