import pytest
from cs235flix.domain.model import Movie, Review, User

@pytest.fixture
def user():
    return User("emelg", "passwd")

@pytest.fixture
def friend():
    return User("notemelg", "wdpass")

@pytest.fixture
def friend2():
    return User("Picroma", "shadow")


def test_send_friend_request(user, friend):
    user.send_friend_request(friend)
    assert user.pending_friends == [friend]
    assert friend.pending_friends == [user]


def test_send_friend_request_invalid(user):
    randstring = "asdf"
    user.send_friend_request(randstring)
    assert user.pending_friends == []


def test_send_friend_request_self(user):
    user.send_friend_request(user)
    assert user.pending_friends == []


def test_send_friend_request_pending_exists(user, friend):
    user.send_friend_request(friend)
    friend.send_friend_request(user)
    assert user.pending_friends == [friend]
    assert friend.pending_friends == [user]


def test_send_friend_request_friend_exists(user, friend):
    user.send_friend_request(friend)
    friend.accept_pending_request(user)
    user.send_friend_request(friend)
    assert user.pending_friends == []
    assert user.friends == [friend]
    assert friend.pending_friends == []
    assert friend.friends == [user]


def test_accept_pending_request(user, friend):
    user.send_friend_request(friend)
    friend.accept_pending_request(user)
    assert user.pending_friends == []
    assert friend.pending_friends == []
    assert user.friends == [friend]
    assert friend.friends == [user]


def test_accept_pending_request_on_behalf_of_friend(user, friend):
    user.send_friend_request(friend)
    assert user.pending_friends == [friend]
    assert friend.pending_friends == [user]

    user.accept_pending_request(user)
    assert user.pending_friends == [friend]
    assert friend.pending_friends == [user]
    assert user.friends == []
    assert friend.friends == []


def test_accept_pending_request_multiple(user, friend, friend2):
    friend.send_friend_request(user)
    friend2.send_friend_request(user)
    assert user.pending_friends == [friend, friend2]

    user.accept_pending_request(friend)
    assert user.pending_friends == [friend2]
    assert user.friends == [friend]

    user.accept_pending_request(friend2)
    assert user.pending_friends == []
    assert user.friends == [friend, friend2]


def test_accept_pending_request_none(user, friend):
    user.accept_pending_request(friend)
    assert user.pending_friends == []
    assert user.friends == []


def test_ignore_pending_request_recipient(user, friend):
    user.send_friend_request(friend)
    friend.ignore_pending_request(user)
    assert user.pending_friends == []
    assert friend.pending_friends == []


def test_ignore_pending_request_sender(user, friend):
    user.send_friend_request(friend)
    user.ignore_pending_request(friend)
    assert user.pending_friends == []
    assert friend.pending_friends == []


def test_ignore_pending_request_none(user, friend):
    user.ignore_pending_request(friend)
    assert user.pending_friends == []


def test_ignore_all_pending_requests(user, friend):
    friend2 = User("Picroma", "shadow")
    friend.send_friend_request(user)
    friend2.send_friend_request(user)
    user.ignore_all_pending_requests()
    assert user.pending_friends == []
    assert friend.pending_friends == []
    assert friend2.pending_friends == []


def test_accessing_non_friend(user, friend):
    thisisamovie = Movie("Garlic Bread", 2020)
    thisisareview = Review(thisisamovie, "this is a review.", 9)

    thisisamovie.runtime_minutes = 69
    friend.watch_movie(Movie("Garlic Bread", 2020))
    friend.add_review(thisisareview)
    assert user.see_friend_watched_movies(friend) is None
    assert user.see_friend_reviews(friend) is None
    assert user.see_friend_minutes_watched(friend) is None



def test_see_friend_watched_movies(user, friend):
    user.send_friend_request(friend)
    friend.accept_pending_request(user)
    friend.watch_movie(Movie("Garlic Bread", 2020))
    assert user.see_friend_watched_movies(friend) == [Movie("Garlic Bread", 2020)]


def test_see_friend_reviews(user, friend):
    user.send_friend_request(friend)
    friend.accept_pending_request(user)
    thisisareview = Review(Movie("Garlic Bread", 2020), "this is a review.", 9)
    friend.add_review(thisisareview)
    assert user.see_friend_reviews(friend) == [thisisareview]


def test_see_friend_minutes_watched(user, friend):
    user.send_friend_request(friend)
    friend.accept_pending_request(user)
    thisisamovie = Movie("Garlic Bread", 2020)
    thisisamovie.runtime_minutes = 69
    friend.watch_movie(thisisamovie)
    assert user.see_friend_minutes_watched(friend) == 69
