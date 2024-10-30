from django.contrib import admin # type: ignore

# Register your models here.
# recommendations/admin.py

from .models import Movie, Rating

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date', 'genres')  # Поля, які будуть відображатися в адмінці
    search_fields = ('title', 'genres')  # Додає поле пошуку за назвою та жанром фільму

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie', 'rating')  # Поля, які відображаються для моделі рейтингу
    list_filter = ('rating',)  # Додає фільтр за рейтингом
