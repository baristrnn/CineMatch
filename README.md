# 🎬 CineMatch

A content-based movie recommendation system that uses a pre-trained transformer model to understand what a movie is about and find movies with similar stories.

> **Status:** Work in progress. The backend recommendation engine is working; user accounts and a mobile app are planned.

---

## How It Works

1. **Data collection:** ~920 movies are fetched from the [TMDB API](https://www.themoviedb.org/) (popular + top rated lists). Duplicates and movies without a description are removed.
2. **Text building:** For each movie, its genres and plot overview are combined into one text, e.g.
   `"Action, Science Fiction, Adventure. After being held captive in an Afghan cave, ..."`
3. **Embedding:** The text is converted into a 384-dimensional vector using the pre-trained sentence transformer [`all-MiniLM-L6-v2`](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2). Movies with similar meaning get vectors that point in similar directions.
4. **Similarity:** Vectors are L2-normalized, so cosine similarity becomes a simple dot product. Similarity to all movies is computed in one matrix multiplication.
5. **Ranking:** Movies are sorted by similarity score and the top *k* are returned (excluding the movie itself).
6. **Caching:** Movies (`movies.json`) and embeddings (`embeddings.npy`) are saved to disk, so the server starts in seconds instead of minutes.

---

## Tech Stack

- **Python**, **FastAPI**, **Uvicorn**
- **sentence-transformers** (PyTorch) for embeddings
- **NumPy** for vector operations
- **TMDB API** as the data source

---

## Project Structure

```
CineMatch/
└── backend/
    ├── main.py              # API endpoints
    ├── core/
    │   └── config.py        # Environment variables
    ├── ml/
    │   ├── tmdb_fetcher.py  # Fetching and caching movie data
    │   └── engine.py        # Embeddings and recommendations
    └── requirements.txt
```

---

## Getting Started

**1. Clone the repository**

```bash
git clone https://github.com/<your-username>/cinematch.git
cd cinematch/backend
```

**2. Create a virtual environment and install dependencies**

```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS / Linux
pip install -r requirements.txt
```

**3. Add your TMDB API key**

Create a `.env` file inside `backend/`:

```
TMDB_API_KEY=your_tmdb_api_key_here
```

**4. Run the server**

```bash
uvicorn main:app --reload
```

The first run downloads the movie data and the model and computes the embeddings (a few minutes). Later runs load everything from the cache.

Interactive API docs: `http://localhost:8000/docs`

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Health check |
| GET | `/movies` | List all movies in the pool |
| GET | `/movies/{movie_id}/recommendations?top_k=5` | Get the most similar movies |

---

## Experiments

I improved the system step by step and tested each version on the same movies.

### Iron Man (2008)

| Version | Change | Top recommendation | Notes |
|---|---|---|---|
| v1 | Overview only, 100 movies | The Avengers (0.373) | 2 of top 5 were Marvel films |
| v2 | + Genres in the text | Avengers: Doomsday (0.542) | 3 of top 5 were Marvel films |
| v3 | + ~920 movies, disk cache | Iron Man 2 (0.739) | 4 of top 5 feature Tony Stark |

### Kalki 2898-AD (2024)

| Version | Result |
|---|---|
| v1 | *Ramayana* (also an Indian epic) was not in the top 5: its overview is about love and exile, not battle. |
| v2 | Adding genres moved *Ramayana* into the top 5 (0.449). |
| v3 | A larger pool pushed *Ramayana* out. *Kraven the Hunter* entered mainly because both overviews contain the word "hunter". |

**Note:** Scores from different versions should not be compared directly. Adding genres to every text raised all scores, so I compare the **ranking**, not the absolute score.

---

## Limitations

- **Only the overview and genres are used.** The model does not know about cast, director, language or country, so it cannot connect movies that share a culture but have different plots.
- **Sensitive to shared words and names.** Iron Man's results are strong because many overviews mention "Tony Stark", but *The Avengers* is missing because its overview does not. *Kraven the Hunter* was matched to *Kalki* because of the word "hunter".
- **More data is not always better.** A larger pool helped Iron Man (real sequels were added) but hurt Kalki (unrelated movies with surface-level matches were added).
- **Dataset bias.** The pool comes from TMDB's popular and top-rated lists, which are dominated by Hollywood films. Recommendations are weaker for movies from under-represented regions.
- **Short overviews.** Some movies have one-sentence descriptions, which give the model very little to work with.

---

## Roadmap

- [x] FastAPI backend with TMDB data
- [x] Embedding-based recommendations
- [x] Genres in the embedding text
- [x] Larger movie pool and disk cache
- [ ] Movie search endpoint
- [ ] Filter out movies with very short overviews
- [ ] User accounts and favourites (Supabase)
- [ ] Recommendations based on a user's favourites
- [ ] React Native mobile app

---

## Acknowledgements

This product uses the TMDB API but is not endorsed or certified by TMDB.