from . import db
from sqlalchemy.sql import func
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(25), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(40), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=func.now())


class Teacher(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'), nullable=False)


class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'), nullable=False)


class Test(db.Model):
    __tablename__ = 'tests'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey(
        'teachers.id'), nullable=False)
    test_name = db.Column(db.String(40), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=func.now())
    date_edited = db.Column(db.DateTime, nullable=False, default=func.now())


class TestQuestion(db.Model):
    __tablename__ = 'test_questions'
    id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    test_id = db.Column(db.Integer, db.ForeignKey(
        'tests.id'), nullable=False)
    question = db.Column(db.String(255), nullable=False)
    answer = db.Column(db.String(255), nullable=False)


class TestAttempt(db.Model):
    __tablename__ = 'test_attempts'
    id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey(
        'students.id'), nullable=False)
    test_id = db.Column(db.Integer, db.ForeignKey(
        'tests.id'), nullable=False)


class TestAttemptQuestion(db.Model):
    __tablename__ = 'test_attempt_questions'
    id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    test_attempt_id = db.Column(db.Integer, db.ForeignKey(
        'test_attempts.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey(
        'test_questions.id'), nullable=False)
    attempted_answer = db.Column(db.String(255), nullable=False)
