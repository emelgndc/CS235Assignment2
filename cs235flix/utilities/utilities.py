from flask import Blueprint, request, render_template, redirect, url_for, session

import cs235flix.adapters.repository as repo
import cs235flix.utilities.services as services


# Configure Blueprint.
utilities_blueprint = Blueprint(
    'utilities_bp', __name__)


def get_tags_and_urls():
    tag_names = services.get_tag_names(repo.repo_instance)
    tag_urls = dict()
    for tag_name in tag_names:
        tag_urls[tag_name] = url_for('movie_bp.movies_by_tag', tag=tag_name)

    return tag_urls


def get_selected_movies(quantity=3):
    movies = services.get_random_movies(quantity, repo.repo_instance)

    #for movie in movies:
    #    movie['hyperlink'] = url_for('movie_bp.movies_by_date', date=movie['date'].isoformat())
    return movies


def get_movies(movie_count):
    movies = services.get_movies(movie_count, repo.repo_instance)

    return movies
