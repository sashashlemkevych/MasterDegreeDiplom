from django.core.management.base import BaseCommand
from recommendations.models import Movie  # Adjust this import based on your actual Movie model location
import json

class Command(BaseCommand):
    help = 'Load movies into the database'

    def handle(self, *args, **kwargs):

        movies_data = ([
    {
        "title": "Ла-Ла Ленд",
        "genres": ["Мюзикл", "Драма", "Романтика"],
        "release_date": "2016-12-09",
        "overview": "Молодий джазовий музикант і актриса закохуються, намагаючись досягти своїх мрій у Лос-Анджелесі.",
        "image": "https://image.tmdb.org/t/p/w500/uf7W6YzP7yMm3Uj5XtKkKAtRC44.jpg"
    },
    {
        "title": "Термінатор 2: Судний день",
        "genres": ["Бойовик", "Фантастика", "Трилер"],
        "release_date": "1991-07-03",
        "overview": "Термінатор повертається в минуле, щоб захистити молодого Джона Коннора від нового супротивника.",
        "image": "https://image.tmdb.org/t/p/w500/rYYbGiM6Yot0stf3K7NlDgDNEXu.jpg"
    },
    {
        "title": "Володар перснів: Братство персня",
        "genres": ["Пригоди", "Фентезі", "Епічний"],
        "release_date": "2001-12-19",
        "overview": "Група героїв об'єднується, щоб знищити могутній перстень і врятувати свою землю.",
        "image": "https://image.tmdb.org/t/p/w500/nNw7EvJYlNU8G8BR3nsrFRz1Pjb.jpg"
    },
    {
        "title": "Люди Ікс",
        "genres": ["Пригоди", "Фантастика", "Бойовик"],
        "release_date": "2000-07-12",
        "overview": "Група мутантів об'єднується, щоб захистити світ від інших мутантів, які ставлять його під загрозу.",
        "image": "https://image.tmdb.org/t/p/w500/fA74hBW5nXLZfU1mFLlmEcm8GRZ.jpg"
    },
    {
        "title": "Крижане серце",
        "genres": ["Анімація", "Пригоди", "Сімейний"],
        "release_date": "2013-11-27",
        "overview": "Дві сестри, одна з яких має магічні здібності, повинні об'єднати зусилля, щоб врятувати королівство від вічної зими.",
        "image": "https://image.tmdb.org/t/p/w500/4U1uRPEyBDtxFf0zLQZ9JH75w0O.jpg"
    },
    {
        "title": "Малефісента",
        "genres": ["Фентезі", "Пригоди", "Драма"],
        "release_date": "2014-05-30",
        "overview": "Історія з точки зору зловісної феї, яка наклала прокляття на принцесу Аврору.",
        "image": "https://image.tmdb.org/t/p/w500/4q0Stn4LZfs7DNRijgFhvNPO0Io.jpg"
    },
    {
        "title": "Аватар",
        "genres": ["Фантастика", "Пригоди"],
        "release_date": "2009-12-18",
        "overview": "Людина на чужій планеті бере участь у конфлікті між аборигенами і людьми, які хочуть експлуатувати її ресурси.",
        "image": "https://image.tmdb.org/t/p/w500/bpN5FYZfQZzC7v2AWCZcAavhW1B.jpg"
    },
    {
        "title": "Час",
        "genres": ["Фантастика", "Драма", "Романтика"],
        "release_date": "2011-09-29",
        "overview": "Чоловік намагається змінити своє життя, використовуючи здатність подорожувати в часі.",
        "image": "https://image.tmdb.org/t/p/w500/8GlVEbZt4HCEHv2xzq1sbE0nA4B.jpg"
    },
])

        for movie in movies_data:
            Movie.objects.create(
                title=movie['title'],
                genres=','.join(movie['genres']),  # Assuming you are storing genres as a comma-separated string
                release_date=movie['release_date'],
                overview=movie['overview'],
                image=movie['image']
            )
        self.stdout.write(self.style.SUCCESS('Movies successfully loaded into the database.'))
