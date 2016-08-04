"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session)

# if it doesn't work, make sure your env is sourced; this is to do with requirements.txt
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template('homepage.html')


@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)


@app.route('/users/<int:user_id>')
def show_user():
    """Shows details of a selected user."""

    return render_template('user_page.html')


@app.route("/register", methods=['GET'])
def register_form():
    """Render registration form."""

    return render_template('register_form.html')


@app.route("/register", methods=['POST'])
def register_process():
    """Confirm user registered."""

    #This is Flask formatting for grabbing elements from a form/form handling in general
    email = request.form.get('email')
    password = request.form.get('password')
    age = request.form.get('age')
    zipcode = request.form.get('zipcode')

    #SQLAlchemy - querying db for username match
    is_user = User.query.filter_by(email='email').first()

    #Instantiating new_user
    new_user = User(email, password, age, zipcode)

    if is_user is not None: #if user exists
        session['user_has_been_added']= is_user.email
        flash('Your account already exists. We\'ve logged you in!')
        return redirect('/') #redirect to homepage
    else: #come back to this in afternoon
        db.session.add(new_user) #write new user to db
        db.session.commit()
        session['user_has_been_added']= new_user.email #handling Flask session like library, index key
        flash("Welcome! Your account has been created")
        return redirect('/') #redirect to homepage


@app.route("/login", methods=["GET"])
def login_form():
    """Show login form."""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """Log user into site.

    Find the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session.
    """

    email = request.form.get('email')
    password = request.form.get('password')

    #SQLAlchemy - querying db for email and password match
    is_user = User.query.filter((email=='email') & (password=='password')).first()

    if is_user is not None:
        session['user_email']= is_user.email
        flash('You\'ve been successfully logged in!')
        return redirect('/')
    else:
        flash('Sorry, we could not find you. Please register.')
        return redirect('/register')


@app.route("/logout")
def logout():
    """Logs user out of site."""        

    session.pop('user_email', None) #pop the key from the session
    flash('You\'ve been successfully logged out!')
    return redirect('/')

@app.route("/movies/<int:movie_id>")
def movie_detail(movie_id):
    """Shows movie details for individual movie"""

    return render_template('movie_list.html', movie_id=movie_id)

@app.route("/all_movies")
def movies_all():
    """ """

    movies = Movie.query.all()
    return render_template("movie_list.html", movies=movies)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
