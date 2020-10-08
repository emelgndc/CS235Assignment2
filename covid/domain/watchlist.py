from covid.domain.movie import Movie

class WatchList:
    def __init__(self):
        self.__watchlist = []

    @property
    def watchlist(self):
        return self.__watchlist

    @watchlist.setter
    def watchlist(self, watchlist):
        allmovies = True
        if type(watchlist) is list:
            for i in watchlist:
                if type(i) is not Movie:
                    allmovies = False
            if allmovies:
                self.__watchlist = watchlist

    def add_movie(self, movie):
        if type(movie) is Movie:
            if movie not in self.__watchlist:
                self.__watchlist.append(movie)

    def remove_movie(self, movie):
        if movie in self.__watchlist:
            self.__watchlist.remove(movie)

    def select_movie_to_watch(self, index):
        if index > len(self.__watchlist)-1:
            return None
        else:
            return self.__watchlist[index]

    def size(self):
        return len(self.__watchlist)

    def first_movie_in_watchlist(self):
        if len(self.__watchlist) == 0:
            return None
        else:
            return self.__watchlist[0]

    def __iter__(self):
        self.__n = 0
        return self

    def __next__(self):
        if self.__n <= len(self.__watchlist)-1:
            result = self.__watchlist[self.__n]
            self.__n += 1
            return result
        else:
            raise StopIteration
