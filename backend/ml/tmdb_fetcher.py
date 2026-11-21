import requests
from core.config import TMDB_API_KEY

BASE_URL = "https://api.themoviedb.org/3"


def fetch_popular_movies(page_count=5):
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

            movies.append({
                "id": movie["id"],
                "title": movie["title"],
                "overview": movie["overview"],
            })

    return movies