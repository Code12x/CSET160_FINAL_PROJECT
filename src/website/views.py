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
        return redirect(url_for("login"))

    if request.method == "POST":
        teacher_id = db.session.execute(
            text(f"SELECT teacher_id FROM Teachers WHERE user_id={current_user.user_id}"))

    return render_template("create_test.html")


@views.route("/tests")
@login_required
def tests():
    return render_template("tests.html")


@views.route("/users")
@login_required
def users():
    query = text("SELECT * FROM Users")
    users = db.session.execute(query).fetchall()
    return render_template("users.html", users=users)
