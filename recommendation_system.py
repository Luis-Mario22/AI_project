"""Sistema simple de recomendación de películas.

Este script demuestra un enfoque básico basado en géneros:
- analiza las películas que ha valorado un usuario,
- calcula su afinidad por géneros,
- recomienda películas no vistas con mayor probabilidad de interesarle.
"""

from collections import defaultdict
from typing import Dict, List, Tuple

MOVIES: Dict[str, Dict[str, str]] = {
    "Inception": {"genre": "Ciencia ficción"},
    "The Matrix": {"genre": "Ciencia ficción"},
    "Interstellar": {"genre": "Ciencia ficción"},
    "The Dark Knight": {"genre": "Acción"},
    "Mad Max: Fury Road": {"genre": "Acción"},
    "Dune": {"genre": "Acción"},
    "Titanic": {"genre": "Romance"},
    "La La Land": {"genre": "Romance"},
    "The Notebook": {"genre": "Romance"},
    "Shrek": {"genre": "Animación"},
    "Toy Story": {"genre": "Animación"},
    "Frozen": {"genre": "Animación"},
    "The Silence of the Lambs": {"genre": "Suspenso"},
    "Se7en": {"genre": "Suspenso"},
    "Gone Girl": {"genre": "Suspenso"},
}

USER_RATINGS: Dict[str, Dict[str, float]] = {
    "Ana": {
        "Inception": 5,
        "The Matrix": 4,
        "Titanic": 2,
        "The Dark Knight": 5,
        "Toy Story": 3,
    },
    "Luis": {
        "Interstellar": 5,
        "Dune": 4,
        "La La Land": 3,
        "The Notebook": 4,
        "Shrek": 4,
    },
    "Marta": {
        "The Dark Knight": 4,
        "Mad Max: Fury Road": 5,
        "Frozen": 5,
        "The Silence of the Lambs": 4,
        "The Matrix": 3,
    },
}


def calculate_genre_affinity(user_ratings: Dict[str, float]) -> Dict[str, float]:
    """Devuelve la media de puntuación por género para un usuario."""
    genre_scores: Dict[str, List[float]] = defaultdict(list)

    for movie_title, score in user_ratings.items():
        if movie_title in MOVIES:
            genre = MOVIES[movie_title]["genre"]
            genre_scores[genre].append(score)

    return {
        genre: sum(scores) / len(scores)
        for genre, scores in genre_scores.items()
    }


def calculate_global_genre_ratings() -> Dict[str, float]:
    """Calcula la nota media global de cada género en todos los usuarios."""
    genre_scores: Dict[str, List[float]] = defaultdict(list)

    for ratings in USER_RATINGS.values():
        for movie_title, score in ratings.items():
            if movie_title in MOVIES:
                genre = MOVIES[movie_title]["genre"]
                genre_scores[genre].append(score)

    return {
        genre: sum(scores) / len(scores)
        for genre, scores in genre_scores.items()
    }


def recommend_movies(username: str, top_n: int = 3) -> List[Tuple[str, float]]:
    """Devuelve una lista ordenada con las mejores recomendaciones para un usuario."""
    if username not in USER_RATINGS:
        raise ValueError(f"El usuario '{username}' no existe en la base de datos.")

    user_ratings = USER_RATINGS[username]
    genre_affinity = calculate_genre_affinity(user_ratings)
    global_genre_ratings = calculate_global_genre_ratings()

    recommendations: List[Tuple[str, float]] = []

    for title, info in MOVIES.items():
        if title in user_ratings:
            continue

        genre = info["genre"]
        affinity = genre_affinity.get(genre, 2.5)
        global_score = global_genre_ratings.get(genre, 2.5)

        # Usamos una combinación de afinidad personal y tendencia global
        predicted_score = round((affinity * 0.7) + (global_score * 0.3), 2)
        recommendations.append((title, predicted_score))

    recommendations.sort(key=lambda item: item[1], reverse=True)
    return recommendations[:top_n]


def show_recommendations(username: str) -> None:
    """Muestra las recomendaciones en formato legible."""
    print(f"\nRecomendaciones para {username}:\n")
    recommended = recommend_movies(username)

    if not recommended:
        print("No hay recomendaciones disponibles.")
        return

    for i, (movie, score) in enumerate(recommended, start=1):
        genre = MOVIES[movie]["genre"]
        print(f"{i}. {movie} - Género: {genre} - Puntuación estimada: {score}")


if __name__ == "__main__":
    print("Sistema de recomendación de películas")
    print("Usuarios disponibles:", ", ".join(USER_RATINGS.keys()))

    user_name = input("\nEscribe el nombre del usuario: ").strip().title()

    if user_name not in USER_RATINGS:
        print(f"Usuario '{user_name}' no encontrado. Intenta con: Ana, Luis o Marta.")
    else:
        show_recommendations(user_name)
