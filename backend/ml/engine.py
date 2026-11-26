import re
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"


def build_movie_text(movie):
    genres = ", ".join(movie["genres"])
    return f"{genres}. {movie['overview']}"

def normalize_text(text):
    text = text.lower()
    text = re.sub(r"\W+", " ", text)
    return text.strip()

class RecommendationEngine:
    def __init__(self, movies, cache_path):
        self.movies = movies
        self.model = SentenceTransformer(MODEL_NAME)
        self.embeddings = self._load_or_build_embeddings(Path(cache_path))

    def _load_or_build_embeddings(self, cache_path):
        if cache_path.exists():
            embeddings = np.load(cache_path)
            if len(embeddings) == len(self.movies):
                print("Loading embeddings from cache...")
                return embeddings

        print(f"Encoding {len(self.movies)} movies...")
        texts = [build_movie_text(movie) for movie in self.movies]
        embeddings = self.model.encode(
            texts, normalize_embeddings=True, show_progress_bar=True
        )

        cache_path.parent.mkdir(parents=True, exist_ok=True)
        np.save(cache_path, embeddings)
        return embeddings

    def find_index(self, movie_id):
        for index, movie in enumerate(self.movies):
            if movie["id"] == movie_id:
                return index
        return None

    def recommend(self, movie_id, top_k=5):
        index = self.find_index(movie_id)
        if index is None:
            return []

        target = self.embeddings[index]
        scores = self.embeddings @ target
        ranked_indices = np.argsort(scores)[::-1]

        recommendations = []
        for i in ranked_indices:
            if i == index:
                continue

            movie = self.movies[i]
            recommendations.append({
                "id": movie["id"],
                "title": movie["title"],
                "score": round(float(scores[i]), 3),
            })

            if len(recommendations) == top_k:
                break

        return recommendations
    
    def search(self, query, limit=10):
        query = normalize_text(query)

        if not query:
            return []

        compact_query = query.replace(" ", "")  # 🆕

        starts_with = []
        contains = []
        compact_matches = []  # 🆕

        for movie in self.movies:
            title = normalize_text(movie["title"])
            compact_title = title.replace(" ", "")  # 🆕

            if title.startswith(query):
                starts_with.append(movie)
            elif query in title:
                contains.append(movie)
            elif compact_query in compact_title:  # 🆕
                compact_matches.append(movie)  # 🆕

        results = starts_with + contains + compact_matches  # 🆕

        return [
            {"id": movie["id"], "title": movie["title"], "genres": movie["genres"]}
            for movie in results[:limit]
        ]