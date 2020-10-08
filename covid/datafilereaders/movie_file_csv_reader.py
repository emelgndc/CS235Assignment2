import csv

from covid.domain.movie import Movie
from covid.domain.actor import Actor
from covid.domain.genre import Genre
from covid.domain.director import Director


class MovieFileCSVReader:

    def __init__(self, file_name: str):
        self.__file_name = file_name
        self.__dataset_of_movies = set([])
        self.__dataset_of_actors = set([])
        self.__dataset_of_directors = set([])
        self.__dataset_of_genres = set([])

    def read_csv_file(self):
        with open(self.__file_name, mode='r', encoding='utf-8-sig') as csvfile:
            movie_file_reader = csv.DictReader(csvfile)

            index = 0
            for row in movie_file_reader:
                title = row['Title']
                release_year = int(row['Year'])
                movie = Movie(title, release_year)

                actors1 = row['Actors'].split(",")
                actors2 = []
                for i in actors1:
                    actors2.append(Actor(i))

                director = Director(row['Director'])

                genres1 = row['Genre'].split(",")
                genres2 = []
                for i in genres1:
                    genres2.append(Genre(i))

                self.__dataset_of_movies.add(movie)

                for actor in actors2:
                    self.__dataset_of_actors.add(actor)

                self.__dataset_of_directors.add(director)

                for genre in genres2:
                    self.__dataset_of_genres.add(genre)

                index += 1

    @property
    def dataset_of_movies(self):
        return self.__dataset_of_movies

    @property
    def dataset_of_actors(self):
        return self.__dataset_of_actors

    @property
    def dataset_of_directors(self):
        return self.__dataset_of_directors

    @property
    def dataset_of_genres(self):
        return self.__dataset_of_genres
