from datetime import datetime, timedelta
from functools import wraps
import jwt
import pymysql
from environs import Env
from flask import Flask, make_response, render_template, request, redirect, session
from os import urandom

# Environmental variables
env = Env()
env.read_env()

MYSQL_USERNAME = env("MYSQL_USERNAME")
MYSQL_PASSWORD = env("MYSQL_PASSWORD")
MYSQL_HOST = env("MYSQL_HOST")
MYSQL_PORT = env.int("MYSQL_PORT")
MYSQL_DATABASE = "CSET160_FINAL_PROJECT"

# Flask Setup
app = Flask(__name__)
app.config['SECRET_KEY'] = env("SECRET_KEY")

# MySQL Setup
connection = pymysql.connect(host=MYSQL_HOST, port=MYSQL_PORT,
                             user=MYSQL_USERNAME, password=MYSQL_PASSWORD, database=MYSQL_DATABASE)

refresh_tokens = []

# def access_token_required(func):
#     @wraps(func)
#     def decorated(*args, **kwargs):
#         if not has_access_token():
#             app.redirect("/login")
#         return func(*args, **kwargs)
#     return decorated


def validate_token(token):
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'],
                             algorithms=["HS256"], verify_signature=True)
        return {"status": "success", "payload": payload}
    except jwt.exceptions.InvalidTokenError as e:
        return {"status": "invalid", "error": e}
    except:
        return {"status": "error", "error": e}


def generate_token(user, refresh=False):
    payload = {'user': user}
    if refresh:
        payload['salt'] = urandom(16).hex()
    else:
        payload['exp'] = datetime.utcnow() + 60*10

    token = jwt.encode(payload, app.config['SECRET_KEY'])
    if refresh:
        refresh_tokens.append(token)
    return token


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form['username'] and request.form['password'] == '123456':
            session['logged_in'] = True

            refresh_token = generate_token(
                request.form['username'], refresh=True)
            access_token = generate_token(request.form["username"])

            res = make_response({
                "access_token": access_token,
            })
            res.set_cookie("refresh_token", refresh_token)
            return res
        else:
            return make_response('Unable to verify', 403,
                                 {'WWW-Authenticate': 'Basic realm: "Authentication Failed!"'})
    elif request.method == "GET":
        return render_template("login.html")


@app.route('/logout', methods=["DELETE"])
def logout():
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        return make_response({"status": "error", "error": "missing token"})
    else:
        if refresh_token in refresh_tokens:
            refresh_tokens.remove(refresh_token)
            return make_response({"status": "success"})
        else:
            return make_response({"status": "error", "error": "invalid"})


@app.route("/token", methods=["POST"])
def token():
    refresh_token = request.cookies.get("refresh_token")

    if refresh_token in refresh_tokens:
        token_status = validate_token(refresh_token)
        if token_status.status == "success":
            return make_response({"access_token": generate_token(token_status.payload.user)})
        else:
            return app.redirect("/login")
    else:
        return app.redirect("/login")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    # return render_template("register.html")
    pass


@app.route("/cool")
def cool():
    access_token = request.args.get("token")
    if access_token:
        token_status = validate_token(access_token)
        if token_status.get("status") == "success":
            return render_template("cool.html", name=token_status.get("payload").get("user"))
        else:
            return make_response(token_status)
    else:
        return redirect("/login")


@app.route("/users")
# @access_token_required
def users():
    # use request.args.get('filter')
    pass


@app.route("/tests")
# @access_token_required
def tests():
    pass


@app.route("/test/take/<int:test_id>", methods=["GET", "POST"])
# @access_token_required
def test_take_get(test_id):
    pass


@app.route("/test/create/<int:test_id>", methods=["GET", "POST", "UPDATE"])
# @access_token_required
def test_create_get(test_id):
    pass


if __name__ == "__main__":
    app.run(debug=True, port=5000)
