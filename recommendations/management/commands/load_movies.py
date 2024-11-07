from django.core.management.base import BaseCommand
from recommendations.models import Movie  # Adjust this import based on your actual Movie model location
import json

class Command(BaseCommand):
    help = 'Load movies into the database'

    def handle(self, *args, **kwargs):

        movies_data = ([

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
