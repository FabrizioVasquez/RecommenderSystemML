from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.pipeline.predict import MovieRecommender
import uvicorn
import os

# Definimos el esquema de entrada (Qué esperamos recibir)
class RecommendationRequest(BaseModel):
    movie_title: str

# Iniciamos la App
app = FastAPI(title="Movie Recommender API", version="1.0")

# Cargamos el modelo UNA SOLA VEZ al iniciar la API
# Esto es vital: en microservicios, el modelo vive en la memoria de la API viaja
recommender = MovieRecommender()

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/predict")
def predict(request: RecommendationRequest):
    """
    Recibe: { "movie_title": "Avatar" }
    Devuelve: { "recommendations": [...], "ids": [...] }
    """
    try:
        names, ids = recommender.recommend(request.movie_title)
        
        if not names:
            raise HTTPException(status_code=404, detail="Movie not found")
            
        return {
            "movie": request.movie_title,
            "recommendations": names,
            "ids": [int(id) for id in ids] # Convertir numpy int a python int normal
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)