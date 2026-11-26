from fastapi import FastAPI, HTTPException
from ml.engine import RecommendationEngine
from ml.tmdb_fetcher import fetch_popular_movies

app = FastAPI()

movies = fetch_popular_movies(page_count=5)
engine = RecommendationEngine(movies)


@app.get("/")
def root():
    return {"message": "CineMatch is running"}


@app.get("/movies")
def get_movies():
    return movies


@app.get("/movies/{movie_id}/recommendations")
def get_recommendations(movie_id: int, top_k: int = 5):
    results = engine.recommend(movie_id, top_k)

    if not results:
        raise HTTPException(status_code=404, detail="Movie not found")

    return results