# recommendations/urls.py

from django.urls import path # type: ignore
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    #path('home/', views.home, name='home'),  # Додатковий маршрут для home
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('addmovie', views.addmovie, name='addmovie'),
    path('updatemovie/<int:movie_id>/', views.updatemovie, name='updatemovie'),
    path('deletemovie/<int:movie_id>/', views.deletemovie, name='deletemovie'),
    path('delete_review/<int:review_id>/', views.delete_review, name='delete_review'),
    path('search/', views.home, name='search'),
    path('logout', views.logout_view, name='logout'),
    path('loginform', views.loginform, name='loginform'),
    path('registerform', views.registerform, name='registerform'),
    path('movies/<int:movie_id>/toggle_favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('favorites/', views.favorite_movies, name='favorite_movies'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
