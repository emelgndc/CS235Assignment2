from datetime import date, datetime
from typing import List

import pytest

from covid.domain.model import Actor, Genre, Director, Movie, User, Tag, Review, make_review
from covid.adapters.repository import RepositoryException


def test_repository_can_add_a_user(in_memory_repo):
    user = User('Picroma', '666666')
    in_memory_repo.add_user(user)

    assert in_memory_repo.get_user('picroma') is user


def test_repository_can_retrieve_a_user(in_memory_repo):
    user = in_memory_repo.get_user('thorke')
    #print(user)
    user2 = User("thorke", "cLQ^C#oFXloS")
    #print(user2)
    assert user == user2


def test_repository_does_not_retrieve_a_non_existent_user(in_memory_repo):
    user = in_memory_repo.get_user('prince')
    assert user is None


def test_repository_can_retrieve_movie_count(in_memory_repo):
    number_of_movies = in_memory_repo.get_number_of_movies()

    # Check that the query returned 30 Movies.
    assert number_of_movies == 30


def test_repository_can_add_movie(in_memory_repo):
    movie = Movie("Arrivaz", 2020)
    in_memory_repo.add_movie(movie)

    assert in_memory_repo.get_movie(31) is movie


def test_repository_can_retrieve_movie(in_memory_repo):
    movie = in_memory_repo.get_movie(1)

    # Check that the Movie has the expected details.
    assert movie.title == "Guardians of the Galaxy"
    assert len(movie.actors) == 4
    assert movie.actors[0].actor_full_name == "Chris Pratt"
    assert movie.director.director_full_name == "James Gunn"
    assert len(movie.genres) == 3
    assert movie.release_year == 2014
    assert movie.description == "A group of intergalactic criminals are forced to work together to stop a fanatical warrior from taking control of the universe."
    assert movie.runtime_minutes == 121

    # Check that the movie is reviewed as expected.
    review_one = [review for review in movie.reviews if review.review_text == 'I LOVE THIS MOVIE!!!'][0]
    review_two = [review for review in movie.reviews if review.review_text == 'doo doo actors'][0]

    assert review_one.user.user_name == 'fmercury'
    assert review_two.user.user_name == "thorke"

    assert review_one.rating == 5
    assert review_two.rating == 1

    # Check that the movie is tagged as expected.
    assert movie.is_tagged_by(Tag('Action'))
    assert movie.is_tagged_by(Tag('Adventure'))
    assert movie.is_tagged_by(Tag('Sci-Fi'))


def test_repository_does_not_retrieve_a_non_existent_movie(in_memory_repo):
    movie = in_memory_repo.get_movie(31)
    assert movie is None


def test_repository_can_retrieve_movies_by_year(in_memory_repo):
    movies = in_memory_repo.get_movies_by_year(2015)

    # Check that the query returned 52 movies.
    assert len(movies) == 1


def test_repository_does_not_retrieve_a_movie_when_there_are_no_movies_for_a_given_year(in_memory_repo):
    movies = in_memory_repo.get_movies_by_year(6969)
    assert len(movies) == 0


def test_repository_can_retrieve_tags(in_memory_repo):
    tags = in_memory_repo.get_tags()
    #print(len(tags))

    assert len(tags) == 16

    tag_one = [tag for tag in tags if tag.tag_name == 'Comedy'][0]
    tag_two = [tag for tag in tags if tag.tag_name == 'Sci-Fi'][0]

    assert tag_one.number_of_tagged_movies == 9
    assert tag_two.number_of_tagged_movies == 5


def test_repository_can_get_first_movie(in_memory_repo):
    movie = in_memory_repo.get_first_movie()
    assert movie.title == 'Guardians of the Galaxy'


def test_repository_can_get_last_movie(in_memory_repo):
    movie = in_memory_repo.get_last_movie()
    assert movie.title == "Assassin's Creed"


def test_repository_can_get_movies_by_ids(in_memory_repo):
    movies = in_memory_repo.get_movies_by_id([1, 4, 5])

    assert len(movies) == 3
    assert movies[0].title == "Guardians of the Galaxy"
    assert movies[1].title == "Sing"
    assert movies[2].title == 'Suicide Squad'


def test_repository_does_not_retrieve_movie_for_non_existent_id(in_memory_repo):
    movies = in_memory_repo.get_movies_by_id([2, 31])

    assert len(movies) == 1
    assert movies[0].title == "Prometheus"


def test_repository_returns_an_empty_list_for_non_existent_ids(in_memory_repo):
    movies = in_memory_repo.get_movies_by_id([0, 31])

    assert len(movies) == 0


def test_repository_returns_movie_ids_for_existing_tag(in_memory_repo):
    movie_ids = in_memory_repo.get_movie_ids_for_tag('Horror')
    #print(len(movie_ids))
    assert movie_ids == [3, 23, 28]


def test_repository_returns_an_empty_list_for_non_existent_tag(in_memory_repo):
    movie_ids = in_memory_repo.get_movie_ids_for_tag('United States')

    assert len(movie_ids) == 0


# def test_repository_returns_year_of_previous_movie(in_memory_repo): #TODO: see if these tests can be refactored
#     movie = in_memory_repo.get_movie(6)
#     previous_date = in_memory_repo.get_date_of_previous_movie(movie)
#
#     assert previous_date.isoformat() == '2020-03-01'


# def test_repository_returns_none_when_there_are_no_previous_movies(in_memory_repo):
#     movie = in_memory_repo.get_movie(1)
#     previous_date = in_memory_repo.get_year_of_previous_movie(movie)
#
#     assert previous_date is None


# def test_repository_returns_date_of_next_movie(in_memory_repo):
#     movie = in_memory_repo.get_movie(3)
#     next_date = in_memory_repo.get_date_of_next_movie(movie)
#
#     assert next_date.isoformat() == '2020-03-05'
#
#
# def test_repository_returns_none_when_there_are_no_subsequent_movies(in_memory_repo):
#     movie = in_memory_repo.get_movie(6)
#     next_date = in_memory_repo.get_date_of_next_movie(movie)
#
#     assert next_date is None


def test_repository_can_add_a_tag(in_memory_repo):
    tag = Tag('Cheese')
    in_memory_repo.add_tag(tag)

    assert tag in in_memory_repo.get_tags()


def test_repository_can_add_a_review(in_memory_repo):
    user = in_memory_repo.get_user('thorke')
    movie = in_memory_repo.get_movie(2)
    review = make_review(movie, "dudududududu", 5, user, datetime.today())

    in_memory_repo.add_review(review)
    print(in_memory_repo.get_reviews())
    assert review in in_memory_repo.get_reviews()


def test_repository_does_not_add_a_review_without_a_user(in_memory_repo):
    movie = in_memory_repo.get_movie(1)
    review = Review(movie, "i love movie hehe xd", 9)

    with pytest.raises(RepositoryException):
        in_memory_repo.add_review(review)


def test_repository_does_not_add_a_review_without_an_movie_properly_attached(in_memory_repo):
    user = in_memory_repo.get_user('thorke')
    movie = in_memory_repo.get_movie(2)
    review = Review(movie, "i love movie hehe xd", 9)

    user.add_review(review)

    with pytest.raises(RepositoryException):
        # Exception expected because the movie doesn't refer to the review.
        in_memory_repo.add_review(review)


def test_repository_can_retrieve_reviews(in_memory_repo):
    #print(in_memory_repo.reviews)
    assert len(in_memory_repo.get_reviews()) == 2



