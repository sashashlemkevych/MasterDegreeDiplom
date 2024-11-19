from django.contrib import admin # type: ignore

# Register your models here.
# recommendations/admin.py

from .models import Movie, Rating, Review

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date', 'genres')  # Поля, які будуть відображатися в адмінці
    search_fields = ('title', 'genres')  # Додає поле пошуку за назвою та жанром фільму

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie', 'rating')  # Поля, які відображаються для моделі рейтингу
    list_filter = ('rating',)  # Додає фільтр за рейтингом

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie', 'created_at')  # Поля, які відображаються в таблиці
    search_fields = ('content',)  # Дозволяє шукати по тексту відгуку
    list_filter = ('created_at',)  # Додає фільтр по даті