from datetime import date, datetime
from typing import List, Iterable


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
        self.__friends_ids = []
        self.__pending_friends = []
        self.__pending_friends_ids = []
        self.__watched_movies = []
        self.__watched_ids = []
        self.__reviews = []
        self.__time_spent_watching_movies_minutes = 0
        self.__id = None

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id):
        if type(id) is int:
            self.__id = id

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

    @friends.setter
    def friends(self, friends):
        if type(friends) is list:
            self.__friends = friends

    @property
    def pending_friends(self):
        return self.__pending_friends

    @pending_friends.setter
    def pending_friends(self, friends):
        if type(friends) is list:
            self.__pending_friends = friends

    @property
    def friends_ids(self):
        return self.__friends

    @friends_ids.setter
    def friends_ids(self, friends):
        if type(friends) is list:
            self.__friends = friends

    @property
    def pending_friends_ids(self):
        return self.__pending_friends_ids

    @pending_friends_ids.setter
    def pending_friends_ids(self, friends):
        if type(friends) is list:
            self.__pending_friends_ids = friends

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
    def watched_ids(self):
        return self.__watched_ids

    @watched_ids.setter
    def watched_ids(self, watched_ids):
        allmovies = True
        if type(watched_ids) is list:
            for i in watched_ids:
                if type(i) is not int:
                    allmovies = False
            if allmovies:
                self.__watched_ids = watched_ids

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

    def watch_movie(self, movie: 'Movie', id: int):
        if type(movie) is Movie:
            self.__watched_movies.append(movie)
            self.__watched_ids.append(id)
            self.__time_spent_watching_movies_minutes += movie.runtime_minutes

    def add_review(self, review: 'Review'):
        if type(review) is Review:
            self.__reviews.append(review)

    @property
    def number_of_friends(self):
        return len(self.__friends)

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


class Actor:
    def __init__(self, actor_full_name: str):
        if actor_full_name == "" or type(actor_full_name) is not str:
            self.__actor_full_name = None
        else:
            self.__actor_full_name = actor_full_name.strip()
        self.__colleagues = []

    @property
    def actor_full_name(self) -> str:
        return self.__actor_full_name

    def __repr__(self):
        return f"<Actor {self.__actor_full_name}>"

    def __eq__(self, other):
        return self.__actor_full_name == other.__actor_full_name

    def __lt__(self, other):
        return self.__actor_full_name < other.__actor_full_name

    def __hash__(self):
        return hash(self.__actor_full_name)

    def add_actor_colleague(self, colleague):
        self.__colleagues.append(colleague)
        colleague.__colleagues.append(self)

    def check_if_this_actor_worked_with(self, colleague):
        for i in self.__colleagues:
            if i.__actor_full_name == colleague.__actor_full_name:
                return True
        return False


class Director:

    def __init__(self, director_full_name: str):
        if director_full_name == "" or type(director_full_name) is not str:
            self.__director_full_name = None
        else:
            self.__director_full_name = director_full_name.strip()

    @property
    def director_full_name(self) -> str:
        return self.__director_full_name

    def __repr__(self):
        return f"<Director {self.__director_full_name}>"

    def __eq__(self, other):
        return self.__director_full_name == other.__director_full_name

    def __lt__(self, other):
        return self.__director_full_name < other.__director_full_name

    def __hash__(self):
        return hash(self.__director_full_name)


class Genre:
    def __init__(self, genre_name: str):
        if genre_name == "" or type(genre_name) is not str:
            self.__genre_name = None
        else:
            self.__genre_name = genre_name.strip()

    @property
    def genre_name(self) -> str:
        return self.__genre_name

    def __repr__(self):
        return f"<Genre {self.__genre_name}>"

    def __eq__(self, other):
        return self.__genre_name == other.__genre_name

    def __lt__(self, other):
        return self.__genre_name < other.__genre_name

    def __hash__(self):
        return hash(self.__genre_name)


class Review:
    def __init__(self, movie: 'Movie', review_text: str, rating: int):
        # movie
        if type(movie) is not Movie:
            self.__movie = None
        else:
            self.__movie = movie

        # review_text
        if review_text == "" or type(review_text) is not str:
            self.__review_text = None
        else:
            self.__review_text = review_text.strip()

        # rating
        if rating < 1 or rating > 10 or type(rating) is not int:
            self.__rating = None
        else:
            self.__rating = rating

        # timestamp
        self.__timestamp = datetime.today()

        # user
        self.__user = None

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

    @user.setter
    def user(self, user):
        if type(user) is User:
            self.__user = user

    @property
    def timestamp(self):
        return self.__timestamp

    @timestamp.setter
    def timestamp(self, timestamp: datetime):
        if type(timestamp) == datetime:
            self.__timestamp = timestamp

    def __repr__(self):
        return f"{self.__movie}, {self.__user}, {self.__review_text}, {self.__timestamp}"

    def __eq__(self, other):
        return (self.__movie, self.__review_text, self.__rating, self.__timestamp) == (
            other.__movie, other.__review_text, other.__rating, other.__timestamp)


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

        if True:
            self.__reviews = []

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
    def reviews(self) -> list:
        return self.__reviews

    @reviews.setter
    def reviews(self, reviews):
        self.__reviews = reviews

    def add_review(self, review):
        self.__reviews.append(review)

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
    def tags(self):
        return self._tags

    @tags.setter
    def tags(self, tags):
        self._tags = tags

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
        return f"<Movie {self.__title}, {self.__release_year}, {self.__reviews}>"

    def __eq__(self, other):
        return self.__title == other.__title and self.__release_year == other.__release_year

    def __lt__(self, other):
        if self.__title == other.__title:
            return self.__release_year < other.__release_year
        else:
            return self.title < other.title

    def __hash__(self):
        return hash((self.__title, self.__release_year))


class Tag:
    def __init__(
            self, tag_name: str
    ):
        self._tag_name: str = tag_name
        self._tagged_movies: List[Movie] = list()

    @property
    def tag_name(self) -> str:
        return self._tag_name

    @property
    def tagged_movies(self) -> List[Movie]:
        return self._tagged_movies

    @property
    def number_of_tagged_movies(self) -> int:
        return len(self._tagged_movies)

    def is_applied_to(self, movie: Movie) -> bool:
        return movie in self._tagged_movies

    def add_movie(self, movie: Movie):
        self._tagged_movies.append(movie)

    def __eq__(self, other):
        if not isinstance(other, Tag):
            return False
        return other._tag_name == self._tag_name

    def __repr__(self):
        return f"<Tag {self._tag_name}>"


def make_review(movie: Movie, review_text: str, rating: int, user: User, timestamp):
    if timestamp == None:
        timestamp = datetime.today()
    review = Review(movie, review_text, rating)
    review.user = user
    review.timestamp = timestamp

    movie.add_review(review)
    user.add_review(review)

    return review


class ModelException(Exception):
    pass


def make_tag_association(movie: Movie, tag: Tag):
    if tag.is_applied_to(movie):
        raise ModelException(f'Tag {tag.tag_name} already applied to Movie "{movie.title}"')

    movie.add_tag(tag)
    tag.add_movie(movie)
