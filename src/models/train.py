import pandas as pd
import pickle
import os
import ast
import nltk
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# --- 1. CONFIGURACIÓN DE NLTK PARA PRODUCCIÓN ---
# Esto descarga los diccionarios necesarios en una carpeta local
nltk.download('punkt')
nltk.download('stopwords')

# --- 2. RUTAS DINÁMICAS ---
# Base dir es la carpeta raíz del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_PATH = os.path.join(BASE_DIR, 'data')
ARTIFACTS_PATH = os.path.join(BASE_DIR, 'artifacts')
os.makedirs(ARTIFACTS_PATH, exist_ok=True)

# --- 3. FUNCIONES DE LIMPIEZA (Tu lógica) ---
def convert(text):
    l = []
    try:
        for i in ast.literal_eval(text):
            l.append(i['name'])
    except: return []
    return l

def convert_cst(text):
    l = []
    counter = 0
    try:
        for i in ast.literal_eval(text):
            if counter < 3:
                l.append(i['name'])
            counter += 1
    except: return []
    return l

def fetch_director(text):
    l = []
    try:
        for i in ast.literal_eval(text):
            if i['job'] == 'Producer': # Mantengo tu lógica de Producer
                l.append(i['name'])
                break
    except: return []
    return l

def remove_space(word):
    return [i.replace(" ", "") for i in word]

def stems(text):
    ps = PorterStemmer()
    return [ps.stem(i) for i in text.split()]

# --- 4. PIPELINE PRINCIPAL ---
def train_model():
    print(" [Training] Iniciando carga de datos...")
    
    # Verificar que existan los datos
    movies_path = os.path.join(DATA_PATH, 'tmdb_5000_movies.csv')
    credits_path = os.path.join(DATA_PATH, 'tmdb_5000_credits.csv')
    
    if not os.path.exists(movies_path) or not os.path.exists(credits_path):
        raise FileNotFoundError(f" No se encuentran los archivos CSV en {DATA_PATH}. Asegúrate de hacer 'dvc pull' primero.")

    movies = pd.read_csv(movies_path)
    credits = pd.read_csv(credits_path)

    # ETL
    print(" [Training] Fusionando y limpiando...")
    movies = movies.merge(credits, on='title')
    movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']]
    movies = movies.dropna(inplace=False)

    movies['genres'] = movies['genres'].map(convert)
    movies['keywords'] = movies['keywords'].map(convert)
    movies['cast'] = movies['cast'].map(convert_cst)
    movies['crew'] = movies['crew'].map(fetch_director)
    
    movies['overview'] = movies['overview'].apply(lambda x: x.split())
    
    movies['cast'] = movies['cast'].apply(remove_space)
    movies['crew'] = movies['crew'].apply(remove_space)
    movies['genres'] = movies['genres'].apply(remove_space)
    movies['keywords'] = movies['keywords'].apply(remove_space)

    movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']
    
    new_df = movies[['movie_id', 'title', 'tags']].copy()
    new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x).lower())
    
    print(" [Training] Aplicando Stemming y Vectorización...")
    new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(stems(x)))

    cv = CountVectorizer(max_features=5000, stop_words='english')
    vectors = cv.fit_transform(new_df['tags']).toarray()
    
    print(" [Training] Calculando similitud del coseno...")
    similarity = cosine_similarity(vectors)

    print(f" [Training] Guardando modelos en {ARTIFACTS_PATH}...")
    pickle.dump(new_df, open(os.path.join(ARTIFACTS_PATH, 'movie_list.pkl'), 'wb'))
    pickle.dump(similarity, open(os.path.join(ARTIFACTS_PATH, 'similarity.pkl'), 'wb'))
    print(" [Training] ¡Éxito!")

if __name__ == "__main__":
    train_model()