import pickle
import os
import streamlit as st
import requests
from dotenv import load_dotenv  # Tienes que instalar

load_dotenv()


def fetch_poster(movie_id):
    api_key = '91f4f736523cc2d1da26a602c2f6ad6a'
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"

    try:
        response = requests.get(url)
        data = response.json()
        #print(url)
        poster_path = data.get('poster_path')
        #print(poster_path)
        if poster_path:
            return "http://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"
    except:
        return "https://via.placeholder.com/500x750?text=No+Image"


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distance = sorted(
        list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommend_movies_name = []
    recommend_movies_poster = []
    for i in distance[1:6]:
        movie_id = movies.iloc[i[0]]['movie_id']
        recommend_movies_poster.append(fetch_poster(movie_id))
        recommend_movies_name.append(movies.iloc[i[0]]['title'])
    return recommend_movies_name, recommend_movies_poster


st.header("Sistema de recomendacion de peliculas usando Machine Learning")

movies = pickle.load(open('artifacts/movie_list.pkl', 'rb'))
similarity = pickle.load(open('artifacts/similarity.pkl', 'rb'))

movie_list = movies["title"].values

selected_movie = st.selectbox(
    'Escribe o selecciona una película para obtener una recomendacion',
    movie_list
)

if st.button('Muestrame recomendaciones'):
    recommended_movies_name, recommended_movies_poster = recommend(
        selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movies_name[0])
        st.image(recommended_movies_poster[0])

    with col2:
        st.text(recommended_movies_name[1])
        st.image(recommended_movies_poster[1])

    with col3:
        st.text(recommended_movies_name[2])
        st.image(recommended_movies_poster[2])

    with col4:
        st.text(recommended_movies_name[3])
        st.image(recommended_movies_poster[3])

    with col5:
        st.text(recommended_movies_name[4])
        st.image(recommended_movies_poster[4])
