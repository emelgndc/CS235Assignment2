from covid.domain.movie import Movie
from covid.domain.review import Review


class User:
    def __init__(self, user_name: str, password: str):
        if type(user_name) is not str:
            self.__user_name = None
        else:
            self.__user_name = user_name.strip().lower()

        if type(password) is not str:
            self.__password = None
        else:
            self.__password = password

        self.__friends = []
        self.__pending_friends = []
        self.__watched_movies = []
        self.__reviews = []
        self.__time_spent_watching_movies_minutes = 0

    @property
    def user_name(self):
        return self.__user_name

    @user_name.setter
    def user_name(self, user_name):
        if type(user_name) is str:
            self.__user_name = user_name.strip()

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, password):
        if type(password) is str:
            self.__password = password

    @property
    def friends(self):
        return self.__friends

    @property
    def pending_friends(self):
        return self.__pending_friends

    @property
    def watched_movies(self):
        return self.__watched_movies

    @watched_movies.setter
    def watched_movies(self, watched_movies):
        allmovies = True
        if type(watched_movies) is list:
            for i in watched_movies:
                if type(i) is not Movie:
                    allmovies = False
            if allmovies:
                self.__watched_movies = watched_movies

    @property
    def reviews(self):
        return self.__reviews

    @reviews.setter
    def reviews(self, reviews):
        allreviews = True
        if type(reviews) is list:
            for i in reviews:
                if type(i) is not Review:
                    allreviews = False
            if allreviews:
                self.__reviews = reviews

    @property
    def time_spent_watching_movies_minutes(self):
        return self.__time_spent_watching_movies_minutes

    @time_spent_watching_movies_minutes.setter
    def time_spent_watching_movies_minutes(self, watchtime):
        if type(watchtime) is int:
            if watchtime >= 0:
                self.__time_spent_watching_movies_minutes = watchtime

    def watch_movie(self, movie: Movie):
        if type(movie) is Movie:
            self.__watched_movies.append(movie)
            self.__time_spent_watching_movies_minutes += movie.runtime_minutes

    def add_review(self, review: Review):
        if type(review) is Review:
            self.__reviews.append(review)
            review.__user = self

    def send_friend_request(self, recipient):
        if type(recipient) is User and self != recipient:
            # check to see if they are not already (pending) friends
            if (recipient not in self.__pending_friends) and (recipient not in self.__friends):
                # add both users to each other's pending lists
                self.__pending_friends.append(recipient)
                recipient.__pending_friends.append(self)

    def accept_pending_request(self, sender):
        if type(sender) is User and self != sender:
            if sender in self.__pending_friends:
                # add both users to each other's friends lists
                self.__friends.append(sender)
                sender.__friends.append(self)
                # remove both users from each other's pending lists
                self.__pending_friends.remove(sender)
                sender.__pending_friends.remove(self)

    def ignore_pending_request(self, user):
        if type(user) is User:
            if user in self.__pending_friends:
                self.__pending_friends.remove(user)
                user.__pending_friends.remove(self)

    def ignore_all_pending_requests(self):
        for user in self.__pending_friends:
            user.__pending_friends.remove(self)
        self.__pending_friends = []

    def see_friend_watched_movies(self, friend):
        if type(friend) is User and friend in self.__friends:
            return friend.__watched_movies

    def see_friend_reviews(self, friend):
        if type(friend) is User and friend in self.__friends:
            return friend.__reviews

    def see_friend_minutes_watched(self, friend):
        if type(friend) is User and friend in self.__friends:
            return friend.__time_spent_watching_movies_minutes

    def __repr__(self):
        return f"<User {self.__user_name}>"

    def __eq__(self, other):
        return self.__user_name == other.__user_name

    def __lt__(self, other):
        return self.__user_name < other.__user_name

    def __hash__(self):
        return hash(self.__user_name)
