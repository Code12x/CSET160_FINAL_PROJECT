from functools import wraps
import jwt
import pymysql
from environs import Env
from flask import Flask, render_template, request

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


def access_token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        if not has_access_token():
            app.redirect("/login")
        return func(*args, **kwargs)
    return decorated


def has_access_token():
    """Returns True if there is a valid JWT Token in the head, and it sets request.user = payload.get("user").
    Returns False if there are no JWT tokens provided or if the JWT token is invalid"""
    token = request.headers.get("authorization")
    if not token:
        return False
    else:
        try:
            token = token.split(" ")[1]
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=[
                                 "HS256"], verify_signature=True)
            print("\n\n--------------------\n" +
                  payload.get("user") + "\n----------------\n\n")
            request.user = payload.get("user")
            return True
        except jwt.exceptions.InvalidTokenError:
            print("Invalid Token Error")
            return False
        except jwt.exceptions.DecodeError:
            print("DecodeError")
            return False


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    # return render_template("register.html")
    pass


@app.route("/cool")
@access_token_required
def cool():
    return render_template("cool.html", name=request.user)


@app.route("/users")
@access_token_required
def users():
    # use request.args.get('filter')
    pass


@app.route("/tests")
@access_token_required
def tests():
    pass


@app.route("/test/take/<int:test_id>", methods=["GET", "POST"])
@access_token_required
def test_take_get(test_id):
    pass


@app.route("/test/create/<int:test_id>", methods=["GET", "POST", "UPDATE"])
@access_token_required
def test_create_get(test_id):
    pass


if __name__ == "__main__":
    app.run(debug=True, port=5000)
