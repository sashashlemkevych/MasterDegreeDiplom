import random
from django.core.management.base import BaseCommand
from recommendations.models import User, Movie, Rating  # Змініть your_app на назву вашого додатка

class Command(BaseCommand):
    help = 'Generate random ratings for users'

    def handle(self, *args, **kwargs):
        # Отримання всіх користувачів і фільмів
        users = User.objects.all()
        movies = Movie.objects.all()

        for user in users:
            # Випадкове число фільмів для оцінювання (30-40)
            num_ratings = random.randint(40, 50)
            
            # Випадковий вибір фільмів
            rated_movies = random.sample(list(movies), num_ratings)

            for movie in rated_movies:
                # Перевірка, чи існує вже запис для даного користувача та фільму
                if not Rating.objects.filter(user_id=user.id, movie_id=movie.id).exists():
                    # Генерація випадкової оцінки від 1 до 5
                    rating_value = random.randint(1, 5)
                    # Створення запису у таблиці Rating
                    Rating.objects.create(user_id=user.id, movie_id=movie.id, rating=rating_value)

        self.stdout.write(self.style.SUCCESS('Successfully generated random ratings without duplicates.'))
