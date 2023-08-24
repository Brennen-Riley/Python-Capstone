import os
import json
from random import choice, randint

import crud
import model
import server


os.system("dropdb -U postgres tracker")
os.system("createdb -U postgres tracker")

model.connect_to_db(server.app)
model.db.create_all()


with open('data/courses.json') as f:
    course_data = json.loads(f.read())


courses_in_db = []
for course in course_data:
    name, par, length, difficulty = (
        course["name"],
        course["par"],
        course["length"],
        course["difficulty"],
    )
    db_course = crud.create_course(name, par, length, difficulty)
    courses_in_db.append(db_course)

model.db.session.add_all(courses_in_db)
model.db.session.commit()


for n in range(10):
    first_name = f"jon{n}"
    last_name = f"nova{n}"
    email = f"user{n}@test.com"
    password = "test"
    handicap = randint(1, 15)

    user = crud.create_user(first_name, last_name, email, password, handicap)
    model.db.session.add(user)

    for _ in range(10):
        random_course = choice(courses_in_db)
        shot = randint(60, 100)

        score = crud.create_score(user, random_course, shot)
        model.db.session.add(score)

model.db.session.commit()