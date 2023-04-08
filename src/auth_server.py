from datetime import datetime, timedelta

import jwt
from environs import Env
from flask import Flask, render_template, request, make_response, session, redirect

# Environmental variables
env = Env()
env.read_env()

# Flask Setup
app = Flask(__name__)
app.config['SECRET_KEY'] = env("SECRET_KEY")

# Current Tokens
tokens = []


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form['username'] and request.form['password'] == '123456':
            session['logged_in'] = True

            token = jwt.encode({
                'user': request.form['username'],
                'exp': datetime.utcnow() + timedelta(seconds=60*5)
            },
                app.config['SECRET_KEY'])
            return make_response({"token": token})
        else:
            return make_response('Unable to verify', 403,
                                 {'WWW-Authenticate': 'Basic realm: "Authentication Failed!"'})
    elif request.method == "GET":
        return render_template("login.html")


@app.route('/logout', methods=["POST"])
def logout():
    token = request.get_json().get('token')
    if not token:
        return make_response({"message": "Missing Token"})
    else:
        token = token.split(" ")[1]
        if token in tokens:
            tokens.remove(token)
            session.clear()
        else:
            return make_response({"message": "Invalid Token"})

    redirect("http://localhost:5000/")


if __name__ == "__main__":
    app.run(debug=True, port=4000)
