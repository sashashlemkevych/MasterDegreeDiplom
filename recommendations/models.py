from django.db import models # type: ignore

# Create your models here.

# recommendations/models.py

from django.contrib.auth.models import User # type: ignore
from django.db import models # type: ignore

class Movie(models.Model):
    title = models.CharField(max_length=255)
    genres = models.CharField(max_length=255)
    overview = models.TextField()
    release_date = models.DateField()
    image = models.ImageField(upload_to='movie_images/')  # Для завантаження зображення фільму

    def __str__(self):
        return self.title

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.IntegerField()

    class Meta:
        unique_together = ('user', 'movie')

class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # Дата створення відгуку

    def __str__(self):
        return f"Review by {self.user.username} on {self.movie.title}"
    

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE, related_name='favorited_by')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'movie')  # Унікальність: кожен користувач може додати фільм тільки один раз