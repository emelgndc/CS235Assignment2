from datetime import date

from flask import Blueprint
from flask import request, render_template, redirect, url_for, session

from better_profanity import profanity
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError

import cs235flix.adapters.repository as repo
import cs235flix.utilities.utilities as utilities
import cs235flix.movie.services as services

from cs235flix.authentication.authentication import login_required


# Configure Blueprint.
movie_blueprint = Blueprint(
    'movie_bp', __name__)


@movie_blueprint.route('/browse', methods=['GET'])
def browse():
    if 'user_name' in session:
        watchbtn = "yes"
        watched = services.get_watched(session['user_name'], repo.repo_instance)
    else:
        watchbtn = "no"
        watched = []

    movies_per_page = 10
    length = services.get_last_movie(repo.repo_instance)['id']

    searchStr = request.args.get('search')
    searchFor = request.args.get('type')
    cursor = request.args.get('cursor')
    movie_to_show_reviews = request.args.get('view_reviews_for')

    # Fetch the first and last movies in the series.
    first_movie = services.get_first_movie(repo.repo_instance)
    last_movie = services.get_last_movie(repo.repo_instance)

    if cursor is None:
        cursor = 0
    else:
        cursor = int(cursor)

    if movie_to_show_reviews is None:
        # No view-reviews query parameter, so set to a non-existent movie id.
        movie_to_show_reviews = -1
    else:
        # Convert movie_to_show_reviews from string to int.
        movie_to_show_reviews = int(movie_to_show_reviews)

    id_list = []
    full_list = []
    if searchStr and searchFor is not None:
        if searchFor == "Actor":
            full_list = services.get_movie_ids_for_actor(searchStr, repo.repo_instance)
        elif searchFor == "Director":
            full_list = services.get_movie_ids_for_director(searchStr, repo.repo_instance)
        full_list = sorted(full_list)
        length = len(full_list)
        id_list = full_list[cursor:min(cursor+movies_per_page, length)]

    else:
        full_list.extend(range(1,length+1))
        for i in range(cursor, cursor + movies_per_page):
            id_list.append(i+1)

    movies = services.get_movies_by_id(id_list, repo.repo_instance)

    first_movie_url = None
    last_movie_url = None
    next_movie_url = None
    prev_movie_url = None

    if len(movies) > 0:
        # There's at least one movie in the list
        if id_list[0] > full_list[0]:
            # There are movies with a lower id, so generate URLs for the 'previous' and 'first' navigation buttons.
            prev_movie_url = url_for('movie_bp.browse', search=searchStr, type=searchFor, cursor=cursor-movies_per_page)
            first_movie_url = url_for('movie_bp.browse', search=searchStr, type=searchFor)

        # There are movies with a higher id, so generate URLs for the 'next' and 'last' navigation buttons.
        if id_list[len(id_list)-1] < full_list[length-1]:
            next_movie_url = url_for('movie_bp.browse', search=searchStr, type=searchFor, cursor=cursor+movies_per_page)

            last_cursor = movies_per_page * (length // movies_per_page)
            if length % movies_per_page == 0:
                last_cursor -= movies_per_page
            last_movie_url = url_for('movie_bp.browse', search=searchStr, type=searchFor, cursor=last_cursor)

        # Construct urls for viewing movie reviews and adding reviews.
        for movie in movies:
            movie['view_review_url'] = url_for('movie_bp.browse', search=searchStr, type=searchFor, cursor=cursor, view_reviews_for=movie['id'])
            movie['add_review_url'] = url_for('movie_bp.review_movie', movie=movie['id'])
            movie['watch_url'] = url_for('authentication_bp.profile', watched=movie['id'])

        # Generate the webpage to display the movies.
        return render_template(
            'movie/movies.html',
            title='Movies',
            movies_title='Page ' + str(int(cursor/movies_per_page)+1),
            movies=movies,
            watched=watched,
            watchbtn=watchbtn,
            tag_urls=utilities.get_tags_and_urls(),
            first_movie_url=first_movie_url,
            last_movie_url=last_movie_url,
            prev_movie_url=prev_movie_url,
            next_movie_url=next_movie_url,
            show_reviews_for_movie=movie_to_show_reviews
        )

    # No movies to show, so return the homepage.
    return redirect(url_for('movie_bp.search_movie', none="True"))


@movie_blueprint.route('/movies_by_tag', methods=['GET'])
def movies_by_tag():
    if 'user_name' in session:
        watchbtn = "yes"
        watched = services.get_watched(session['user_name'], repo.repo_instance)
    else:
        watchbtn = "no"
        watched = []

    movies_per_page = 10

    # Read query parameters.
    tag_name = request.args.get('tag')
    cursor = request.args.get('cursor')
    movie_to_show_reviews = request.args.get('view_reviews_for')

    if movie_to_show_reviews is None:
        # No view-reviews query parameter, so set to a non-existent movie id.
        movie_to_show_reviews = -1
    else:
        # Convert movie_to_show_reviews from string to int.
        movie_to_show_reviews = int(movie_to_show_reviews)

    if cursor is None:
        # No cursor query parameter, so initialise cursor to start at the beginning.
        cursor = 0
    else:
        # Convert cursor from string to int.
        cursor = int(cursor)

    # Retrieve movie ids for movies that are tagged with tag_name.
    movie_ids = services.get_movie_ids_for_tag(tag_name, repo.repo_instance)

    # Retrieve the batch of movies to display on the Web page.
    movies = services.get_movies_by_id(movie_ids[cursor:cursor + movies_per_page], repo.repo_instance)

    first_movie_url = None
    last_movie_url = None
    next_movie_url = None
    prev_movie_url = None

    if cursor > 0:
        # There are preceding movies, so generate URLs for the 'previous' and 'first' navigation buttons.
        prev_movie_url = url_for('movie_bp.movies_by_tag', tag=tag_name, cursor=cursor - movies_per_page)
        first_movie_url = url_for('movie_bp.movies_by_tag', tag=tag_name)

    if cursor + movies_per_page < len(movie_ids):
        # There are further movies, so generate URLs for the 'next' and 'last' navigation buttons.
        next_movie_url = url_for('movie_bp.movies_by_tag', tag=tag_name, cursor=cursor + movies_per_page)

        last_cursor = movies_per_page * int(len(movie_ids) / movies_per_page)
        if len(movie_ids) % movies_per_page == 0:
            last_cursor -= movies_per_page
        last_movie_url = url_for('movie_bp.movies_by_tag', tag=tag_name, cursor=last_cursor)

    # Construct urls for viewing movie reviews and adding reviews.
    for movie in movies:
        movie['view_review_url'] = url_for('movie_bp.movies_by_tag', tag=tag_name, cursor=cursor, view_reviews_for=movie['id'])
        movie['add_review_url'] = url_for('movie_bp.review_movie', movie=movie['id'], tag=tag_name)
        movie['watch_url'] = url_for('authentication_bp.profile', watched=movie['id'])

    # Generate the webpage to display the movies.
    return render_template(
        'movie/movies.html',
        title='Movies',
        movies_title='Movies tagged by ' + tag_name,
        movies=movies,
        watched=watched,
        tag_urls=utilities.get_tags_and_urls(),
        first_movie_url=first_movie_url,
        last_movie_url=last_movie_url,
        prev_movie_url=prev_movie_url,
        next_movie_url=next_movie_url,
        show_reviews_for_movie=movie_to_show_reviews,
        watchbtn=watchbtn
    )


@movie_blueprint.route('/search', methods=['GET', 'POST'])
def search_movie():
    if 'user_name' in session:
        watchbtn = "yes"
        watched = services.get_watched(session['user_name'], repo.repo_instance)
    else:
        watchbtn = "no"
        watched = []

    none_found = request.args.get('none')
    none_message = ""
    if none_found == "True":
        none_message = "No movies found for searched name. Are you sure you spelt it correctly?"
    movies_per_page = 10

    # Create form
    form = SearchForm()

    if form.validate_on_submit():
        searchStr = form.search.data.title()
        searchFor = form.searching_for.data

        return redirect(url_for('movie_bp.browse', search=searchStr, type=searchFor))


    # For a GET or an unsuccessful POST, retrieve the movie to review in dict form, and return a Web page that allows
    # the user to enter a review. The generated Web page includes a form object.
    return render_template(
        'movie/search.html',
        title='Search by actor or director',
        form=form,
        handler_url=url_for('movie_bp.search_movie'),
        watched=watched,
        watchbtn=watchbtn,
        selected_movies=utilities.get_selected_movies(),
        tag_urls=utilities.get_tags_and_urls(),
        none_message=none_message
    )


@movie_blueprint.route('/review', methods=['GET', 'POST'])
@login_required
def review_movie():
    movies_per_page = 10
    # Obtain the username of the currently logged in user.
    username = session['user_name']

    # Create form. The form maintains state, e.g. when this method is called with a HTTP GET request and populates
    # the form with an movie id, when subsequently called with a HTTP POST request, the movie id remains in the
    # form.
    form = ReviewForm()

    if form.validate_on_submit():
        # Successful POST, i.e. the review text has passed data validation.
        # Extract the movie id, representing the reviewed movie, from the form.
        movie_id = int(form.movie_id.data)

        # Use the service layer to store the new review.
        services.add_review(movie_id, form.review.data, int(form.rating.data), username, repo.repo_instance)

        # Retrieve the movie in dict form.
        movie = services.get_movie(movie_id, repo.repo_instance)

        # Cause the web browser to go to 'browse' page containing the movie.
        num = (movie_id // movies_per_page) * movies_per_page
        if movie_id % movies_per_page == 0:
            num -= movies_per_page
        return redirect(url_for('movie_bp.browse', cursor=num, view_reviews_for=movie_id))



    if request.method == 'GET':
        # Request is a HTTP GET to display the form.
        # Extract the movie id, representing the movie to review, from a query parameter of the GET request.
        movie_id = int(request.args.get('movie'))

        # Store the movie id in the form.
        form.movie_id.data = movie_id
    else:
        # Request is a HTTP POST where form validation has failed.
        # Extract the movie id of the movie being reviewed from the form.
        movie_id = int(form.movie_id.data)

    # For a GET or an unsuccessful POST, retrieve the movie to review in dict form, and return a Web page that allows
    # the user to enter a review. The generated Web page includes a form object.
    movie = services.get_movie(movie_id, repo.repo_instance)
    return render_template(
        'movie/review_movie.html',
        title='Create review',
        movie=movie,
        form=form,
        handler_url=url_for('movie_bp.review_movie'),
        selected_movies=utilities.get_selected_movies(),
        tag_urls=utilities.get_tags_and_urls()
    )


class ProfanityFree:
    def __init__(self, message=None):
        if not message:
            message = u'Field must not contain profanity'
        self.message = message

    def __call__(self, form, field):
        if profanity.contains_profanity(field.data):
            raise ValidationError(self.message)


class ReviewForm(FlaskForm):
    review = TextAreaField('Review', [
        DataRequired(),
        Length(min=4, message='Your review is too short'),
        ProfanityFree(message='Your review must not contain profanity')])
    rating = SelectField('Rating', choices=[(1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5"), (6, "6"), (7, "7"), (8, "8"), (9, "9"), (10, "10")])
    movie_id = HiddenField("Movie id")
    submit = SubmitField('Submit')


class SearchForm(FlaskForm):
    search = TextAreaField('Search', [DataRequired(), Length(min=1, message='Please enter a name')])
    searching_for = SelectField('searchfor', choices=[("Actor", "Actor"), ("Director", "Director")])
    submit = SubmitField('Search')