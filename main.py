from flask import Flask, render_template, request, make_response, redirect, url_for
import random
from models import User, db

app = Flask(__name__)
db.create_all()


@app.route("/", methods=["GET"])
def index():
    email_address = request.cookies.get("email")
    if email_address:
        user = db.query(User).filter_by(email=email_address).first()
    else:
        user = None

    return render_template("index.html", user=user)


@app.route("/login", methods=["POST"])
def login():
    name = request.form.get("user-name")
    email = request.form.get("user-email")

    secret_number = random.randint(1, 30)

    user = db.query(User).filter_by(email=email).first()

    if not user:
        user = User(name=name, email=email, secret_number=secret_number)

        db.add(user)
        db.commit()

    response = make_response(redirect(url_for("index")))
    response.set_cookie("email", email)

    return response


@app.route("/result", methods=["POST"])
def result():
    guess = int(request.form.get("my_guess"))
    email_address = request.cookies.get("email")

    user = db.query(User).filter_by(email=email_address).first()

    if guess == user.secret_number:
        correct_hl = "Congratulations!!!"
        correct_message = "Correct! The secret number is {0}.".format(str(user.secret_number))

        new_secret = random.randint(1, 30)
        user.secret_number = new_secret

        db.add(user)
        db.commit()

        return render_template("result.html", correct=correct_message, correct_hl=correct_hl)

    elif guess > user.secret_number:
        message = "Sorry, {0} is not correct. Try something smaller...".format(str(guess))
        return render_template("result.html", message=message)
    elif guess < user.secret_number:
        message = "Sorry, {0} is incorrect. Try something bigger...".format(str(guess))
        return render_template("result.html", message=message)


if __name__ == '__main__':
    app.run()
