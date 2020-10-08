from datetime import datetime

from covid.domain.movie import Movie
from covid.domain.user import User

class Review:
    def __init__(self, movie: Movie, review_text: str, rating: int, user: User):
        #movie
        if type(movie) is not Movie:
            self.__movie = None
        else:
            self.__movie = movie

        #review_text
        if review_text == "" or type(review_text) is not str:
            self.__review_text = None
        else:
            self.__review_text = review_text.strip()

        #rating
        if rating < 1 or rating > 10 or type(rating) is not int:
            self.__rating = None
        else:
            self.__rating = rating

        #timestamp
        self.__timestamp = datetime.today()

        #user
        self.__user = user

    @property
    def movie(self):
        return self.__movie

    @property
    def review_text(self):
        return self.__review_text

    @property
    def rating(self):
        return self.__rating

    @property
    def user(self):
        return self.__user

    @property
    def timestamp(self):
        return self.__timestamp

    def __repr__(self):
        return f"{self.__movie}, {self.__timestamp}"

    def __eq__(self, other):
        return (self.__movie, self.__review_text, self.__rating, self.__timestamp) == (other.__movie, other.__review_text, other.__rating, other.__timestamp)
