from faker import Faker
from random import randint

from database.db import session
from database.models import Teacher, Student, Team, Grade, Subject

fake = Faker('uk_UA')

TEACHERS = 5
STUDENTS = 30
TEAMS = 3
GRADES = 10
SUBJECTS = 5
GROUPS = 3


def create_teachers():
    for _ in range(TEACHERS):
        teacher = Teacher(
            name=fake.name()
        )
        session.add(teacher)
    session.commit()


def create_students():
    for _ in range(STUDENTS):
        student = Student(
            name=fake.name(),
            team_id=randint(1, GROUPS)
        )
        session.add(student)
    session.commit()


def create_teams():
    for i in range(1, TEAMS+1):
        team = Team(
            team_name=f'team{i}'
        )
        session.add(team)
    session.commit()


def create_grades():
    for _ in range(STUDENTS * GRADES):
        grade = Grade(
            grades=randint(1, 12),
            student_id=randint(1, STUDENTS),
            subject_id=randint(1, SUBJECTS),
            lesson_date=fake.date_between(start_date='-2y')
        )
        session.add(grade)
    session.commit()


def create_subjects():
    for _ in range(SUBJECTS):
        subject = Subject(
            subject_name=fake.job(),
            teacher_id=randint(1, TEACHERS)
        )
        session.add(subject)
    session.commit()


if __name__ == '__main__':
    # create_teachers()
    create_teams  ()
    # create_students()
    # create_subjects()
    # create_grades()
