import requests
from core.config import TMDB_API_KEY

BASE_URL = "https://api.themoviedb.org/3"

def fetch_genre_map():
    response = requests.get(
        f"{BASE_URL}/genre/movie/list",
        params={"api_key": TMDB_API_KEY, "language": "en-US"},
    )
    genres = response.json()["genres"]
    return {genre["id"]: genre["name"] for genre in genres}

def fetch_popular_movies(page_count=5):
    genre_map = fetch_genre_map()  # 🆕
    movies = []

    for page in range(1, page_count + 1):
        response = requests.get(
            f"{BASE_URL}/movie/popular",
            params={"api_key": TMDB_API_KEY, "language": "en-US", "page": page},
        )
        data = response.json()

        for movie in data["results"]:
            if not movie["overview"]:
                continue

            genre_names = [genre_map.get(genre_id, "") for genre_id in movie["genre_ids"]]  # 🆕

            movies.append({
                "id": movie["id"],
                "title": movie["title"],
                "overview": movie["overview"],
                "genres": genre_names,  # 🆕
            })

    return movies