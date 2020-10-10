from datetime import date

import pytest

from cs235flix.authentication.services import AuthenticationException
from cs235flix.movie import services as movie_services
from cs235flix.authentication import services as auth_services
from cs235flix.movie.services import NonExistentMovieException


def test_can_add_user(in_memory_repo):
    new_username = 'jz'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    user_as_dict = auth_services.get_user(new_username, in_memory_repo)
    assert user_as_dict['user_name'] == new_username

    # Check that password has been encrypted.
    assert user_as_dict['password'].startswith('pbkdf2:sha256:')


def test_cannot_add_user_with_existing_name(in_memory_repo):
    username = 'thorke'
    password = 'abcd1A23'

    with pytest.raises(auth_services.NameNotUniqueException):
        auth_services.add_user(username, password, in_memory_repo)


def test_authentication_with_valid_credentials(in_memory_repo):
    new_username = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    try:
        auth_services.authenticate_user(new_username, new_password, in_memory_repo)
    except AuthenticationException:
        assert False


def test_authentication_with_invalid_credentials(in_memory_repo):
    new_username = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    with pytest.raises(auth_services.AuthenticationException):
        auth_services.authenticate_user(new_username, '0987654321', in_memory_repo)


def test_can_add_review(in_memory_repo):
    movie_id = 3
    rating = 5
    review_text = 'The loonies are stripping the supermarkets bare!'
    username = 'fmercury'

    # Call the service layer to add the review.
    movie_services.add_review(movie_id, review_text, rating, username, in_memory_repo)

    # Retrieve the reviews for the movie from the repository.
    reviews_as_dict = movie_services.get_reviews_for_movie(movie_id, in_memory_repo)

    # Check that the reviews include a review with the new review text.
    assert next(
        (dictionary['review_text'] for dictionary in reviews_as_dict if dictionary['review_text'] == review_text),
        None) is not None


def test_cannot_add_review_for_non_existent_movie(in_memory_repo):
    movie_id = 31
    rating = 5
    review_text = "COVID-19 - what's that?"
    username = 'fmercury'

    # Call the service layer to attempt to add the review.
    with pytest.raises(movie_services.NonExistentMovieException):
        movie_services.add_review(movie_id, review_text, rating, username, in_memory_repo)


def test_cannot_add_review_by_unknown_user(in_memory_repo):
    movie_id = 3
    rating = 5
    review_text = 'The loonies are stripping the supermarkets bare!'
    username = 'gmichael'

    # Call the service layer to attempt to add the review.
    with pytest.raises(movie_services.UnknownUserException):
        movie_services.add_review(movie_id, review_text, rating, username, in_memory_repo)


def test_can_get_movie(in_memory_repo):
    movie_id = 2

    movie_as_dict = movie_services.get_movie(movie_id, in_memory_repo)

    assert movie_as_dict['id'] == movie_id
    assert movie_as_dict['year'] == 2012
    assert movie_as_dict['title'] == 'Prometheus'
    assert movie_as_dict['description'] == 'Following clues to the origin of mankind, a team finds a structure on a distant moon, but they soon realize they are not alone.'
    assert movie_as_dict['director'].director_full_name == 'Ridley Scott'
    assert movie_as_dict['actors'][0].actor_full_name == "Noomi Rapace"
    assert len(movie_as_dict['reviews']) == 2

    tag_names = [dictionary['name'] for dictionary in movie_as_dict['tags']]
    assert 'Adventure' in tag_names
    assert 'Mystery' in tag_names
    assert 'Sci-Fi' in tag_names


def test_cannot_get_movie_with_non_existent_id(in_memory_repo):
    movie_id = 31

    # Call the service layer to attempt to retrieve the Movie.
    with pytest.raises(movie_services.NonExistentMovieException):
        movie_services.get_movie(movie_id, in_memory_repo)


def test_get_first_movie(in_memory_repo):
    movie_as_dict = movie_services.get_first_movie(in_memory_repo)

    assert movie_as_dict['id'] == 1


def test_get_last_movie(in_memory_repo):
    movie_as_dict = movie_services.get_last_movie(in_memory_repo)

    assert movie_as_dict['id'] == 30


def test_get_movies_by_tag(in_memory_repo):
    target_tag = "Action"

    id_list = movie_services.get_movie_ids_for_tag(target_tag, in_memory_repo)
    as_dict = movie_services.get_movies_by_id(id_list, in_memory_repo)

    assert len(id_list) == 10
    assert as_dict[0]['id'] == 1
    assert as_dict[0]['title'] == "Guardians of the Galaxy"
    assert as_dict[len(as_dict)-1]['id'] == 30


def test_get_movies_by_tag_with_non_existent_tag(in_memory_repo):
    target_tag = 'Banana'

    id_list = movie_services.get_movie_ids_for_tag(target_tag, in_memory_repo)
    as_dict = movie_services.get_movies_by_id(id_list, in_memory_repo)

    # Check that there are no movies dated 2020-03-06.
    assert len(as_dict) == 0


def test_get_movies_by_id(in_memory_repo):
    target_movie_ids = [5, 6, 7, 8]
    as_dict = movie_services.get_movies_by_id(target_movie_ids, in_memory_repo)

    # Check that 4 movies were returned from the query.
    assert len(as_dict) == 4

    # Check that the movie ids returned were 5 and 6.
    movie_ids = [movie['id'] for movie in as_dict]
    assert set([5, 6, 7, 8]).issubset(movie_ids)
    assert as_dict[0]['title'] == "Suicide Squad"


def test_get_reviews_for_movie(in_memory_repo):
    reviews_as_dict = movie_services.get_reviews_for_movie(2, in_memory_repo)

    # Check that 2 reviews were returned for movie with id 2.
    assert len(reviews_as_dict) == 2

    assert reviews_as_dict[1]['username'] == 'thorke'

    # Check that the reviews relate to the movie whose id is 2.
    movie_ids = [review['movie_id'] for review in reviews_as_dict]
    movie_ids = set(movie_ids)
    assert 2 in movie_ids and len(movie_ids) == 1


def test_get_reviews_for_non_existent_movie(in_memory_repo):
    with pytest.raises(NonExistentMovieException):
        reviews_as_dict = movie_services.get_reviews_for_movie(31, in_memory_repo)


def test_get_reviews_for_movie_without_reviews(in_memory_repo):
    reviews_as_dict = movie_services.get_reviews_for_movie(3, in_memory_repo)
    assert len(reviews_as_dict) == 0

