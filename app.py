import os
from re import M # os module for accessing the os on the machine running flask
from flask import (Flask, render_template, make_response,  #Importing Flask and the ability to render templates
    redirect, request, session, url_for, flash) # Importing the ability to redirect users to other templates, request form data, use session cookies, standin urls with python and jinja, and flash information
from bson.objectid import ObjectId #Importing the ability to reference MongoDB object ids
from flask_pymongo import PyMongo   # Importing a module to use python with MongoDB
from werkzeug.security import generate_password_hash, check_password_hash   # Importing the ability to hash passwords and check hashed passwords
from itsdangerous import URLSafeTimedSerializer # Importing the ability to generate safe serialized id strings
import datetime # For... you know. The date... and the time.
from flask_mail import Mail, Message
if os.path.exists("env.py"):    # If statement so that the program works without env.py present
    import env                  # import secret information


app = Flask(__name__)           # setting flask to the standard __name__
app.config.from_object(__name__)


app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME") # Getting the DBNAME defined in env.py
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")       # Getting the URI for the DB
app.config["MAIL_SERVER"]= os.environ.get("MAIL_SERVER")
app.config["MAIL_PORT"]= os.environ.get("MAIL_PORT")
app.config["MAIL_USE_TLS"]= os.environ.get("MAIL_USE_TLS")
app.config["MAIL_USE_SSL"]= os.environ.get("MAIL_USE_SSL")
app.config["MAIL_USERNAME"]= os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"]= os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"]= os.environ.get("MAIL_DEFAULT_SENDER")
app.secret_key = os.environ.get("SECRET_KEY")               # Getting the secret key for accessing the DB
app.security_password_salt = os.environ.get("SECURITY_PASSWORD_SALT")
app.mail_default_sender = os.environ.get("MAIL_DEFAULT_SENDER")

mail = Mail(app)
mongo = PyMongo(app)
print(mail.use_tls)

# app route for home page(index)
@app.route("/")
@app.route("/about")
def about():
    return render_template("about.html")


@app.errorhandler(404)
def not_found():
    """Page not found."""
    return make_response(render_template("404.html"), 404)


@app.route("/library")
def library():
    return render_template("library.html")


@app.route("/play")
def play():
    return render_template("play.html")


@app.route("/character/<username>", methods=["GET", "POST"])
def character(username):
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    characters = mongo.db.characters.find(
        {"owner": username}
    )

    if request.method == "POST" and "form-submit" in request.form:
        if request.form.get("class") == "inward_fist":
            chosen_icon = "images/fist_icon.png"
        new_char = {
            "name": request.form.get("name").lower(),
            "chclass": request.form.get("class"),
            "current_exp": 0,
            "spent_exp": 0,
            "max_hp": 100,
            "max_energy": 100,
            "ac": 30,
            "hitroll": [5, 20],
            "dodge": 20,
            "block": 0,
            "parry": 0,
            "speed_max": 0,
            "damage": [2, 40],
            "dr": 0,
            "owner": username,
            "icon": chosen_icon,
        }
        mongo.db.characters.insert_one(new_char)
        flash("Character Created")
        return redirect(url_for("character", username=session["user"]))

    if session["user"]:
        return render_template("character.html", username=username, characters=characters)


    return redirect(url_for("login"))

    # Search through characters to find those that belong to the user and pump those into a list
    # Push all their stats into each list item
    # if request.method == "POST":
    # Make sure the player has the requisite points, deduct the points, add them to the spent points list, and award the training


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
                #"confirmed": False,
                "email": request.form.get("email"),
                "registered_on": datetime.datetime.now(),
            }
            mongo.db.users.insert_one(register)
        else:
            flash("Password fields do not match")
            return redirect(url_for("register"))

        # put the new user into session cookie
        #token = generate_confirmation_token(request.form.get("email"))
        #confirm_url = url_for('confirm_email', token=token, _external=True)
        ##html = render_template('activate.html', confirm_url=confirm_url)
        #subject = "Please confirm your email"
        #send_email(request.form.get("email"), subject, html)

        session["user"] = request.form.get("username").lower()
        flash("Registration Successful")
        return redirect(url_for("character", username=session["user"]))
    return render_template("register.html")


@app.route("/logout")
def logout():
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


#@app.route('/confirm/<token>')
#def confirm_email(token):
#    try:
#        email = confirm_token(token)
#    except:
##        flash("The confirmation link is invalid or has expired.")
#    user = mongo.db.users.find_on({"email": email})
#    if user.confirmed:
#        flash("Account already confirmed, please login.")
#    else:
##        user.confirmed = True
#        session["user"] = user
#        flash("You have confirmed your account. High five!")
#    return redirect(url_for("character"))


# Generate key for confirmation email
#def generate_confirmation_token(email):
#    serializer = URLSafeTimedSerializer(app.secret_key)
#    return serializer.dumps(email, salt=app.security_password_salt)


#def confirm_token(token, expiration=3600):
#    serializer = URLSafeTimedSerializer(app.secret_key)
#    try:
#        email = serializer.loads(
#            token,
#            salt=app.security_password_salt,
#            max_age=expiration
#        )
#    except:
#        return False
#    return email


#def send_email(to, subject, template):
#    print(app.config["MAIL_SERVER"])
#    msg = Message(
#        subject,
#        recipients=[to],
#        html=template,
#    )
#    mail.send(msg)



if __name__ == "__main__":  # If the name is valid
    app.run(host=os.environ.get("IP"),#Setting the ip
            port=int(os.environ.get("PORT")),#setting the port #
            debug=True) #Using debug mode while developing the backend