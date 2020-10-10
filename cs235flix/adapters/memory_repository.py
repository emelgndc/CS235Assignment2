import os
import csv
from datetime import date, datetime
from typing import List

from bisect import bisect, bisect_left, insort_left

from werkzeug.security import generate_password_hash

from cs235flix.adapters.repository import AbstractRepository, RepositoryException
from cs235flix.domain.model import Actor, Director, Genre, Movie, Review, User, Tag, make_tag_association, make_review
from cs235flix.datafilereaders.movie_file_csv_reader import MovieFileCSVReader


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
        for i in range(len(self._users)):
            if self._users[i].user_name == username:
                user = self._users[i]
                break
        return user

    def get_user_by_id(self, id) -> User:
        user = None
        for i in range(len(self._users)):
            if self._users[i].id == id:
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

        return movie_ids

    def get_movie_ids_for_actor(self, name: str):
        movies = []
        for movie in self._movies:
            for actor in movie.actors:
                if actor.actor_full_name == name:
                    movies.append(movie)
                    break

        if movies is not []:
            movie_ids = [self.movie_index(movie) for movie in movies]
        else:
            movie_ids = list()

        return movie_ids

    def get_movie_ids_for_director(self, name: str):
        movies = []
        for movie in self._movies:
            if movie.director.director_full_name == name:
                movies.append(movie)

        if movies is not []:
            movie_ids = [self.movie_index(movie) for movie in movies]
        else:
            movie_ids = list()

        return movie_ids

    def add_tag(self, tag: Tag):
        self._tags.append(tag)

    def get_tags(self) -> List[Tag]:
        return self._tags

    def add_review(self, review: Review):
        super().add_review(review)
        self._reviews.append(review)

    def get_reviews(self):
        return self._reviews

    def get_reviews_for_user(self, user_name):
        user = self.get_user(user_name)
        return user.reviews

    def get_review_num_of_user(self, user_name):
        user = self.get_user(user_name)
        return len(user.reviews)

    def get_friends_for_user(self, user_name):
        user = self.get_user(user_name)
        return user.friends

    def get_pending_friends_for_user(self, user_name):
        user = self.get_user(user_name)
        return user.pending_friends

    def get_watched(self, user_name):
        user = self.get_user(user_name)
        return user.watched_movies

    #def add_watched(self, user_name, movie: Movie):
    #    user = self.get_user(user_name)
    #    user.watch_movie(movie)

    def get_watched_ids(self, user_name):
        user = self.get_user(user_name)
        return user.watched_ids

    def add_watched_ids(self, user_name, movie: Movie, id: int):
        user = self.get_user(user_name)
        user.watch_movie(movie, id)

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
    file = MovieFileCSVReader(data_path + "/movies.csv")

    file.read_csv_file()

    # Add movies to repo, and create tag associations
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

        friends_ids = data_row[3].split(",")
        if friends_ids == ['']:
            pass
        else:
            user.friends_ids = friends_ids

        pending_ids = data_row[4].split(",")
        if pending_ids == ['']:
            pass
        else:
            user.pending_friends_ids = pending_ids

        user.id = int(data_row[0])
        repo.add_user(user)
        users[data_row[0]] = user

        watched_ids = data_row[5].split(",")
        if watched_ids == ['']:
            pass
        else:
            int_ids = [int(x) for x in watched_ids]
            user.watched_ids = int_ids
            user.watched_movies = repo.get_movies_by_id(int_ids)

    for key in users:
        user = users[key]
        friends = []
        pending = []
        for id in user.friends_ids:
            friends.append(repo.get_user_by_id(int(id)))
        for id2 in user.pending_friends_ids:
            pending.append(repo.get_user_by_id(int(id2)))
        user.friends = friends
        user.pending_friends = pending

    return users


def load_reviews(data_path: str, repo: MemoryRepository, users):
    for data_row in read_csv_file(os.path.join(data_path, 'reviews.csv')):
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
