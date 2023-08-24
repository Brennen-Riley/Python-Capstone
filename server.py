"""Server for Golf Round Tracker"""

from flask import (Flask, render_template, request, flash, session, redirect)

from model import connect_to_db, db
import crud

from jinja2 import StrictUndefined


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined



@app.route('/')
def homepage():
    """View Homepage."""

    return render_template('homepage.html')

@app.route('/scores')
def all_scores():
    """View all scores"""

    scores = crud.get_scores()

    return render_template("all_scores.html", scores=scores)

@app.route('/scores', methods=["POST"])
def submit_score():
    """Submit a score"""

    logged_in_email = session.get("user_email")
    score_shot = request.form.get("shot")

    if logged_in_email is None:
        flash("You must log in to submit a score.")
    elif not score_shot:
        flash("Error: you didn't post a number for you score.")
    else:
        user = crud.get_user_by_email(logged_in_email)
        course = crud.get_course_by_name(request.form.get("course"))

        score = crud.create_score(user, course, int(score_shot))
        db.session.add(score)
        db.session.commit()

        flash(f"You Shot {score_shot}")

    return render_template("homepage.html")

@app.route('/scores/<score_id>')
def show_score(score_id):
    """Show Details on a Players Score"""

    score = crud.get_score_by_id(score_id)

    return render_template("score_details.html", score=score)

@app.route('/courses')
def all_courses():
    """View all courses"""

    courses = crud.get_courses()

    return render_template("all_courses.html", courses=courses)

@app.route('/courses/<course_id>')
def show_course(course_id):
    """Show details on a particular course"""

    course = crud.get_course_by_id(course_id)

    return render_template("course_details.html", course=course)

@app.route('/users')
def all_users():
    """View all users"""

    users = crud.get_users()

    return render_template("all_users.html", users=users)

@app.route('/users/<user_id>')
def show_user(user_id):
    """Show details on a user"""

    user = crud.get_user_by_id(user_id)

    return render_template("user_details.html", user=user)

@app.route('/users', methods=["POST"])
def register_user():
    """Create a new user."""

    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    password = request.form.get("password")
    handicap = request.form.get("handicap")

    user = crud.get_user_by_email(email)
    if user:
        flash("Account already created. Try again.")
    else:
        user = crud.create_user(first_name, last_name, email, password, handicap)
        db.session.add(user)
        db.session.commit()
        flash("Account created successfully. Please log in.")

    return redirect("/")

@app.route('/login', methods=["POST"])
def process_login():
    """Process user login."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if not user or user.password != password:
        flash("The email or passwrod you entered was incorrect.")
    else:
        session["user_email"] = user.email
        flash(f"Welcome back, {user.first_name}!")

    return redirect("/")



if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)