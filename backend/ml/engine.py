from sentence_transformers import SentenceTransformer
import numpy as np
from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"


class RecommendationEngine:
    def __init__(self, movies):
        self.movies = movies
        self.model = SentenceTransformer(MODEL_NAME)

        overviews = [movie["overview"] for movie in movies]
        self.embeddings = self.model.encode(overviews, normalize_embeddings=True)
    
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