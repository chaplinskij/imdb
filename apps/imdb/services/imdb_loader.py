import csv
import gzip
from tqdm import tqdm

from apps.imdb.models import (
    Akas,
    Crew,
    Episode,
    Genre,
    Person,
    Principal,
    Profession,
    Movie,
    MovieType,
    Rating,
)

__all__ = ('IMDbLoader', )

BATCH_SIZE = 1000


class IMDbLoader:
    @classmethod
    def load(cls, path):
        cls.load_movies(f'{path}/title.basics.tsv.gz')
        cls.load_persons(f'{path}/name.basics.tsv.gz')
        cls.load_ratings(f'{path}/title.ratings.tsv.gz')
        cls.load_crew(f'{path}/title.crew.tsv.gz')
        # cls.load_akas(f'{path}/title.akas.tsv.gz')
        # cls.load_episodes(f'{path}/title.episode.tsv.gz')
        # cls.load_principals(f'{path}/title.principals.tsv.gz')

    @classmethod
    def get_total_lines(cls, file_path):
        with gzip.open(file_path, 'rt', encoding='utf-8') as file:
            total_lines = sum(1 for _ in file) - 1
        return total_lines

    @classmethod
    def load_persons(cls, file_path):
        total_rows = cls.get_total_lines(file_path)
        with gzip.open(file_path, 'rt', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter='\t', quoting=csv.QUOTE_NONE)
            persons = []
            movies = {}
            professions = {}
            for row in tqdm(reader, total=total_rows, desc="Loading Persons", unit="rows"):
                persons.append(Person(
                    id=row['nconst'],
                    name=row['primaryName'],
                    birth_year=int(row['birthYear']) if row['birthYear'] != '\\N' else None,
                    death_year=int(row['deathYear']) if row['deathYear'] != '\\N' else None,
                ))
                movies[row['nconst']] = row['knownForTitles'].split(',')
                professions[row['nconst']] = row['primaryProfession'].split(',')
                if len(persons) >= BATCH_SIZE:
                    persones_objects = Person.objects.bulk_create(persons, batch_size=BATCH_SIZE)
                    movie_objects = []
                    proffesion_objects = []
                    for p in persones_objects:
                        movie_objects += [
                            Person.movies.through(person_id=p.id, movie_id=item)
                            for item in movies[p.id] if item != '\\N'
                        ]
                        proffesion_objects += [
                            Person.professions.through(person_id=p.id, profession_id=Profession.mapped_choices.get(item))
                            for item in professions[p.id] if Profession.mapped_choices.get(item)
                        ]
                    Person.movies.through.objects.bulk_create(movie_objects, batch_size=BATCH_SIZE)
                    Person.professions.through.objects.bulk_create(proffesion_objects, batch_size=BATCH_SIZE)
                    persons = []
            if persons:
                persones_objects = Person.objects.bulk_create(persons, batch_size=BATCH_SIZE)
                movie_objects = []
                proffesion_objects = []
                for p in persones_objects:
                    movie_objects += [
                        Person.movies.through(person_id=p.id, movie_id=item)
                        for item in movies[p.id] if item != '\\N'
                    ]
                    proffesion_objects += [
                        Person.professions.through(person_id=p.id, profession_id=Profession.mapped_choices.get(item))
                        for item in professions[p.id] if Profession.mapped_choices.get(item)
                    ]
                Person.movies.through.objects.bulk_create(movie_objects, batch_size=BATCH_SIZE)
                Person.professions.through.objects.bulk_create(proffesion_objects, batch_size=BATCH_SIZE)

    @classmethod
    def load_movies(cls, file_path):
        total_rows = cls.get_total_lines(file_path)
        with gzip.open(file_path, 'rt', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter='\t', quoting=csv.QUOTE_NONE)
            genres = {}
            movies = []
            for row in tqdm(reader, total=total_rows, desc="Loading Movies", unit="rows"):
                movies.append(Movie(
                    id=row['tconst'],
                    movie_type_id=MovieType.mapped_choices.get(row['titleType'], MovieType.no_type),
                    title=row['primaryTitle'],
                    original_title=row['originalTitle'],
                    is_adult=row['isAdult'] == '1',
                    year=int(row['startYear']) if row['startYear'] != '\\N' else None,
                    end_year=int(row['endYear']) if row['endYear'] != '\\N' else None,
                    runtime_minutes=int(row['runtimeMinutes']) if row['runtimeMinutes'] != '\\N' else None
                ))
                genres[row['tconst']] = row['genres'].split(',')
                if len(movies) >= BATCH_SIZE:
                    movies_objects = Movie.objects.bulk_create(movies, batch_size=BATCH_SIZE)
                    genres_objects = []
                    for m in movies_objects:
                        genres_objects += [
                            Movie.genres.through(movie_id=m.id, genre_id=Genre.mapped_choices.get(item))
                            for item in genres[m.id] if Genre.mapped_choices.get(item)
                        ]
                    Movie.genres.through.objects.bulk_create(genres_objects)
                    movies = []
            if movies:
                movies_objects = Movie.objects.bulk_create(movies, batch_size=BATCH_SIZE)
                genres_objects = []
                for m in movies_objects:
                    genres_objects += [
                        Movie.genres.through(movie_id=m.id, genre_id=Genre.mapped_choices.get(item))
                        for item in genres[m.id] if Genre.mapped_choices.get(item)
                    ]
                Movie.genres.through.objects.bulk_create(genres_objects)

    @classmethod
    def load_akas(cls, file_path):
        total_rows = cls.get_total_lines(file_path)
        with gzip.open(file_path, 'rt', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter='\t', quoting=csv.QUOTE_NONE)
            akas = []
            for row in tqdm(reader, total=total_rows, desc="Loading Akas", unit="rows"):
                akas.append(Akas(
                    movie_id=row['titleId'],
                    ordering=int(row['ordering']),
                    title=row['title'][:512],
                    region=row['region'],
                    language=row['language'],
                    types=row['types'],
                    attributes=row['attributes'],
                    is_original_title=row['isOriginalTitle'] == '1'
                ))
                if len(akas) >= BATCH_SIZE:
                    Akas.objects.bulk_create(akas, batch_size=BATCH_SIZE)
                    akas = []
            if akas:
                Akas.objects.bulk_create(akas, batch_size=BATCH_SIZE)

    @classmethod
    def load_crew(cls, file_path):
        total_rows = cls.get_total_lines(file_path)
        with gzip.open(file_path, 'rt', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter='\t', quoting=csv.QUOTE_NONE)
            crews = []
            directors = {}
            writers = {}
            for row in tqdm(reader, total=total_rows, desc="Loading Crews", unit="rows"):
                movie_id = row['tconst']
                crews.append(Crew(
                    movie_id=row['tconst'],
                ))
                directors[movie_id] = row['directors'].split(',')
                writers[movie_id] = row['writers'].split(',')
                if len(crews) >= BATCH_SIZE:
                    crew_objects = Crew.objects.bulk_create(crews, batch_size=BATCH_SIZE)
                    director_objects = []
                    writer_objects = []
                    for c in crew_objects:
                        director_objects += [
                            Crew.directors.through(crew_id=c.id, person_id=item)
                            for item in directors[c.movie_id]  if item != '\\N'
                        ]
                        writer_objects += [
                            Crew.writers.through(crew_id=c.id, person_id=item)
                            for item in writers[c.movie_id] if item != '\\N'
                        ]
                    Crew.directors.through.objects.bulk_create(director_objects)
                    Crew.writers.through.objects.bulk_create(writer_objects)
                    crews = []
            if crews:
                crew_objects = Crew.objects.bulk_create(crews, batch_size=BATCH_SIZE)
                director_objects = []
                writer_objects = []
                for c in crew_objects:
                    director_objects += [
                        Crew.directors.through(crew_id=c.id, person_id=item)
                        for item in directors[c.movie_id] if item != '\\N'
                    ]
                    writer_objects += [
                        Crew.writers.through(crew_id=c.id, person_id=item)
                        for item in writers[c.movie_id] if item != '\\N'
                    ]
                Crew.directors.through.objects.bulk_create(director_objects)
                Crew.writers.through.objects.bulk_create(writer_objects)

    @classmethod
    def load_episodes(cls, file_path):
        total_rows = cls.get_total_lines(file_path)
        with gzip.open(file_path, 'rt', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter='\t', quoting=csv.QUOTE_NONE)
            episodes = []
            for row in tqdm(reader, total=total_rows, desc="Loading Episodes", unit="rows"):
                episodes.append(Episode(
                    movie_id=int(row['tconst'][2:]),
                    parent_id=int(row['parentTconst'][2:]),
                    season_number=int(row['seasonNumber']) if row['seasonNumber'] != '\\N' else None,
                    episode_number=int(row['episodeNumber']) if row['episodeNumber'] != '\\N' else None
                ))

                if len(episodes) >= BATCH_SIZE:
                    Episode.objects.bulk_create(episodes, batch_size=BATCH_SIZE)
                    episodes = []
            if episodes:
                Episode.objects.bulk_create(episodes, batch_size=BATCH_SIZE)

    @classmethod
    def load_principals(cls, file_path):
        with gzip.open(file_path, 'rt', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter='\t', quoting=csv.QUOTE_NONE)
            principals = []
            for row in reader:
                principals.append(Principal(
                    movie_id=int(row['tconst'][2:]),
                    person_id=int(row['nconst'][2:]),
                    category=row['category'],
                    job=row['job'] if row['job'] != '\\N' else '',
                    characters=row['characters'] if row['characters'] != '\\N' else ''
                ))
                if len(principals) >= BATCH_SIZE:
                    Principal.objects.bulk_create(principals, batch_size=BATCH_SIZE)
                    principals = []
            if principals:
                Principal.objects.bulk_create(principals, batch_size=BATCH_SIZE)

    @classmethod
    def load_ratings(cls, file_path):
        total_rows = cls.get_total_lines(file_path)
        with gzip.open(file_path, 'rt', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter='\t', quoting=csv.QUOTE_NONE)
            ratings = []
            for row in tqdm(reader, total=total_rows, desc="Loading Ratings", unit="rows"):
                ratings.append(Rating(
                    movie_id=row['tconst'],
                    average_rating=float(row['averageRating']),
                    num_votes=int(row['numVotes'])
                ))
                if len(ratings) >= BATCH_SIZE:
                    Rating.objects.bulk_create(ratings, batch_size=BATCH_SIZE)
                    ratings = []
            if ratings:
                Rating.objects.bulk_create(ratings, batch_size=BATCH_SIZE)
