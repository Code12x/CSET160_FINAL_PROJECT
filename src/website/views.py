from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from sqlalchemy import text
from .models import *

views = Blueprint('views', __name__)


@views.route("/")
def index():
    return render_template("index.html")


@views.route("/create/test", methods=["GET", "POST"])
@login_required
def create_test():
    if not current_user.is_teacher:
        return redirect(url_for("tests"))

    if request.method == "POST":
        teacher_id = Teachers.query.filter_by(
            user_id=current_user.user_id).first().teacher_id
        test_name = request.form.get("name")
        q1 = request.form.get("q1")
        q2 = request.form.get("q2")
        q3 = request.form.get("q3")
        a1 = request.form.get("a1")
        a2 = request.form.get("a2")
        a3 = request.form.get("a3")

        test = Tests(teacher_id=teacher_id, test_name=test_name)
        db.session.add(test)
        db.session.commit()

        test_question1 = TestQuestions(
            test_id=test.test_id, question=q1, answer=a1)
        test_question2 = TestQuestions(
            test_id=test.test_id, question=q2, answer=a2)
        test_question3 = TestQuestions(
            test_id=test.test_id, question=q3, answer=a3)
        db.session.add_all([test_question1, test_question2, test_question3])
        db.session.commit()
        return redirect(url_for("views.tests"))

    return render_template("create_test.html", test=None, q1=None, q2=None, q3=None)


@views.route("/update/test/<int:test_id>", methods=["POST", "GET"])
@login_required
def update_test(test_id):
    if not current_user.is_teacher:
        return redirect(url_for("views.tests"))

    if request.method == "POST":
        test = Tests.query.filter_by(test_id=test_id).first()
        test.test_name = request.form.get("name")
        test.date_edited = func.now()
        questions = TestQuestions.query.filter_by(test_id=test_id).all()
        questions[0].question = request.form.get("q1")
        questions[0].answer = request.form.get("a1")
        questions[1].question = request.form.get("q2")
        questions[1].answer = request.form.get("a2")
        questions[2].question = request.form.get("q3")
        questions[2].answer = request.form.get("a3")
        db.session.commit()
        return redirect(url_for("views.tests"))

    else:
        test = Tests.query.filter_by(test_id=test_id).first()
        questions = TestQuestions.query.filter_by(test_id=test_id).all()
        q1 = questions[0]
        q2 = questions[1]
        q3 = questions[2]
        return render_template("create_test.html", test=test, q1=q1, q2=q2, q3=q3)


@views.route("/delete/test/<int:test_id>", methods=["POST"])
@login_required
def delete_test(test_id):
    if not current_user.is_teacher:
        return redirect(url_for("views.tests"))
    if request.method == "POST":
        db.session.execute(
            text(f"DELETE FROM TestQuestions WHERE test_id={test_id}"))
        db.session.execute(text(f"DELETE FROM Tests WHERE test_id={test_id}"))
        db.session.commit()
    return redirect(url_for("views.tests"))


@views.route("/tests")
@login_required
def tests():
    if current_user.is_teacher:
        teacher_id = Teachers.query.filter_by(
            user_id=current_user.user_id).first().teacher_id
        tests = Tests.query.filter_by(teacher_id=teacher_id).all()
    else:
        tests = Tests.query.all()
    return render_template("tests.html", tests=tests)


@views.route("/users")
@login_required
def users():
    users = Users.query.all()
    return render_template("users.html", users=users)


@views.route("/users/teachers")
@login_required
def teachers():
    teachers = Teachers.query.all()
    users = []
    for teacher in teachers:
        users.append(teacher.user)
    return render_template("users.html", users=users)


@views.route("/users/students")
@login_required
def students():
    students = Students.query.all()
    users = []
    for student in students:
        users.append(student.user)
    return render_template("users.html", users=users)


@views.route("/take/test/<int:test_id>", methods=["GET", "POST"])
@login_required
def take_test(test_id):
    if current_user.is_teacher:
        return redirect(url_for("views.tests"))

    if request.method == "POST":
        a1 = request.form.get("q1")
        a2 = request.form.get("q2")
        a3 = request.form.get("q3")
        answers = [a1, a2, a3]

        student_id = Students.query.filter_by(
            user_id=current_user.user_id).first().student_id
        test_attempt = TestAttempts(student_id=student_id, test_id=test_id)
        db.session.add(test_attempt)
        db.session.commit()

        test_attempt_questions = []
        test_questions = TestQuestions.query.filter_by(test_id=test_id).all()
        for i in range(3):
            attempted_answer = answers[i]
            test_question = test_questions[i]
            test_attempt_question = TestAttemptQuestions(
                test_attempt_id=test_attempt.test_attempt_id, question_id=test_question.test_question_id, attempted_answer=attempted_answer)
            test_attempt_questions.append(test_attempt_question)
        db.session.add_all(test_attempt_questions)
        db.session.commit()
        return redirect(url_for("views.tests"))

    else:
        test = Tests.query.filter_by(test_id=test_id).first()
        questions = TestQuestions.query.filter_by(test_id=test_id).all()
        return render_template("take_test.html", test=test, questions=questions)
