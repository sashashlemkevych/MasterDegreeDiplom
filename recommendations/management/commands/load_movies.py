from django.core.management.base import BaseCommand
from recommendations.models import Movie  # Adjust this import based on your actual Movie model location
import json

class Command(BaseCommand):
    help = 'Load movies into the database'

    def handle(self, *args, **kwargs):
        movies_data = [
    {
        "title": "Inception",
        "genres": ["Action", "Science Fiction", "Adventure"],
        "release_date": "2010-07-16",
        "overview": "A skilled thief is given a chance at redemption if he can successfully perform inception: planting an idea into a target's subconscious.",
        "image": "https://image.tmdb.org/t/p/w500/r1R1aW5jN2ku1xyzyLoACrE9P2T.jpg"
    },
    {
        "title": "The Matrix",
        "genres": ["Action", "Science Fiction"],
        "release_date": "1999-03-31",
        "overview": "A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.",
        "image": "https://image.tmdb.org/t/p/w500/xJ9g2U8WoAUMtZ1i2i5G3gOTVQD.jpg"
    },
    {
        "title": "Titanic",
        "genres": ["Drama", "Romance"],
        "release_date": "1997-12-19",
        "overview": "A seventeen-year-old aristocrat falls in love with a kind but poor artist aboard the luxurious, ill-fated R.M.S. Titanic.",
        "image": "https://image.tmdb.org/t/p/w500/7bS3AL8E67gU9JDL81C0xltwz5N.jpg"
    },
    {
        "title": "The Shawshank Redemption",
        "genres": ["Drama"],
        "release_date": "1994-09-23",
        "overview": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
        "image": "https://image.tmdb.org/t/p/w500/8vOZ9UNtR8S4Ijl8yYv1hMLi9iM.jpg"
    },
    {
        "title": "Forrest Gump",
        "genres": ["Drama", "Romance"],
        "release_date": "1994-07-06",
        "overview": "The presidencies of Kennedy and Johnson, the Vietnam War, the Watergate scandal, and other historical events unfold through the perspective of an Alabama man with an IQ of 75.",
        "image": "https://image.tmdb.org/t/p/w500/4YoqNU6ay9D7mUgH0xIcT8NY7pW.jpg"
    },
    {
        "title": "Gladiator",
        "genres": ["Action", "Drama"],
        "release_date": "2000-05-05",
        "overview": "A former Roman General sets out to exact vengeance against the corrupt emperor who murdered his family and sent him into slavery.",
        "image": "https://image.tmdb.org/t/p/w500/dZ8P58BcGcmF5nC9esBJJYp8r2H.jpg"
    },
    {
        "title": "The Godfather",
        "genres": ["Crime", "Drama"],
        "release_date": "1972-03-14",
        "overview": "An organized crime dynasty's aging patriarch transfers control of his clandestine empire to his reluctant son.",
        "image": "https://image.tmdb.org/t/p/w500/lAHojF7R0D3S4w4vLhAD1pQcb8L.jpg"
    },
    {
        "title": "The Dark Knight",
        "genres": ["Action", "Crime", "Drama"],
        "release_date": "2008-07-18",
        "overview": "When the menace known as the Joker emerges from his mysterious past, he wreaks havoc and chaos on the people of Gotham. The Dark Knight must accept one of the greatest psychological and physical tests of his ability to fight injustice.",
        "image": "https://image.tmdb.org/t/p/w500/xJ1p4F4D0MyI1GB8w5I3P0MBjVa.jpg"
    },
    {
        "title": "Pulp Fiction",
        "genres": ["Crime", "Drama"],
        "release_date": "1994-10-14",
        "overview": "The lives of two mob hitmen, a boxer, a gangster's wife, and a pair of diner bandits intertwine in four tales of violence and redemption.",
        "image": "https://image.tmdb.org/t/p/w500/4VItqB1XezW4wLZ4Uqnl92rOj3j.jpg"
    },
    {
        "title": "Fight Club",
        "genres": ["Drama"],
        "release_date": "1999-10-15",
        "overview": "An insomniac office worker and a devil-may-care soap maker form an underground fight club that evolves into much more.",
        "image": "https://image.tmdb.org/t/p/w500/jPKInw4I3gqFOSDgFMAqheI12kZ.jpg"
    },
    {
        "title": "The Social Network",
        "genres": ["Drama", "Biography"],
        "release_date": "2010-10-01",
        "overview": "As Harvard students create the social networking site, Mark Zuckerberg finds himself becoming the target of lawsuits that threaten to destroy everything he has built.",
        "image": "https://image.tmdb.org/t/p/w500/5KX8hx2YQY18m5Hb0Ip4yRDmYTo.jpg"
    },
    {
        "title": "Interstellar",
        "genres": ["Science Fiction", "Adventure"],
        "release_date": "2014-11-07",
        "overview": "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.",
        "image": "https://image.tmdb.org/t/p/w500/5e15N7a2fOQ56NzFYkNXY0SgToY.jpg"
    },
    {
        "title": "The Silence of the Lambs",
        "genres": ["Crime", "Drama", "Thriller"],
        "release_date": "1991-02-14",
        "overview": "A young FBI cadet must confide in an incarcerated and manipulative killer to receive his help on catching another serial killer who skins his victims.",
        "image": "https://image.tmdb.org/t/p/w500/nB7jZxtwqtMOTks1WPPbN6KqTCA.jpg"
    },
    {
        "title": "The Lord of the Rings: The Fellowship of the Ring",
        "genres": ["Action", "Adventure", "Fantasy"],
        "release_date": "2001-12-19",
        "overview": "A meek hobbit from the Shire and eight companions set out on a journey to destroy the One Ring and save Middle-earth from the Dark Lord Sauron.",
        "image": "https://image.tmdb.org/t/p/w500/5e1g3C43gfwwyX2OIf7h5rQG9F2.jpg"
    },
    {
        "title": "Harry Potter and the Sorcerer's Stone",
        "genres": ["Adventure", "Fantasy"],
        "release_date": "2001-11-16",
        "overview": "An orphaned boy discovers he is a wizard and attends Hogwarts School of Witchcraft and Wizardry, where he learns the truth about himself, his family, and the terrible evil that haunts the magical world.",
        "image": "https://image.tmdb.org/t/p/w500/4yBfF65cQhmtXeo8URqK40tX8kp.jpg"
    },
    {
        "title": "Jurassic Park",
        "genres": ["Science Fiction", "Adventure"],
        "release_date": "1993-06-11",
        "overview": "During a preview tour, a theme park suffers a major power breakdown that allows its cloned dinosaur exhibits to run amok.",
        "image": "https://image.tmdb.org/t/p/w500/6uFb0xlq3uB1cgCPMdfTxzH0b1Y.jpg"
    },
    {
        "title": "The Avengers",
        "genres": ["Action", "Adventure", "Science Fiction"],
        "release_date": "2012-05-04",
        "overview": "Nick Fury of S.H.I.E.L.D. brings together a team of superheroes to save the planet from Loki and his army.",
        "image": "https://image.tmdb.org/t/p/w500/fz9X8x9BTrgU6dPQ9iU4wN5ZP9n.jpg"
    },
    {
        "title": "Guardians of the Galaxy",
        "genres": ["Action", "Adventure", "Comedy"],
        "release_date": "2014-08-01",
        "overview": "A group of intergalactic criminals must pull together to stop a fanatical warrior with plans to purge the universe.",
        "image": "https://image.tmdb.org/t/p/w500/7I5YRL0pUbQPVyGxlD2nTscNp0o.jpg"
    },
    {
        "title": "The Lion King",
        "genres": ["Animation", "Adventure", "Drama"],
        "release_date": "1994-06-15",
        "overview": "Lion prince Simba flees his kingdom after the death of his father, but returns as an adult to reclaim his throne from his uncle, Scar.",
        "image": "https://image.tmdb.org/t/p/w500/5i2p7OvNSdPHpSRGpKzpRmhEu1w.jpg"
    },
    {
        "title": "Inside Out",
        "genres": ["Animation", "Family", "Adventure"],
        "release_date": "2015-06-19",
        "overview": "After young Riley is uprooted from her Midwest life and moved to San Francisco, her emotions — Joy, Fear, Anger, Disgust, and Sadness — conflict on how best to navigate a new city, house, and school.",
        "image": "https://image.tmdb.org/t/p/w500/5wW1NOABVeWc3VwUReED4p4azY6.jpg"
    },
    {
        "title": "Coco",
        "genres": ["Animation", "Adventure", "Family"],
        "release_date": "2017-11-22",
        "overview": "Despite his family's baffling generations-old ban on music, Miguel dreams of becoming an accomplished musician. He sets off on an extraordinary journey to unlock the real story behind his family history.",
        "image": "https://image.tmdb.org/t/p/w500/9zZ8YTH62MoIzgtbERbAzONlHOf.jpg"
    },
    {
        "title": "The Grand Budapest Hotel",
        "genres": ["Comedy", "Drama", "Adventure"],
        "release_date": "2014-03-28",
        "overview": "A writer encounters the former owner of The Grand Budapest Hotel, who recounts his former life and the events that led to his present situation.",
        "image": "https://image.tmdb.org/t/p/w500/9iMNZmlHMGtoML5cl7u4jZGGq43.jpg"
    },
    {
        "title": "Django Unchained",
        "genres": ["Drama", "Western"],
        "release_date": "2012-12-25",
        "overview": "With the help of a German bounty hunter, a freed slave sets out to rescue his wife from a brutal Mississippi plantation owner.",
        "image": "https://image.tmdb.org/t/p/w500/7F8XHSO9uVVmv0dlZBxREgr6Wx7.jpg"
    },
    {
        "title": "Black Panther",
        "genres": ["Action", "Adventure", "Fantasy"],
        "release_date": "2018-02-16",
        "overview": "T'Challa, the king of Wakanda, rises to the throne in the isolated, technologically advanced African nation, but his past soon comes back to haunt him.",
        "image": "https://image.tmdb.org/t/p/w500/oeAoW89e9U1AK88HugMmZl2MeHq.jpg"
    },
]

        
        for movie in movies_data:
            Movie.objects.create(
                title=movie['title'],
                genres=','.join(movie['genres']),  # Assuming you are storing genres as a comma-separated string
                release_date=movie['release_date'],
                overview=movie['overview'],
                image=movie['image']
            )
        self.stdout.write(self.style.SUCCESS('Movies successfully loaded into the database.'))
