import pytest
from domainmodel.movie import Movie
from domainmodel.watchlist import WatchList

@pytest.fixture
def watchlist():
    return WatchList()


def test_init_watchlist(watchlist):
    assert type(watchlist) == WatchList


def test_check_size(watchlist):
    assert watchlist.size() == 0


def test_check_size_of_nonempty_watchlist(watchlist):
    watchlist.add_movie(Movie("Moana", 2016))
    assert watchlist.size() == 1


def test_add_movie(watchlist):
    watchlist.add_movie(Movie("Moana", 2016))
    assert watchlist.first_movie_in_watchlist() == Movie("Moana", 2016)


def test_add_same_movie_again(watchlist):
    watchlist.add_movie(Movie("Moana", 2016))
    watchlist.add_movie(Movie("Moana", 2016))
    assert watchlist.size() == 1


def test_remove_movie(watchlist):
    watchlist.add_movie(Movie("Moana", 2016))
    watchlist.add_movie(Movie("Your Name", 2016))
    watchlist.remove_movie(Movie("Moana", 2016))
    assert watchlist.size() == 1
    assert watchlist.first_movie_in_watchlist() == Movie("Your Name", 2016)


def test_remove_movie_which_is_not_in_watchlist(watchlist):
    watchlist.add_movie(Movie("Moana", 2016))
    assert watchlist.remove_movie(Movie("Your Name", 2016)) == None
    assert watchlist.size() == 1


def test_select_movie_to_watch_index(watchlist):
    watchlist.add_movie(Movie("Moana", 2016))
    watchlist.add_movie(Movie("Your Name", 2016))
    watchlist.add_movie(Movie("A Silent Voice", 2016))
    assert watchlist.select_movie_to_watch(1) == Movie("Your Name", 2016)


def test_select_movie_to_watch_index_out_of_bounds(watchlist):
    watchlist.add_movie(Movie("Moana", 2016))
    watchlist.add_movie(Movie("Your Name", 2016))
    watchlist.add_movie(Movie("A Silent Voice", 2016))
    assert watchlist.select_movie_to_watch(3) == None


def test_iterator_used(watchlist):
    watchlist.add_movie(Movie("Moana", 2016))
    watchlist.add_movie(Movie("Your Name", 2016))
    watchlist.add_movie(Movie("A Silent Voice", 2016))
    iterator = iter(watchlist)
    assert next(watchlist) == Movie("Moana", 2016)
    assert next(watchlist) == Movie("Your Name", 2016)
    assert next(watchlist) == Movie("A Silent Voice", 2016)


def test_iterator_reaches_final_element(watchlist):
    watchlist.add_movie(Movie("Moana", 2016))
    watchlist.add_movie(Movie("Your Name", 2016))
    watchlist.add_movie(Movie("A Silent Voice", 2016))
    iterator = iter(watchlist)
    next(watchlist)
    next(watchlist)
    next(watchlist)
    with pytest.raises(StopIteration):
        next(watchlist)


def test_getter(watchlist):
    watchlist.add_movie(Movie("Moana", 2016))
    watchlist.add_movie(Movie("Your Name", 2016))
    watchlist.add_movie(Movie("A Silent Voice", 2016))
    assert watchlist.watchlist == [Movie("Moana", 2016), Movie("Your Name", 2016), Movie("A Silent Voice", 2016)]


def test_setter(watchlist):
    watchlist.add_movie(Movie("Moana", 2016))
    new_watchlist = [Movie("Your Name", 2016), Movie("A Silent Voice", 2016)]
    watchlist.watchlist = new_watchlist
    assert watchlist.watchlist == [Movie("Your Name", 2016), Movie("A Silent Voice", 2016)]