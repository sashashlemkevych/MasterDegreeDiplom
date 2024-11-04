# recommendations/recommendations.py

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from django.db.models import Avg
from .models import Movie, Rating

def get_hybrid_recommendations(user_id, top_n=10):
    # Завантаження даних з бази даних
    user_movie_matrix = Rating.objects.values('user', 'movie', 'rating')
    user_movie_df = pd.DataFrame(user_movie_matrix)

    # Перетворюємо дані в матрицю
    user_movie_df = user_movie_df.pivot(index='user', columns='movie', values='rating').fillna(0)

    # Обчислення матриці схожості
    content_similarity = compute_content_similarity()
    collaborative_similarity = compute_collaborative_similarity(user_movie_df)

    # Ваги для гібридної системи
    content_weight = 0.5
    collaborative_weight = 0.5

    # Створюємо гібридну матрицю схожості
    final_recommendation_score = (content_similarity * content_weight) + (collaborative_similarity * collaborative_weight)

    # Отримання рекомендованих фільмів для користувача
    unrated_movie_ids = user_movie_df.columns[user_movie_df.loc[user_id] == 0].tolist()  # Фільми, які користувач ще не оцінив
    movie_scores = []
    for movie_id in unrated_movie_ids:
        # Розрахунок рейтингу як середнього схожості з іншими користувачами
        movie_score = sum(final_recommendation_score.loc[user_id, other_user] * user_movie_df.loc[other_user, movie_id]
                          for other_user in user_movie_df.index if movie_id in user_movie_df.columns)
        movie_scores.append((movie_id, movie_score))

    sorted_movies = sorted(movie_scores, key=lambda x: x[1], reverse=True)
    recommended_movie_ids = [movie[0] for movie in sorted_movies[:top_n]]

    # Повертаємо рекомендовані фільми
    return Movie.objects.filter(id__in=recommended_movie_ids)

def compute_content_similarity():
    movies = Movie.objects.all()
    # Створюємо матрицю жанрів, описів та назв
    genres = [movie.genres.split(', ') for movie in movies]  # Розділення жанрів
    overviews = [movie.overview for movie in movies]
    titles = [movie.title for movie in movies]

    # Об'єднуємо жанри, описи та назви
    combined_features = [f"{title} {' '.join(genres)} {overview}" for title, genres, overview in zip(titles, genres, overviews)]

    count_vectorizer = CountVectorizer()
    feature_matrix = count_vectorizer.fit_transform(combined_features)

    # Обчислюємо косинусну схожість
    content_similarity = cosine_similarity(feature_matrix)
    return pd.DataFrame(content_similarity, index=movies.values_list('id', flat=True), columns=movies.values_list('id', flat=True))


def compute_collaborative_similarity(user_movie_df):
    # Обчислюємо косинусну схожість для колаборативної фільтрації
    user_similarity = cosine_similarity(user_movie_df)
    return pd.DataFrame(user_similarity, index=user_movie_df.index, columns=user_movie_df.index)
