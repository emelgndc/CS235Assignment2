from typing import Iterable
import random

from covid.adapters.repository import AbstractRepository
from covid.domain.model import Movie


def get_tag_names(repo: AbstractRepository):
    tags = repo.get_tags()
    tag_names = [tag.tag_name for tag in tags]

    return tag_names


def get_random_movies(quantity, repo: AbstractRepository):
    movie_count = repo.get_number_of_movies()

    if quantity >= movie_count:
        # Reduce the quantity of ids to generate if the repository has an insufficient number of articles.
        quantity = movie_count - 1

    # Pick distinct and random articles.
    random_ids = random.sample(range(1, movie_count), quantity)
    movies = repo.get_movies_by_id(random_ids)

    return movies_to_dict(movies)


# ============================================
# Functions to convert dicts to model entities
# ============================================

def movie_to_dict(movie: Movie):
    movie_dict = {
        'year': movie.release_year,
        'title': movie.title,
        #'image_hyperlink': movie.image_hyperlink
    }
    return movie_dict


def movies_to_dict(movies: Iterable[Movie]):
    return [movie_to_dict(movie) for movie in movies]
