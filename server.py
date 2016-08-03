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


@app.route("/register", methods=['GET'])
def register_form():
    """Render registration form."""

    return render_template('register_form.html')


@app.route("/register", methods=['POST'])
def register_process():
    """Confirm user registered."""

    #This is Flask formatting for grabbing elements from a form/form handling in general
    username = request.form.get('username')
    password = request.form.get('password')

    #SQLAlchemy
    is_user = User.query.filter_by(user_id='username').first() #querying db for username match

    if is_user is not None: #if user exists
        return redirect('/') #redirect to homepage
    else: #come back to this in afternoon
        db.session.add(#something) #write new user to db
        db.session.commit()
        return redirect('/') #redirect to homepage




 #this is where user verification happens
 #add user to db.session, commit changes


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
