import os
import csv
from datetime import date, datetime
from typing import List

from bisect import bisect, bisect_left, insort_left

from werkzeug.security import generate_password_hash

from covid.adapters.repository import AbstractRepository, RepositoryException
from covid.domain.model import Actor, Director, Genre, Movie, Review, User, Tag, make_tag_association, make_review
from covid.datafilereaders.movie_file_csv_reader import MovieFileCSVReader


class MemoryRepository(AbstractRepository):

    def __init__(self):
        self._movies = list() #alphabetical
        self._movies_index = dict() #key=rank, value=movie name
        self._tags = list()
        self._users = list()
        self._reviews = list()

    def add_user(self, user: User):
        self._users.append(user)

    def get_user(self, username) -> User:
        user = None
        #print(self._users)
        for i in range(len(self._users)):
            if self._users[i].user_name == username:
                user = self._users[i]
                break
        return user

    def add_movie(self, movie: Movie):
        insort_left(self._movies, movie)  # inserts alphabetically
        self._movies_index[len(self._movies)] = movie

    def get_movie(self, id: int) -> Movie:
        movie = None

        try:
            movie = self._movies_index[id]
        except KeyError:
            pass  # Ignore exception and return None.

        return movie

    def get_movies_by_year(self, year: int):
        # target_movie = Movie(
        #     date=target_date,
        #     title=None,
        #     first_para=None,
        #     hyperlink=None,
        #     image_hyperlink=None
        # )
        matching_movies = list()

        for movie in self._movies:
            if movie.release_year == year:
                matching_movies.append(movie)

        return matching_movies

    def get_number_of_movies(self):
        return len(self._movies)

    def get_first_movie(self):
        movie = None

        if len(self._movies) > 0:
            movie = self._movies_index[1]
        return movie

    def get_last_movie(self):
        movie = None

        if len(self._movies) > 0:
            movie = self._movies_index[self.get_number_of_movies()]
        return movie

    def get_movies_by_id(self, id_list):
        # Strip out any ids in id_list that don't represent movie ids in the repository.
        movie_ids = [id for id in id_list if id in self._movies_index]
        # Fetch the movies.
        movies = [self._movies_index[id] for id in movie_ids]
        return movies

    def get_movie_ids_for_tag(self, tag_name: str):
        # Linear search, to find the first occurrence of a Tag with the name tag_name.
        try:
            tag = [tag for tag in self._tags if tag.tag_name == tag_name][0]
        except IndexError:
            return []

        # Retrieve the ids of movies associated with the Tag.
        if tag is not None:
            # movies = [movie for movie in tag.tagged_movies]
            # movie_ids = []
            # for mov in movies:
            #     movie_ids.append(self._movies.index(mov))
            movie_ids = [self.movie_index(movie) for movie in tag.tagged_movies]

        else:
            # No Tag with name tag_name, so return an empty list.
            movie_ids = list()

        #return sorted(movie_ids)
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
        self._reviews.append(review)

    def get_reviews(self):
        return self._reviews

    # Helper method to return movie index.
    def movie_index(self, movie: Movie):
        for id in self._movies_index:
            if self._movies_index[id] == movie:
                return id
        return ValueError



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
    file = MovieFileCSVReader(data_path + "/Data1000Movies.csv")
    #file = MovieFileCSVReader(data_path + "/Data30MoviesTEST.csv")

    file.read_csv_file()

    # Add movies to repo, and create tag associations TODO: are tags for actors/directors needed?
    for movie in file.dataset_of_movies:
        repo.add_movie(movie)
        for genre in movie.genres:
            tags = [tag for tag in repo.get_tags() if tag.tag_name == genre.genre_name]
            if len(tags) == 0:
                newtag = Tag(genre.genre_name)
                repo.add_tag(newtag)
                make_tag_association(movie, newtag)
            else:
                existingtag = tags[0]
                make_tag_association(movie, existingtag)


def load_users(data_path: str, repo: MemoryRepository):
    users = dict()

    for data_row in read_csv_file(os.path.join(data_path, 'users.csv')):
        user = User(
            user_name=data_row[1],
            password=generate_password_hash(data_row[2])
        )
        repo.add_user(user)
        users[data_row[0]] = user
    return users


def load_reviews(data_path: str, repo: MemoryRepository, users):
    for data_row in read_csv_file(os.path.join(data_path, 'comments.csv')):
        review = make_review(
            movie=repo.get_movie(int(data_row[2])),
            review_text=data_row[3],
            rating=int(data_row[4]),
            user=users[data_row[1]],
            timestamp=datetime.fromisoformat(data_row[5])
        )

        repo.add_review(review)


def populate(data_path: str, repo: MemoryRepository):
    # Load movies and tags into the repository.
    load_movies_and_tags(data_path, repo)

    # Load users into the repository.
    users = load_users(data_path, repo)

    # Load reviews into the repository.
    load_reviews(data_path, repo, users)
