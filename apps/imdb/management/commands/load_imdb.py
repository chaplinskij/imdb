import json

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from apps.imdb.services import IMDbLoader


class Command(BaseCommand):
    help = """
        Loads all IMDb datasets into the database.

        This command imports data from all IMDb dataset files (.tsv.gz) and populates the corresponding Django models.

        Usage:
            python manage.py load_imdb_data --path <path_to_imdb_datasets>

        Arguments:
            --path      Path to the directory containing IMDb dataset files.

        Supported Files:
            - name.basics.tsv.gz       (People: actors, directors, writers)
            - title.akas.tsv.gz        (Alternate titles for movies/TV shows)
            - title.basics.tsv.gz      (Basic information about movies/TV shows)
            - title.crew.tsv.gz        (Directors and writers)
            - title.episode.tsv.gz     (Episode information for TV shows)
            - title.principals.tsv.gz  (Key cast and crew members)
            - title.ratings.tsv.gz     (Ratings and number of votes)

        Example:
            python manage.py load_imdb --path datasets/imdb

        Notes:
            - Data is loaded in bulk for better performance.
            - Missing or invalid data is safely ignored.
            - Ensure the database is migrated before running this command.
    """

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str, required=True, help='Path to IMDb dataset files.')


    def handle(self, *args, **options):
        IMDbLoader.load(options['path'])
