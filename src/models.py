import os
import pandas as pd

movies = pd.read_csv('../data/tmdb_5000_movies.csv')
credits = pd.read_csv('../data/tmdb_5000_credits.csv')

movies = movies.merge(credits,on='title')
movies.shape

import pandas as pd
import matplotlib.pyplot as plt
plt.tight_layout()


fig, ax = plt.subplots(figsize=(8,6))

movies.boxplot(column='vote_average', by='status', ax=ax)

medias = movies.groupby('status')['vote_average'].mean()

# Poner los promedios sobre la gráfica
for i, (status, media) in enumerate(medias.items(), start=1):  # start=1 porque los boxplots de Pandas indexan desde 1
    ax.scatter(i, media, color='red', zorder=3)  # rojo para el promedio
    ax.text(i, media+0.10, f'{media:.2f}', ha='center', color='blue')  # muestra el número

ax.set_title('Distribución de voto promedio por estado')
ax.set_xlabel('Status')
ax.set_ylabel('Vote Average')
plt.suptitle('')
plt.show()


movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']]

import ast

def convert(text: str=None):
    l = []
    for i in ast.literal_eval(text):
        l.append(i['name'])
    return l


movies['genres'] = movies['genres'].map(convert)
movies['keywords'] = movies['keywords'].map(convert)

def convert_cst(text: str=None):
    l = []
    counter = 0
    for i in ast.literal_eval(text):
        if counter < 3:
            l.append(i['name'])
        counter +=1
    return l

movies['cast'] = movies['cast'].map(convert_cst)

def fetch_director(text: str=None):
    l = []
    for i in ast.literal_eval(text):
        if i['job'] == 'Producer':
            l.append(i['name'])
            break
    return l

movies['crew'] = movies['crew'].map(fetch_director)

movies['overview'] = movies['overview'].map(lambda x:x.split())

def remove_space(word):
    l = []
    for i in word:
        l.append(i.replace(" ",""))
    return l

movies['cast'] = movies['cast'].map(remove_space)
movies['crew'] = movies['crew'].map(remove_space)
movies['genres'] = movies['genres'].map(remove_space)
movies['keywords'] = movies['keywords'].map(remove_space)

movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

new_movies = movies[['movie_id','title','tags']]

new_movies['tags'] = new_movies['tags'].map(lambda x: " ".join(x))

new_movies['tags'] = new_movies['tags'].map(lambda x:x.lower())


import nltk
from nltk.stem import PorterStemmer
ps = PorterStemmer()
def stems(text:str):
    l = []
    for i in text.split():
        l.append(ps.stem(i))
    return l

new_movies['tags'] = new_movies['tags'].map(stems)
new_movies['tags'] = new_movies['tags'].apply(lambda x: ' '.join(x))

from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=5000,stop_words='english')

vector = cv.fit_transform(new_movies['tags']).toarray()

from sklearn.metrics.pairwise import cosine_similarity
similarity = cosine_similarity(vector)
similarity

def recomemnd(movie):
    index = new_movies[new_movies['title'] == movie].index[0]
    distance = sorted(list(enumerate(similarity[index])),reverse=True,key=lambda x:x[1])
    for i in distance[1:6]:
        print(new_movies.iloc[i[0]].title)

recomemnd('Avatar')


import pickle 
os.makedirs('../artifacts',exist_ok=True)
pickle.dump(new_movies, open('../artifacts/movie_list.pkl','wb'))
pickle.dump(similarity, open('../artifacts/similarity.pkl','wb'))