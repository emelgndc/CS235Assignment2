from werkzeug.security import generate_password_hash, check_password_hash

from cs235flix.adapters.repository import AbstractRepository
from cs235flix.domain.model import User
from cs235flix.movie.services import movie_to_dict, movies_to_dict


class NameNotUniqueException(Exception):
    pass


class UnknownUserException(Exception):
    pass


class AuthenticationException(Exception):
    pass


def add_user(user_name: str, password: str, repo: AbstractRepository):
    # Check that the given username is available.
    user = repo.get_user(user_name)
    if user is not None:
        raise NameNotUniqueException

    # Encrypt password so that the database doesn't store passwords 'in the clear'.
    password_hash = generate_password_hash(password)

    # Create and store the new User, with password encrypted.
    user = User(user_name, password_hash)
    repo.add_user(user)


def get_user(user_name: str, repo: AbstractRepository):
    user = repo.get_user(user_name)
    if user is None:
        raise UnknownUserException

    return user_to_dict(user)


def get_friends_of_user(user_name: str, repo: AbstractRepository):
    user = repo.get_user(user_name)
    if user is None:
        raise UnknownUserException
    return friends_to_dict(user.friends)


def get_review_num_of_user(user_name: str, repo: AbstractRepository):
    user = repo.get_user(user_name)
    if user is None:
        raise UnknownUserException
    return repo.get_review_num_of_user(user)


def authenticate_user(user_name: str, password: str, repo: AbstractRepository):
    authenticated = False

    user = repo.get_user(user_name)
    if user is not None:
        authenticated = check_password_hash(user.password, password)
    if not authenticated:
        raise AuthenticationException


def get_watched(user_name: str, repo: AbstractRepository):
    id_list = repo.get_watched_ids(user_name)
    watched = repo.get_watched(user_name)

    #return movies_to_dict(watched, id_list, repo)
    return id_list


def add_watched(user_name: str, id: int, repo: AbstractRepository):
    movie = repo.get_movie(id)
    repo.add_watched_ids(user_name, movie, id)

# ===================================================
# Functions to convert model entities to dictionaries
# ===================================================

def user_to_dict(user: User):
    user_dict = {
        'user_name': user.user_name,
        'password': user.password,
        'friends': user.friends,
        'friendnum': user.number_of_friends,
        'reviews': user.reviews,
        'watched_movies': user.watched_movies
    }
    return user_dict


def friend_to_dict(friend: User):
    friend_dict = {
        'user_name': friend.user_name
    }
    return friend_dict


def friends_to_dict(friends: list):
    returnlist = []
    for friend in friends:
        returnlist.append(friend_to_dict(friend))
    return returnlist
