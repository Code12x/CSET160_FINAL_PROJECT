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

    return render_template("create_test.html")


@views.route("/tests")
@login_required
def tests():
    if current_user.is_teacher:
        teacher_id = Teachers.query.filter_by(user_id=current_user.user_id)
        tests = Tests.query.fiter_by(teacher_id=teacher_id)
    else:
        tests = Tests.query.all()
    return render_template("tests.html", test=tests)


@views.route("/users")
@login_required
def users():
    query = text("SELECT * FROM Users")
    users = db.session.execute(query).fetchall()
    return render_template("users.html", users=users)
