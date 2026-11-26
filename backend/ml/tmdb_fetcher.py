import json
from pathlib import Path

import requests
from core.config import TMDB_API_KEY

BASE_URL = "https://api.themoviedb.org/3"


def fetch_genre_map():
    response = requests.get(
        f"{BASE_URL}/genre/movie/list",
        params={"api_key": TMDB_API_KEY, "language": "en-US"},
        timeout=10,
    )
    response.raise_for_status()
    genres = response.json()["genres"]
    return {genre["id"]: genre["name"] for genre in genres}


def fetch_movies(endpoint, page_count, genre_map):
    movies = []

    for page in range(1, page_count + 1):
        response = requests.get(
            f"{BASE_URL}/movie/{endpoint}",
            params={"api_key": TMDB_API_KEY, "language": "en-US", "page": page},
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()

        for movie in data["results"]:
            if not movie["overview"]:
                continue

            genre_names = [genre_map.get(genre_id, "") for genre_id in movie["genre_ids"]]

            movies.append({
                "id": movie["id"],
                "title": movie["title"],
                "overview": movie["overview"],
                "genres": genre_names,
            })

    return movies


def fetch_movie_pool(page_count=25):
    genre_map = fetch_genre_map()

    popular = fetch_movies("popular", page_count, genre_map)
    top_rated = fetch_movies("top_rated", page_count, genre_map)

    unique_movies = {}
    for movie in popular + top_rated:
        unique_movies[movie["id"]] = movie

    return list(unique_movies.values())


def load_movies(cache_path):
    cache_path = Path(cache_path)

    if cache_path.exists():
        print("Loading movies from cache...")
        with open(cache_path, "r", encoding="utf-8") as file:
            return json.load(file)

    print("Fetching movies from TMDB...")
    movies = fetch_movie_pool()

    cache_path.parent.mkdir(parents=True, exist_ok=True)
    with open(cache_path, "w", encoding="utf-8") as file:
        json.dump(movies, file, ensure_ascii=False, indent=2)

    return movies