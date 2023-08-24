"""Models for Golf Round Tracker"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()



class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    handicap = db.Column(db.Integer)

    def __repr__(self):
        return f"<User user_id={self.user_id} email={self.email}>"
    
class Course(db.Model):
    """A Golf Course."""

    __tablename__ = "courses"

    course_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String)
    par = db.Column(db.Integer)
    length = db.Column(db.Integer)
    difficulty = db.Column(db.Integer)

    def __repr__(self):
        return f"<Course course_id={self.course_id} name={self.name}>"


class Score(db.Model):
    """Players Score"""

    __tablename__ = "scores"

    score_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    shot = db.Column(db.Integer)
    # date_played = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    course_id = db.Column(db.Integer, db.ForeignKey("courses.course_id"))

    user = db.relationship("User", backref="scores")
    course = db.relationship("Course", backref="scores")

    def __repr__(self):
        return f"<Score score_id={self.score_id} score={self.score}>"
    
    def get_user(self):
        return User.query.get(self.user_id)

    




def connect_to_db(flask_app, db_uri='postgresql://postgres:David1997$@localhost:5432/tracker', echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")

if __name__ == "__main__":
    from server import app

    connect_to_db(app)