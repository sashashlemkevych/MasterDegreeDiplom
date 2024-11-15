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
from django.db.models import Avg, F
from django.db.models import Q
from django.db.models import F, Case, When, Value, IntegerField
from django.db.models.functions import Lower
from .forms import AddMovieForm
from django.core.paginator import Paginator
from django.shortcuts import render

from .recommendations import get_hybrid_recommendations, get_popular_movies # Імпортуємо вашу функцію


def home(request):
    query = request.GET.get('q')
    search_results = None
    user = request.user
    sort_option = request.GET.get('sort', 'default')
    current_user = request.user

    if query:
        # Split the query into words and create a filter that matches any of them in the title
        search_terms = query.split()
        search_query = Q()
        for term in search_terms:
            search_query |= Q(title__icontains=term)
        # Get movies that match any word in the query, ignoring case
        search_results = Movie.objects.filter(search_query)
    
    if request.user.is_authenticated:
        # Перевіряємо, чи є у користувача оцінки
        if Rating.objects.filter(user_id=user.id).exists():
            # Якщо користувач авторизований, отримуємо рекомендації
            recommendations = get_hybrid_recommendations(request.user.id)[:9]
        else:
            # Якщо користувач не оцінив фільми, даємо популярні фільми
            recommendations = get_popular_movies(top_n=9)
        
        #movies = Movie.objects.all()  # Отримуємо всі фільми
        movies = Movie.objects.order_by('-id')
    else:
        # # Якщо користувач не авторизований, показуємо топові фільми
        # top_movies = Rating.objects.values('movie').annotate(avg_rating=Avg('rating')).order_by('-avg_rating')[:9]
        # movies = Movie.objects.filter(id__in=[item['movie'] for item in top_movies])
        
        # Якщо користувач не авторизований, показуємо топові фільми з середнім рейтингом від 4 до 5
        top_movies = Rating.objects.values('movie') \
        .annotate(avg_rating=Avg('rating')) \
        .filter(avg_rating__gte=3, avg_rating__lte=5) \
        .order_by('-avg_rating')[:9]

        movies = Movie.objects.filter(id__in=[item['movie'] for item in top_movies])
        
            
        # Get sorting option from query parameters
        
    if sort_option == 'az':
        movies = movies.order_by('title')  # Sort A-Z
    elif sort_option == 'za':
        movies = movies.order_by('-title')  # Sort Z-A

    



    # Пагінація
    paginator = Paginator(movies, 9)  # 9 фільмів на сторінку
    page_number = request.GET.get('page')  # Номер сторінки з GET-запиту
    page_obj = paginator.get_page(page_number)  # Об'єкт сторінки

 # Додавання рейтингів і зірок для кожного фільму на поточній сторінці
    for movie in page_obj.object_list:
        if request.user.is_authenticated:
            user_rating = Rating.objects.filter(user=request.user, movie=movie).first()
            movie.user_rating = user_rating.rating if user_rating else 0  # Set to 0 if no rating
        else:
            movie.user_rating = 0  # Для анонімного користувача встановити рейтинг 0 або None
        # Створити список зірок: заповнені (True) або порожні (False)
        movie.stars = [True if i < movie.user_rating else False for i in range(5)]


    context = {
        'page_obj': page_obj,  # Передаємо об'єкт сторінки в шаблон
        'movies': movies,
        'recommendations': recommendations if request.user.is_authenticated else None,
        'search_results': search_results,
        'query': query,
        'sort_option': sort_option,  # Параметр сортування
    }
    return render(request, 'recommendations/home.html', context)


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


def addmovie(request):
    error = ''
    if request.method == 'POST':
        form  = AddMovieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            error = "Дані не правильного формату"
    form = AddMovieForm()
    context = {

        'form': form, 
        'error': error

    }
    return render(request, 'recommendations/addmovie.html', context)


def updatemovie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if request.method == "POST":
        form = AddMovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('movie_detail', movie_id=movie.id)
    else:
        form = AddMovieForm(instance=movie)
    
    context = {
        'form': form,
        'movie': movie,
    }
    return render(request, 'recommendations/updatemovie.html', context)

def deletemovie(request, movie_id):
    movies = Movie.objects.get(pk=movie_id)
    movies.delete()
    return redirect('home')
   

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