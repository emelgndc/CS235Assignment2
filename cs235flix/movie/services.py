from typing import List, Iterable

from cs235flix.adapters.repository import AbstractRepository
from cs235flix.domain.model import make_review, Movie, Review, Tag


class NonExistentMovieException(Exception):
    pass


class UnknownUserException(Exception):
    pass


def add_review(movie_id: int, review_text: str, rating: int, user_name: str, repo: AbstractRepository):
    # Check that the review exists.
    movie = repo.get_movie(movie_id)
    if movie is None:
        raise NonExistentMovieException

    user = repo.get_user(user_name)
    if user is None:
        raise UnknownUserException

    # Create review.
    review = make_review(movie, review_text, rating, user, None)

    # Update the repository.
    repo.add_review(review)


def get_movie(movie_id: int, repo: AbstractRepository):
    movie = repo.get_movie(movie_id)

    if movie is None:
        raise NonExistentMovieException

    return movie_to_dict(movie, movie_id)


def get_first_movie(repo: AbstractRepository):

    movie = repo.get_movie(1)

    return movie_to_dict(movie)


def get_last_movie(repo: AbstractRepository):

    movie = repo.get_movie(repo.get_number_of_movies())
    return movie_to_dict(movie)

#TODO: this stuff

# def get_movies_by_genre(date, repo: AbstractRepository):
#     # Returns movies for the target date (empty if no matches), the date of the previous movie (might be null), the date of the next movie (might be null)
#
#     movies = repo.get_movies_by_date(target_date=date)
#
#     movies_dto = list()
#     prev_date = next_date = None
#
#     if len(movies) > 0:
#         prev_date = repo.get_date_of_previous_movie(movies[0])
#         next_date = repo.get_date_of_next_movie(movies[0])
#
#         # Convert Movies to dictionary form.
#         movies_dto = movies_to_dict(movies)
#
#     return movies_dto, prev_date, next_date


def get_movie_ids_for_tag(tag_name, repo: AbstractRepository):
    movie_ids = repo.get_movie_ids_for_tag(tag_name)

    return movie_ids


def get_movies_by_id(id_list, repo: AbstractRepository):
    movies = repo.get_movies_by_id(id_list)

    # Convert Movies to dictionary form.
    movies_as_dict = movies_to_dict(movies)

    return movies_as_dict


def get_reviews_for_movie(movie_id, repo: AbstractRepository):
    movie = repo.get_movie(movie_id)

    if movie is None:
        raise NonExistentMovieException

    return reviews_to_dict(movie.reviews, movie_id)


# ============================================
# Functions to convert model entities to dicts
# ============================================

def movie_to_dict(movie: Movie, movie_id: int):
    movie_dict = {
        'id': movie_id,
        'year': movie.release_year,
        'title': movie.title,
        'description': movie.description,
        'director': movie.director,
        'actors': movie.actors,
        'length': movie.runtime_minutes,
        'reviews': reviews_to_dict(movie.reviews),
        'tags': tags_to_dict(movie.tags)
    }
    return movie_dict


def movies_to_dict(movies: Iterable[Movie], movie_id: int):
    return [movie_to_dict(movie, movie_id) for movie in movies]


def review_to_dict(review: Review, movie_id: int):
    review_dict = {
        'username': review.user.user_name,
        'movie_id': movie_id,
        'review_text': review.review_text,
        'rating': review.rating,
        'timestamp': review.timestamp
    }
    return review_dict


def reviews_to_dict(reviews: Iterable[Review], movie_id: int):
    return [review_to_dict(review, movie_id) for review in reviews]


def tag_to_dict(tag: Tag):
    tag_dict = {
        'name': tag.tag_name,
        'tagged_movies': [movie.id for movie in tag.tagged_movies]
    }
    return tag_dict


def tags_to_dict(tags: Iterable[Tag]):
    return [tag_to_dict(tag) for tag in tags]


# ============================================
# Functions to convert dicts to model entities
# ============================================

def dict_to_movie(dict):
    movie = Movie(dict.title, dict.year)
    # Note there's no reviews or tags.
    return movie
