import csv
import os
from datetime import date, datetime
from typing import List

from bisect import bisect, bisect_left, insort_left

from werkzeug.security import generate_password_hash

from covid.adapters.repository import AbstractRepository, RepositoryException
from covid.domain.model import Tag, Comment, make_tag_association, make_comment
from covid.domain.actor import Actor
from covid.domain.director import Director
from covid.domain.genre import Genre
from covid.domain.movie import Movie
from covid.domain.review import Review
from covid.domain.user import User
from covid.domain.watchlist import WatchList
from covid.datafilereaders.movie_file_csv_reader import MovieFileCSVReader

class MemoryRepository(AbstractRepository):

    def __init__(self):
        self._movies = list()
        #self._movies_index = dict()
        self._tags = list()
        self._users = list()
        self._comments = list()

    def add_user(self, user: User):
        self._users.append(user)

    def get_user(self, username) -> User:
        return next((user for user in self._users if user.username == username), None)

    def add_movie(self, movie: Movie):
        insort_left(self._movies, movie)
        self._movies_index[movie.id] = movie

    def get_movie(self, id: int) -> Movie:
        movie = None

        try:
            movie = self._movies_index[id]
        except KeyError:
            pass  # Ignore exception and return None.

        return movie

    # def get_movies_by_date(self, target_date: date) -> List[Movie]:
    #     target_movie = Movie( ***note that order of movies dataset is rank***
    #         date=target_date,
    #         title=None,
    #         first_para=None,
    #         hyperlink=None,
    #         image_hyperlink=None
    #     )
    #     matching_movies = list()
    #
    #     try:
    #         index = self.movie_index(target_movie)
    #         for movie in self._movies[index:None]:
    #             if movie.date == target_date:
    #                 matching_movies.append(movie)
    #             else:
    #                 break
    #     except ValueError:
    #         # No movies for specified id. Simply return an empty list.
    #         pass
    #
    #     return matching_movies

    def get_number_of_movies(self):
        return len(self._movies)

    def get_first_movie(self):
        movie = None

        if len(self._movies) > 0:
            movie = self._movies[0]
        return movie

    def get_last_movie(self):
        movie = None

        if len(self._movies) > 0:
            movie = self._movies[-1]
        return movie

    def get_movies_by_id(self, id_list):
        # Strip out any ids in id_list that don't represent movie ids in the repository.
        existing_ids = [id for id in id_list if id in self._movies_index]

        # Fetch the movies.
        movies = [self._movies_index[id] for id in existing_ids]
        return movies

    def get_movie_ids_for_tag(self, tag_name: str):
        # Linear search, to find the first occurrence of a Tag with the name tag_name.
        tag = next((tag for tag in self._tags if tag.tag_name == tag_name), None)

        # Retrieve the ids of movies associated with the Tag.
        if tag is not None:
            movie_ids = [movie.id for movie in tag.tagged_movies]
        else:
            # No Tag with name tag_name, so return an empty list.
            movie_ids = list()

        return movie_ids

    # def get_date_of_previous_movie(self, movie: Movie):
    #     previous_date = None
    #
    #     try:
    #         index = self.movie_index(movie)
    #         for stored_movie in reversed(self._movies[0:index]):
    #             if stored_movie.date < movie.date:
    #                 previous_date = stored_movie.date
    #                 break
    #     except ValueError:
    #         # No earlier movies, so return None.
    #         pass
    #
    #     return previous_date
    #
    # def get_date_of_next_movie(self, movie: movie):
    #     next_date = None
    #
    #     try:
    #         index = self.movie_index(movie)
    #         for stored_movie in self._movies[index + 1:len(self._movies)]:
    #             if stored_movie.date > movie.date:
    #                 next_date = stored_movie.date
    #                 break
    #     except ValueError:
    #         # No subsequent movies, so return None.
    #         pass
    #
    #     return next_date

    def add_tag(self, tag: Tag):
        self._tags.append(tag)

    def get_tags(self) -> List[Tag]:
        return self._tags

    def add_review(self, review: Review):
        super().add_review(review)
        self._comments.append(review)

    def get_reviews(self):
        return self._reviews

    # Helper method to return movie index.
    def movie_index(self, movie: Movie):
        index = bisect_left(self._movies, movie)
        if index != len(self._movies) and self._movies[index].date == movie.date:
            return index
        raise ValueError


def read_csv_file(filename: str):
    with open(filename, encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)

        # Read first line of the the CSV file.
        headers = next(reader)

        # Read remaining rows from the CSV file.
        for row in reader:
            # Strip any leading/trailing white space from data read.
            row = [item.strip() for item in row]
            yield row


def load_movies_and_tags(data_path: str, repo: MemoryRepository):
    tags = dict()
    csv = MovieFileCSVReader("Data1000Movies.csv")

    csv.read_csv_file()
    alltags = csv.dataset_of_actors.extend(csv.dataset_of_directors).extend(csv.dataset_of_genres)
    alltagsV2 = []

    for movie in csv.dataset_of_movies:
        repo.add_movie(movie)
        for genre in movie.genres:
            make_tag_association(movie, genre)


    for tag in alltags:

    # for data_row in csv.read_csv_file():
    #
    #     movie_id = int(data_row[0])
    #     number_of_tags = len(data_row) - 6
    #     movie_tags = data_row[-number_of_tags:]
    #
    #     # Add any new tags; associate the current movie with tags.
    #     for tag in movie_tags:
    #         if tag not in tags.keys():
    #             tags[tag] = list()
    #         tags[tag].append(movie_id)
    #     del data_row[-number_of_tags:]
    #
    #     # Create movie object.
    #     movie = movie(
    #         date=date.fromisoformat(data_row[1]),
    #         title=data_row[2],
    #         first_para=data_row[3],
    #         hyperlink=data_row[4],
    #         image_hyperlink=data_row[5],
    #         id=movie_key
    #     )
    #
    #     # Add the movie to the repository.
    #     repo.add_movie(movie)
    #
    # # Create Tag objects, associate them with movies and add them to the repository.
    # for tag_name in tags.keys():
    #     tag = Tag(tag_name)
    #     for movie_id in tags[tag_name]:
    #         movie = repo.get_movie(movie_id)
    #         make_tag_association(movie, tag)
    #     repo.add_tag(tag)


def load_users(data_path: str, repo: MemoryRepository):
    users = dict()

    for data_row in read_csv_file(os.path.join(data_path, 'users.csv')):
        user = User(
            username=data_row[1],
            password=generate_password_hash(data_row[2])
        )
        repo.add_user(user)
        users[data_row[0]] = user
    return users


def load_comments(data_path: str, repo: MemoryRepository, users):
    for data_row in read_csv_file(os.path.join(data_path, 'comments.csv')):
        comment = make_comment(
            comment_text=data_row[3],
            user=users[data_row[1]],
            movie=repo.get_movie(int(data_row[2])),
            timestamp=datetime.fromisoformat(data_row[4])
        )
        repo.add_comment(comment)


def populate(data_path: str, repo: MemoryRepository):
    # Load movies and tags into the repository.
    load_movies_and_tags(data_path, repo)

    # Load users into the repository.
    users = load_users(data_path, repo)

    # Load comments into the repository.
    load_comments(data_path, repo, users)
