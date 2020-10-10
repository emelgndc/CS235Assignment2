from datetime import date, datetime

from cs235flix.domain.model import User, Movie, Tag, make_review, make_tag_association, ModelException

import pytest


@pytest.fixture()
def movie():
    movie = Movie("Barnacle Boy", 2020)
    movie.director = "John Mack"
    movie.description = "this guy is from spongebob"
    return movie


@pytest.fixture()
def user():
    return User('dbowie', '1234567890')


@pytest.fixture()
def tag():
    return Tag('Spongebob Squarepants')


def test_user_construction(user):
    assert user.user_name == 'dbowie'
    assert user.password == '1234567890'
    assert repr(user) == '<User dbowie>'

    for review in user.reviews:
        # User should have an empty list of Reviews after construction.
        assert False


def test_movie_construction(movie):
    assert movie.title == 'Barnacle Boy'
    assert movie.description == 'this guy is from spongebob'
    assert movie.actors == []
    assert movie.number_of_tags == 0

    assert repr(movie) == '<Movie Barnacle Boy, 2020, []>'


def test_movie_less_than_operator():
    movie_1 = Movie("abc", 2020)

    movie_2 = Movie("def", 2019)

    assert movie_1 < movie_2


def test_tag_construction(tag):
    assert tag.tag_name == 'Spongebob Squarepants'

    for movie in tag.tagged_movies:
        assert False

    assert not tag.is_applied_to(Movie("Barnacle Boy", 2020))


def test_make_review_establishes_relationships(movie, user):
    review_text = 'Barnacle Boy in the USA!'
    review = make_review(movie, review_text, 10, user, datetime.today())

    # Check that the User object knows about the Review.
    assert review in user.reviews

    # Check that the Review knows about the User.
    assert review.user is user

    # Check that Movie knows about the Review.
    assert review in movie.reviews

    # Check that the Review knows about the Movie.
    assert review.movie is movie


def test_make_tag_associations(movie, tag):
    make_tag_association(movie, tag)

    # Check that the Movie knows about the Tag.
    assert movie.is_tagged()
    assert movie.is_tagged_by(tag)

    # check that the Tag knows about the Movie.
    assert tag.is_applied_to(movie)
    assert movie in tag.tagged_movies


def test_make_tag_associations_with_movie_already_tagged(movie, tag):
    make_tag_association(movie, tag)

    with pytest.raises(ModelException):
        make_tag_association(movie, tag)
