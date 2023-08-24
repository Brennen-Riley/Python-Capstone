"""CRUD operations."""

from model import db, User, Course, Score, connect_to_db



def create_user(first_name, last_name, email, password, handicap):
    """Create and return a new user."""

    user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password,
        handicap=handicap,
    )

    return user

def get_users():
    """Return all users"""

    return User.query.all()

def get_user_by_id(user_id):
    """Return a user by primary key"""

    return User.query.get(user_id)

def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email).first()

def create_course(name, par, length, difficulty):
    """Create and return a new Course"""

    course = Course(
        name=name,
        par=par,
        length=length,
        difficulty=difficulty,
    )

    return course

def get_courses():
    """Return all courses"""

    return Course.query.all()

def get_course_by_id(course_id):
    """Return a course by ID"""

    return Course.query.get(course_id)

def get_course_by_name(course_name):
    """Return a course by name"""

    return Course.query.filter_by(name=course_name).first()

def get_scores():
    """Return all scores"""

    return Score.query.all()

def get_score_by_id(score_id):
    """Return a score by primary key"""

    return Score.query.get(score_id)

def create_score(user, course, shot):
    """Create and return a new Score"""

    score = Score(
        user=user,
        course=course,
        shot=shot,
    )

    return score


if __name__ == '__main__':
    from server import app
    connect_to_db(app)