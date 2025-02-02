from django.db import models

__all__ = ['Genre', 'MovieType', 'Movie', 'Profession', 'Person', 'Akas', 'Crew', 'Episode', 'Principal', 'Rating']


class Genre(models.Model):
    (action, adult, adventure, animation, biography, comedy, crime, documentary, drama, family, fantasy, film_noir,
     game_show, history, horror, music, musical, mystery, news, reality_tv, romance, sci_fi, short, sport, talk_show,
     thriller, war, western) = range(1, 29)

    choices = (
        (action, 'Action'),
        (adult, 'Adult'),
        (adventure, 'Adventure'),
        (animation, 'Animation'),
        (biography, 'Biography'),
        (comedy, 'Comedy'),
        (crime, 'Crime'),
        (documentary, 'Documentary'),
        (drama, 'Drama'),
        (family, 'Family'),
        (fantasy, 'Fantasy'),
        (film_noir, 'Film-Noir'),
        (game_show, 'Game-Show'),
        (history, 'History'),
        (horror, 'Horror'),
        (music, 'Music'),
        (musical, 'Musical'),
        (mystery, 'Mystery'),
        (news, 'News'),
        (reality_tv, 'Reality-TV'),
        (romance, 'Romance'),
        (sci_fi, 'Sci-Fi'),
        (short, 'Short'),
        (sport, 'Sport'),
        (talk_show, 'Talk-Show'),
        (thriller, 'Thriller'),
        (war, 'War'),
        (western, 'Western'),
    )
    mapped_choices = {k: v for (v, k) in choices}

    id = models.IntegerField(primary_key=True, choices=choices)
    code = models.CharField(unique=True, max_length=20)
    title = models.CharField(max_length=256)

    def __str__(self):
        return self.title


class MovieType(models.Model):
    (no_type, movie, short, video, video_game, tv_short, tv_movie, tv_episode, tv_series, tv_mini_series, tv_special,
     tv_pilot) = range(12)

    choices = (
        (no_type, 'no_type'),
        (movie, 'movie'),
        (short, 'short'),
        (video, 'video'),
        (video_game, 'videoGame'),
        (tv_short, 'tvShort'),
        (tv_movie, 'tvMovie'),
        (tv_episode, 'tvEpisode'),
        (tv_series, 'tvSeries'),
        (tv_mini_series, 'tvMiniSeries'),
        (tv_special, 'tvSpecial'),
        (tv_pilot, 'tvPilot'),
    )
    mapped_choices = {k: v for (v, k) in choices}

    id = models.IntegerField(primary_key=True, choices=choices)
    code = models.CharField(unique=True, max_length=20)
    title = models.CharField(max_length=256)

    def __str__(self):
        return self.title


class Movie(models.Model):
    id = models.CharField(max_length=16, primary_key=True)
    movie_type = models.ForeignKey(MovieType, default=MovieType.no_type, on_delete=models.CASCADE)
    title = models.CharField(max_length=512)
    original_title = models.CharField(max_length=512)
    is_adult = models.BooleanField(default=False)
    year = models.IntegerField(null=True, blank=True)
    end_year = models.IntegerField(null=True, blank=True)
    runtime_minutes = models.IntegerField(null=True, blank=True)
    genres = models.ManyToManyField(Genre, related_name='movies', blank=True)

    def __str__(self):
        return self.title


class Profession(models.Model):
    (accountant, actor, actress, animation_department, archive_footage, archive_sound, art_department, art_director,
     assistant, assistant_director, camera_department, casting_department, casting_director, choreographer,
     cinematographer, composer, costume_department, costume_designer, director, editor, editorial_department,
     electrical_department, executive, legal, location_management, make_up_department, manager, miscellaneous,
     music_artist, music_department, podcaster, producer, production_department, production_designer,
     production_manager, publicist, script_department, set_decorator, sound_department, soundtrack, special_effects,
     stunts, talent_agent, transportation_department, visual_effects, writer) = range(1, 47)

    choices = (
        (accountant, 'accountant'),
        (actor, 'actor'),
        (actress, 'actress'),
        (animation_department, 'animation_department'),
        (archive_footage, 'archive_footage'),
        (archive_sound, 'archive_sound'),
        (art_department, 'art_department'),
        (art_director, 'art_director'),
        (assistant, 'assistant'),
        (assistant_director, 'assistant_director'),
        (camera_department, 'camera_department'),
        (casting_department, 'casting_department'),
        (casting_director, 'casting_director'),
        (choreographer, 'choreographer'),
        (cinematographer, 'cinematographer'),
        (composer, 'composer'),
        (costume_department, 'costume_department'),
        (costume_designer, 'costume_designer'),
        (director, 'director'),
        (editor, 'editor'),
        (editorial_department, 'editorial_department'),
        (electrical_department, 'electrical_department'),
        (executive, 'executive'),
        (legal, 'legal'),
        (location_management, 'location_management'),
        (make_up_department, 'make_up_department'),
        (manager, 'manager'),
        (miscellaneous, 'miscellaneous'),
        (music_artist, 'music_artist'),
        (music_department, 'music_department'),
        (podcaster, 'podcaster'),
        (producer, 'producer'),
        (production_department, 'production_department'),
        (production_designer, 'production_designer'),
        (production_manager, 'production_manager'),
        (publicist, 'publicist'),
        (script_department, 'script_department'),
        (set_decorator, 'set_decorator'),
        (sound_department, 'sound_department'),
        (soundtrack, 'soundtrack'),
        (special_effects, 'special_effects'),
        (stunts, 'stunts'),
        (talent_agent, 'talent_agent'),
        (transportation_department, 'transportation_department'),
        (visual_effects, 'visual_effects'),
        (writer, 'writer'),
    )
    mapped_choices = {k: v for (v, k) in choices}

    id = models.IntegerField(primary_key=True, choices=choices)
    code = models.CharField(unique=True, max_length=32)
    title = models.CharField(max_length=256)


class Person(models.Model):
    id = models.CharField(max_length=16, primary_key=True)
    name = models.CharField(max_length=255)
    birth_year = models.IntegerField(null=True, blank=True)
    death_year = models.IntegerField(null=True, blank=True)
    professions = models.ManyToManyField(Profession, related_name='persons', blank=True)
    movies = models.ManyToManyField(Movie, related_name='persons', blank=True)

    def __str__(self):
        return self.name


class Akas(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    ordering = models.IntegerField()
    title = models.CharField(max_length=512)
    region = models.CharField(max_length=4, blank=True)
    language = models.CharField(max_length=4, blank=True)
    types = models.CharField(max_length=50, blank=True)
    attributes = models.CharField(max_length=255, blank=True)
    is_original_title = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Crew(models.Model):
    movie = models.OneToOneField(Movie, on_delete=models.CASCADE)
    directors = models.ManyToManyField(Person, related_name = 'crew_directors', blank = True)
    writers = models.ManyToManyField(Person, related_name = 'crew_writers', blank = True)

    def __str__(self):
        return f'Crew: {self.movie.title}'


class Episode(models.Model):
    movie = models.OneToOneField(Movie, on_delete=models.CASCADE, related_name='episode')
    parent = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='episodes')
    season_number = models.IntegerField(null=True, blank=True)
    episode_number = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'Episode {self.episode_number}: {self.movie.title}'


class Principal(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    # TODO make as enum
    category = models.CharField(max_length=50)
    # TODO make as enum
    job = models.CharField(max_length=255, blank=True)
    characters = models.CharField(max_length=255, blank=True)
    ordering = models.IntegerField()

    def __str__(self):
        return f'Principal: {self.person.name}'


class Rating(models.Model):
    movie = models.OneToOneField(Movie, on_delete=models.CASCADE, related_name='rating')
    average_rating = models.FloatField()
    num_votes = models.IntegerField()

    def __str__(self):
        return f'{self.movie.title} - {self.average_rating}'
