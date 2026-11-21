from fastapi import FastAPI
from ml.tmdb_fetcher import fetch_popular_movies

app = FastAPI()


@app.get("/")
def root():
    return {"message": "CineMatch is running"}


@app.get("/movies")
def get_movies():
    return fetch_popular_movies(page_count=2)