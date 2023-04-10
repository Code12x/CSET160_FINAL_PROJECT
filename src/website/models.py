from . import db
from sqlalchemy.sql import func
from flask_login import UserMixin


class Users(db.Model, UserMixin):
    __tablename__ = 'Users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(40), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=func.now())

    @property
    def is_teacher(self):
        teacher = Teachers.query.filter_by(user_id=self.user_id).first()
        if teacher:
            return True
        else:
            return False


class Teachers(db.Model, UserMixin):
    __tablename__ = 'Teachers'
    teacher_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'Users.user_id'), nullable=False)
    user = db.relationship('Users', backref='teachers')

    @property
    def id(self):
        return self.user.user_id


class Students(db.Model, UserMixin):
    __tablename__ = 'Students'
    student_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'Users.user_id'), nullable=False)
    user = db.relationship('Users', backref='students')

    @property
    def id(self):
        return self.user.user_id


class Tests(db.Model):
    __tablename__ = 'Tests'
    test_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey(
        'Teachers.teacher_id'), nullable=False)
    test_name = db.Column(db.String(40), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=func.now())
    date_edited = db.Column(db.DateTime, nullable=False, default=func.now())
    teacher = db.relationship('Teachers', backref='tests')


class TestQuestions(db.Model):
    __tablename__ = 'TestQuestions'
    test_question_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    test_id = db.Column(db.Integer, db.ForeignKey(
        'Tests.test_id'), nullable=False)
    question = db.Column(db.String(255), nullable=False)
    answer = db.Column(db.String(255), nullable=False)
    test = db.relationship('Tests', backref='test_questions')


class TestAttempts(db.Model):
    __tablename__ = 'TestAttempts'
    test_attempt_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey(
        'Students.student_id'), nullable=False)
    test_id = db.Column(db.Integer, db.ForeignKey(
        'Tests.test_id'), nullable=False)
    student = db.relationship('Students', backref='test_attempts')
    test = db.relationship('Tests', backref='test_attempts')


class TestAttemptQuestions(db.Model):
    __tablename__ = 'TestAttemptQuestions'
    test_attempt_question_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True)
    test_attempt_id = db.Column(db.Integer, db.ForeignKey(
        'TestAttempts.test_attempt_id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey(
        'TestQuestions.test_question_id'), nullable=False)
    attempted_answer = db.Column(db.String(255), nullable=False)
    test_attempt = db.relationship(
        'TestAttempts', backref='test_attempt_questions')
    test_question = db.relationship(
        'TestQuestions', backref='test_attempt_questions')
