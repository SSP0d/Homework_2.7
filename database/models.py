from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime


Base = declarative_base()


class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

    teachers = relationship("Subject", backref="teacher")


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    team_id = Column(Integer, ForeignKey("teams.id", ondelete="CASCADE"))

    grades = relationship("Grade", backref="student")


class Team(Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True)
    team_name = Column(String(25), nullable=False, unique=True)

    students = relationship("Student", backref="team")


class Grade(Base):
    __tablename__ = "grades"
    id = Column(Integer, primary_key=True)
    grades = Column(Integer)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"))
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="CASCADE"))
    lesson_date = Column(DateTime)


class Subject(Base):
    __tablename__ = "subjects"
    id = Column(Integer, primary_key=True)
    subject_name = Column(String(50), nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id", ondelete="CASCADE"))

    grades = relationship("Grade", backref="subject")
