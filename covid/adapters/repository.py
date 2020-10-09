import abc
from typing import List
from datetime import date

from covid.domain.model import Actor, Director, Genre, Movie, Review, User, Tag


repo_instance = None


class RepositoryException(Exception):

    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_user(self, user: User):
        """" Adds a User to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, username) -> User:
        """ Returns the User named username from the repository.

        If there is no User with the given username, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_movie(self, movie: Movie):
        """ Adds an movie to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie(self, id: int) -> Movie:
        """ Returns movie with id from the repository.

        If there is no movie with given id, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_year(self, year: int) -> List[Movie]:
        """ Returns a list of movies that were published in year.

        If there are no movies on the given date, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_movies(self):
        """ Returns the number of movies in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_first_movie(self) -> Movie:
        """ Returns the first movie, alphabetically ordered, from the repository.

        Returns None if the repository is empty.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_last_movie(self) -> Movie:
        """ Returns the last movie, alphabetically ordered, from the repository.

        Returns None if the repository is empty.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_id(self, id_list):
        """ Returns a list of movies, whose ids match those in id_list, from the repository.

        If there are no matches, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie_ids_for_tag(self, tag_name: str):
        """ Returns a list of ids representing movies that are tagged by tag_name.

        If there are no movies that are tagged by tag_name, this method returns an empty list.
        """
        raise NotImplementedError

    # @abc.abstractmethod
    # def get_date_of_previous_movie(self, movie: Movie):
    #     """ Returns the date of an movie that immediately precedes movie.
    #
    #     If movie is the first movie in the repository, this method returns None because there are no movies
    #     on a previous date.
    #     """
    #     raise NotImplementedError
    #
    # @abc.abstractmethod
    # def get_date_of_next_movie(self, movie: Movie):
    #     """ Returns the date of an movie that immediately follows movie (i.e. lower rank).
    #
    #     If movie is the last movie in the repository, this method returns None because there are no movies
    #     on a later date.
    #     """
    #     raise NotImplementedError

    @abc.abstractmethod
    def add_tag(self, tag: Tag):
        """ Adds a Tag to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_tags(self) -> List[Tag]: #just put all of directors/actors/genres into tags list. search by movie OR tag.
        """ Returns the Tags stored in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, review: Review):
        """ Adds a review to the repository.

        If the Review doesn't have bidirectional links with a Movie and a User, this method raises a
        RepositoryException and doesn't update the repository.
        """
        if review.user is None or review not in review.user.reviews:
            raise RepositoryException('Review not correctly attached to a User')
        if review.movie is None or review not in review.movie.reviews:
            raise RepositoryException('Review not correctly attached to an Movie')

    @abc.abstractmethod
    def get_reviews(self):
        """ Returns the reviews stored in the repository. """
        raise NotImplementedError







