from django.shortcuts import render, redirect, get_object_or_404 # type: ignore
from django.contrib.auth import login, authenticate, logout # type: ignore
from django.contrib.auth.hashers import make_password # type: ignore
# Create your views here.

# recommendations/views.py


from .models import Movie, Rating
from .forms import RegisterForm
import joblib
from django.http import JsonResponse # type: ignore
from django.views.decorators.csrf import csrf_exempt # type: ignore
import json
from django.contrib.auth.decorators import login_required # type: ignore
from django.db.models import Avg
from .recommendations import get_hybrid_recommendations  # Імпортуємо вашу функцію

def home(request):
    if request.user.is_authenticated:
        # Якщо користувач авторизований, отримуємо рекомендації
        recommendations = get_hybrid_recommendations(request.user.id)
        movies = Movie.objects.all()  # Отримуємо всі фільми
    else:
        # Якщо користувач не авторизований, показуємо топові фільми
        top_movies = Rating.objects.values('movie').annotate(avg_rating=Avg('rating')).order_by('-avg_rating')[:10]
        # Отримуємо фільми за їх ID
        movies = Movie.objects.filter(id__in=[item['movie'] for item in top_movies])

    for movie in movies:
        if request.user.is_authenticated:
            # Знайти рейтинг поточного користувача для кожного фільму
            user_rating = Rating.objects.filter(user=request.user, movie=movie).first()
            movie.user_rating = user_rating.rating if user_rating else 0  # Якщо рейтинг відсутній, встановити 0
        else:
            movie.user_rating = 0  # Для анонімного користувача встановити рейтинг 0 або None
        # Створити список зірок: заповнені (True) або порожні (False)
        movie.stars = [True if i < movie.user_rating else False for i in range(5)]

    return render(request, 'recommendations/home.html', {
        'movies': movies,
        'recommendations': recommendations if request.user.is_authenticated else None,  # Передаємо рекомендації, якщо авторизовані
    })

# def home(request):
#     movies = Movie.objects.all()
#     for movie in movies:
#         if request.user.is_authenticated:
#             # Знайти рейтинг поточного користувача для кожного фільму
#             user_rating = Rating.objects.filter(user=request.user, movie=movie).first()
#             movie.user_rating = user_rating.rating if user_rating else 0  # Якщо рейтинг відсутній, встановити 0
#         else:
#             movie.user_rating = 0  # Для анонімного користувача встановити рейтинг 0 або None
#         # Створити список зірок: заповнені (True) або порожні (False)
#         movie.stars = [True if i < movie.user_rating else False for i in range(5)]
#     return render(request, 'recommendations/home.html', {'movies': movies})


def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    
    # Перевірка наявності рейтингу тільки для авторизованих користувачів
    current_rating = None
    if request.user.is_authenticated:
        user_rating = Rating.objects.filter(user=request.user, movie=movie).first()
        current_rating = user_rating.rating if user_rating else None

    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            rating = request.POST.get('rating')
            if rating:
                # Оновити або створити рейтинг
                Rating.objects.update_or_create(user=request.user, movie=movie, defaults={'rating': rating})
                return JsonResponse({'success': True, 'new_rating': rating})
        else:
            return JsonResponse({'success': False, 'message': 'Треба увійти, щоб залишити рейтинг'}, status=401)

    # Додаємо список з 1 до 5 для зірочок
    star_range = range(1, 6)
    
    return render(request, 'recommendations/movie_detail.html', {
        'movie': movie,
        'current_rating': current_rating,
        'star_range': star_range
    })



def loginform(request):
    error_message=''
    if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Перенаправлення після успішної авторизації
            else:
                error_message = 'Неправильне ім`я користувача або пароль'

    return render(request, 'recommendations/loginform.html', {'error_message': error_message})


def registerform(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Перенаправлення після успішної реєстрації
    else:
        form = RegisterForm()

    return render(request, 'recommendations/registerform.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')  # Перенаправлення після виходу