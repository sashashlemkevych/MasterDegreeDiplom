# recommendations/urls.py

from django.urls import path # type: ignore
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    #path('home/', views.home, name='home'),  # Додатковий маршрут для home
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    #path('movie/<int:id>/rate/', views.rate_movie, name='rate_movie'),
    

    
    path('logout', views.logout_view, name='logout'),
    path('loginform', views.loginform, name='loginform'),
    path('registerform', views.registerform, name='registerform'),
]
