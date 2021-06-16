import os # os module for accessing the os on the machine running flask
from flask import (Flask, render_template,  #Importing Flask and the ability to render templates
    redirect, request, session, url_for, flash) # Importing the ability to redirect users to other templates, request form data, use session cookies, standin urls with python and jinja, and flash information
from bson.objectid import ObjectId #Importing the ability to reference MongoDB object ids
from flask_pymongo import PyMongo   # Importing a module to use python with MongoDB
from werkzeug.security import generate_password_hash, check_password_hash   # Importing the ability to hash passwords and check hashed passwords
from itsdangerous import URLSafeTimedSerializer # Importing the ability to generate safe serialized id strings
import datetime # For... you know. The date... and the time.
if os.path.exists("env.py"):    # If statement so that the program works without env.py present
    import env                  # import secret information


app = Flask(__name__)           # setting flask to the standard __name__


app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME") # Getting the DBNAME defined in env.py
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")       # Getting the URI for the DB
app.secret_key = os.environ.get("SECRET_KEY")               # Getting the secret key for accessing the DB
app.security_password_salt = os.environ.get("SECURITY_PASSWORD_SALT")


mongo = PyMongo(app)


# app route for home page(index)
@app.route("/")
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/library")
def library():
    return render_template("library.html")


@app.route("/play")
def play():
    return render_template("play.html")


# I'm going to need to establish a session and user before this section can be done
@app.route("/character", methods=["GET", "POST"])
def character():
    return render_template("character.html")


@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            if check_password_hash(existing_user["password"], request.form.get("password")):
                    session["user"] = request.form.get("username").lower()
                    flash("Welcome, {}".format(request.form.get("username")))
                    return redirect(
                        url_for("character", username=session["user"]))
            else:
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))
            
    return render_template("login.html")


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})# Check if the username already exists

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))
        
        if request.form.get("password") == request.form.get("password_confirm"):
            register = {
                "username": request.form.get("username").lower(),
                "password": generate_password_hash(request.form.get("password")),
                "confirmed": False,
                "email": request.form.get("email"),
                "registered_on": datetime.datetime.now(),
            }
            mongo.db.users.insert_one(register)
        else:
            flash("Password fields do not match")
            return redirect(url_for("register"))

        # put the new user into session cookie
        token = generate_confirmation_token(request.form.get("email"))s
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful")
        return redirect(url_for("character", username=session["user"]))
    return render_template("register.html")


@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash("The confirmation link is invalid or has expired.")
    user = mongo.db.users.find_on({"email": email})
    if user.confirmed:
        flash("Account already confirmed, please login.")
    else:
        user.confirmed = True
        session["user"] = user
        flash("You have confirmed your account. High five!")
    return redirect(url_for("character"))


@app.route("/logout")
def logout():
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


# Generate key for confirmation email
def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.secret_key)
    return serializer.dumps(email, salt=app.security_password_salt)

def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.secret_key)
    try:
        email = serializer.loads(
            token,
            salt=app.security_password_salt,
            max_age=expiration
        )
    except:
        return False
    return email


        


if __name__ == "__main__":  # If the name is valid
    app.run(host=os.environ.get("IP"),#Setting the ip
            port=int(os.environ.get("PORT")),#setting the port #
            debug=True) #Using debug mode while developing the backend