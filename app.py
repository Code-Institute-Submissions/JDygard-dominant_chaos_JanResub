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
from flask_socketio import SocketIO
import math
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
socketio = SocketIO(app)

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



@socketio.on('message')
def handle_message(data):
    print('received message: ' + data)



@app.route("/leaderboard")
def leaderboard():
    characters = list(mongo.db.characters.find().sort("spent_experience", 1))
    return render_template("leaderboard.html", characters=characters)


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    try:
        username = mongo.db.users.find_one(
            {"username": username})["username"]
        characters = mongo.db.characters.find(
            {"owner": username})
    except:
        username = "Username does not exist"
        characters = []
    #####     POST to DB stuff     #####
    if request.method == "POST":
        form_name = request.form['form-name']
        #####      Create character modal form      #####
        if form_name == "create-character":
            existing_char = mongo.db.characters.find_one(
                {"name": request.form.get("name").lower()}
            )

            if existing_char:
                flash("Character name taken, try again with a more differenter name")
                return redirect(
                        url_for("profile", username=session["user"]))

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
                "speed_max": 100,
                "damage": [2, 40],
                "dr": 0,
                "owner": username,
                "href": "character/" + request.form.get("name").lower(),
                "winloss": [0, 0]
            }
            if request.form.get("class") == "inward_fist":
                new_char["icon"] = "images/fist-icon.png"
                new_char["hands"] = 0
                new_char["legs"] = 0
                new_char["torso"] = 0
                new_char["arms"] = 0
                new_char["discipline"] = 0
            mongo.db.characters.insert_one(new_char)
            flash("Character Created")
            return redirect(url_for("profile", username=session["user"]))
        
        if form_name == "delete-account":
            user = mongo.db.users.find_one({"username":username})
            print(user["password"])
            if check_password_hash(user["password"], request.form.get("password")) and request.form.get("username").lower() == username:
                    mongo.db.characters.delete_many({"owner": user["username"]})
                    mongo.db.users.remove({"username": user["username"]})
                    session.pop("user")


    if session["user"]:
        return render_template("profile.html", username=username, characters=characters)



@app.route("/character/<charactername>", methods=["GET", "POST"])
def character(charactername):
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    charactername = mongo.db.characters.find_one(
        {"name": charactername}
    )

    if request.method == "POST":
        form_name = request.form['form-name']
        if form_name == "arms":
            training = int(request.form.get('flask-arms'))
            arms = int(charactername["arms"])
            spent_experience = charactername["spent_exp"]
            experience = int(charactername["current_exp"])
            cost = calculateCost(arms, training)
            updatefilter= {"name": charactername["name"]}
            if experience >= cost and training + arms <= 100:
                submit = {
                    "arms": training + arms,
                    "current_exp": experience - cost,
                    "spent_exp": spent_experience + cost              
                }
                mongo.db.characters.update_one(updatefilter, {"$set": submit})
                flash("Training complete")
                return redirect(url_for("character", charactername=charactername['name']))
            else:
                flash("Insufficient experience for training")
                return redirect(url_for("character", charactername=charactername['name']))

        if form_name == "hands":
            training = int(request.form.get('flask-hands'))
            hands = int(charactername["hands"])
            spent_experience = charactername["spent_exp"]
            experience = int(charactername["current_exp"])
            cost = calculateCost(hands, training)
            updatefilter= {"name": charactername["name"]}
            if experience >= cost and training + hands <= 100:
                submit = {
                    "hands": training + hands,
                    "current_exp": experience - cost,
                    "spent_exp": spent_experience + cost              
                }
                mongo.db.characters.update_one(updatefilter, {"$set": submit})
                flash("Training complete")
                return redirect(url_for("character", charactername=charactername['name']))
            else:
                flash("Insufficient experience for training")
                return redirect(url_for("character", charactername=charactername['name']))

        if form_name == "legs":
            training = int(request.form.get('flask-legs'))
            legs = int(charactername["legs"])
            spent_experience = charactername["spent_exp"]
            experience = int(charactername["current_exp"])
            cost = calculateCost(legs, training)
            updatefilter= {"name": charactername["name"]}
            if experience >= cost and training + legs <= 100:
                submit = {
                    "legs": training + legs,
                    "current_exp": experience - cost,
                    "spent_exp": spent_experience + cost              
                }
                mongo.db.characters.update_one(updatefilter, {"$set": submit})
                flash("Training complete")
                return redirect(url_for("character", charactername=charactername['name']))
            else:
                flash("Insufficient experience for training")
                return redirect(url_for("character", charactername=charactername['name']))

        if form_name == "torso":
            training = int(request.form.get('flask-torso'))
            torso = int(charactername["torso"])
            spent_experience = charactername["spent_exp"]
            experience = int(charactername["current_exp"])
            cost = calculateCost(torso, training)
            updatefilter= {"name": charactername["name"]}
            if experience >= cost and training + torso <= 100:
                submit = {
                    "torso": training + torso,
                    "current_exp": experience - cost,
                    "spent_exp": spent_experience + cost              
                }
                mongo.db.characters.update_one(updatefilter, {"$set": submit})
                flash("Training complete")
                return redirect(url_for("character", charactername=charactername['name']))
            else:
                flash("Insufficient experience for training")
                return redirect(url_for("character", charactername=charactername['name']))

        if form_name == "discipline":
            discipline = int(charactername["discipline"])
            cost = disciplineCost(discipline)
            spent_experience = int(charactername["spent_exp"])
            experience = int(charactername["current_exp"])
            if experience > cost:
                submit = {
                    "discipline": discipline + 1,
                    "current_exp": experience - cost,
                    "spent_exp": spent_experience + cost
                }
                mongo.db.characters.update_one({"name": charactername["name"]}, {"$set": submit})
            else:
                flash("Insufficient experience for training")
                return redirect(url_for("character", charactername=charactername['name']))

            
        if form_name == "char-bio":
            submit = {
                "charbio": request.form.get('char-bio')
            }
            mongo.db.characters.update_one({"name": charactername["name"]}, {"$set": submit})
            flash("Bio updated")

        if form_name == "delete":
            if request.form.get('delete') == charactername['name']:
                mongo.db.characters.remove({"name": charactername["name"]})
 
    return render_template("character.html", username=username, charactername=charactername)


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
                        url_for("profile", username=session["user"]))
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
                "email": request.form.get("email"),
                "registered_on": datetime.datetime.now(),
            }
            mongo.db.users.insert_one(register)
        else:
            flash("Password fields do not match")
            return redirect(url_for("register"))

        session["user"] = request.form.get("username").lower()
        flash("Registration Successful")
        return redirect(url_for("profile", username=session["user"]))
    return render_template("register.html")


@app.route("/logout")
def logout():
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))

def calculateCost(current, iterations):
    initialValue = current
    result = 0
    i = 0
    while i < int(iterations):
        result += math.sqrt(initialValue) * 1500
        initialValue += 1
        i += 1
    return round(result)

def disciplineCost(current):
    return (current + 1) * 500000


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