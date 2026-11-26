from fastapi import FastAPI, HTTPException,Query
from ml.engine import RecommendationEngine
from ml.tmdb_fetcher import load_movies


app = FastAPI()

movies = load_movies("data/movies.json")
engine = RecommendationEngine(movies, "data/embeddings.npy")


@app.get("/")
def root():
    return {"message": "CineMatch is running"}


@app.get("/movies")
def get_movies():
    return movies

@app.get("/movies/search")
def search_movies(
    q: str = Query(min_length=2),
    limit: int = Query(default=10, ge=1, le=50),
):
    return engine.search(q, limit)


@app.get("/movies/{movie_id}/recommendations")
def get_recommendations(movie_id: int, top_k: int = 5):
    results = engine.recommend(movie_id, top_k)

    if not results:
        raise HTTPException(status_code=404, detail="Movie not found")

    return results