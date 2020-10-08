from covid.domain.genre import Genre
from covid.domain.actor import Actor
from covid.domain.director import Director
from covid.domain.model import Tag
from typing import Iterable


class Movie:
    def __init__(self, title: str, release_year: int):
        if title == "" or type(title) is not str:
            self.__title = None
        else:
            self.__title = title.strip()

        if release_year < 1900 or type(release_year) is not int:
            self.__release_year = None
        else:
            self.__release_year = release_year

        self.__director = None
        self.__description = ""
        self.__actors = []
        self.__genres = []
        self._tags = []
        self.__runtime_minutes = 0

    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, title: str):
        if type(title) is str:
            self.__title = title.strip()

    @property
    def release_year(self) -> int:
        return self.__release_year

    @release_year.setter
    def release_year(self, release_year: int):
        if type(release_year) is int:
            if release_year >= 1900:
                self.__release_year = release_year

    @property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, description: str):
        if type(description) is str:
            self.__description = description.strip()

    @property
    def director(self) -> str:
        return self.__director

    @director.setter
    def director(self, director: Director):
        if type(director) is Director:
            self.__director = director

    @property
    def actors(self) -> list:
        return self.__actors

    @actors.setter
    def actors(self, actors: list):
        allactors = True
        if type(actors) is list:
            for i in actors:
                if type(i) is not Actor:
                    allactors = False
            if allactors:
                self.__actors = actors

    @property
    def genres(self) -> list:
        return self.__genres

    @genres.setter
    def genres(self, genres: list):
        allgenres = True
        if type(genres) is list:
            for i in genres:
                if type(i) is not Genre:
                    allgenres = False
            if allgenres:
                self.__genres = genres

    @property
    def runtime_minutes(self) -> int:
        return self.__runtime_minutes

    @runtime_minutes.setter
    def runtime_minutes(self, num: int):
        if type(num) is int:
            if num > 0:
                self.__runtime_minutes = num
            else:
                raise ValueError
        else:
            raise ValueError

    @property
    def number_of_tags(self) -> int:
        return len(self._tags)

    @property
    def tags(self) -> Iterable['Tag']:
        return iter(self._tags)

    def is_tagged_by(self, tag: 'Tag'):
        return tag in self._tags

    def is_tagged(self) -> bool:
        return len(self._tags) > 0

    def add_tag(self, tag: 'Tag'):
        self._tags.append(tag)

    def add_actor(self, actor: Actor):
        if type(actor) is Actor:
            self.__actors.append(actor)

    def remove_actor(self, actor: Actor):
        if actor in self.__actors:
            self.__actors.remove(actor)

    def add_genre(self, genre: Genre):
        if type(genre) is Genre:
            self.__genres.append(genre)

    def remove_genre(self, genre: Genre):
        if genre in self.__genres:
            self.__genres.remove(genre)
        
    def __repr__(self):
        return f"<Movie {self.__title}, {self.__release_year}>"

    def __eq__(self, other):
        return self.__title == other.__title and self.__release_year == other.__release_year

    def __lt__(self, other):
        if self.__title == other.__title:
            return self.__release_year < other.__release_year
        else:
            return self.title < other.title

    def __hash__(self):
        return hash((self.__title, self.__release_year))
