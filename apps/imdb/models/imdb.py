from django.db import models


__all__ = ['Movie', 'Rating']


class Movie(models.Model):
    imdb_id = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=255)
    original_title = models.CharField(max_length=255)
    is_adult = models.BooleanField(default=False)
    year = models.IntegerField(null=True, blank=True)
    genres = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.title


class Rating(models.Model):
    movie = models.OneToOneField(Movie, on_delete=models.CASCADE, related_name='rating')
    average_rating = models.FloatField()
    num_votes = models.IntegerField()

    def __str__(self):
        return f'{self.movie.title} - {self.average_rating}'
