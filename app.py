import os
import static.py.cfg as cfg
from re import M # os module for accessing the os on the machine running flask
from flask import (Flask, render_template, make_response,  #Importing Flask and the ability to render templates
    redirect, request, session, url_for, flash) # Importing the ability to redirect users to other templates, request form data, use session cookies, standin urls with python and jinja, and flash information
from bson.objectid import ObjectId #Importing the ability to reference MongoDB object ids
from flask_pymongo import PyMongo   # Importing a module to use python with MongoDB
from werkzeug.security import generate_password_hash, check_password_hash   # Importing the ability to hash passwords and check hashed passwords
import datetime # For... you know. The date... and the time.
from flask_socketio import SocketIO, emit, disconnect
from threading import Lock
import random

#from bson import json_util
#from bson.json_util import loads
#from bson.json_util import dumps

import time
import math
import json
if os.path.exists("env.py"):    # If statement so that the program works without env.py present
    import env                  # import secret information


app = Flask(__name__)           # setting flask to the standard __name__
app.config.from_object(__name__)

async_mode = None
thread = None
thread_lock = Lock()

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME") # Getting the DBNAME defined in env.py
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")       # Getting the URI for the DB
app.secret_key = os.environ.get("SECRET_KEY")               # Getting the secret key for accessing the DB
app.security_password_salt = os.environ.get("SECURITY_PASSWORD_SALT")

mongo = PyMongo(app)
socket_ = SocketIO(app, async_mode=async_mode)

# Combat system variables
combat_switch = False
curtime = time.time()


#####                  Fight instance logic                    #####
##### This is where all of the functions related to resolving  #####
##### the actual combat instances will be located.             #####
##### There is a better solution involving blueprints that was #####
##### scrapped due to time constraints. This uglier solution   #####
##### will have to suffice.                                    #####


#Roll to hit. "type" will refer to different attacks so that this function is multipurpose
def rth(ch, vict, type): 
    # This will wind up having to be significantly more complex
    # because of the nature of different classes having some varies hit or damage effects.
    if ch["is_dead"] != True and vict["is_dead"] != True:
        if type == "auto":
            hitroll = dice_roll( ch["hitroll"][0], ch["hitroll"][1] ) # Call the dice roll function
            if hitroll >= vict["ac"]:   # If it clears their armor class
                dbp(ch, vict, type)           # Call on the Dodge Block and Parry function
            else:                       # Otherwise
                miss("miss", ch, vict)               # Send it to the miss function with "hit"


# After a hit registers, run the dbp function, short for dodge, block and parry
def dbp(ch, vict, type): # dodge block parry
    # Check dodge roll
    dodge = vict["dodge"]
    dodgeroll = dice_roll( 1, 100 )
    if dodgeroll <= dodge:
        miss("dodge", ch, vict)
        return

    # Check block roll
    block = vict["block"]
    blockroll = dice_roll( 1, 100 )
    if blockroll <= block:
        miss("block", ch, vict)
        return

    # Check parry roll
    parry = vict["parry"]
    parryroll = dice_roll( 1, 100 )
    if parryroll <= parry:
        miss("parry", ch, vict)
        return

    # If damage isn't prevented, calculate damage
    dmg(ch,vict, type)


# dmg( Damage ) function for calculating damage and checking for death
def dmg(ch, vict, type):
    damage_dice = ch["damage"][0]  # Collect the number of damage dice to be rolled
    damage_sides = ch["damage"][1] # and how many facets those dice have
    damage_resistance = ch["dr"]  # Collect the damage resistance
    damage = dice_roll( damage_dice, damage_sides )    #roll damage
    damage -= damage_resistance   #subtract vict["dr"]
    vict["hp"] -= damage    #apply damage
    add_to_queue("auto", damage)
    if vict["hp"] <= 0:
        victory(ch, vict)


def miss(case, ch, vict):
    if case == "miss" and ch["name"] == cfg.fighter1["name"]:
        print("You swing for your opponent, but miss.")
    if case == "dodge" and ch["name"] == cfg.fighter1["name"]:
        print("You swing for your opponent, but your attack is dodged.")
    if case == "block" and ch["name"] == cfg.fighter1["name"]:
        print("You swing for your opponent, but your attack is blocked.")
    if case == "parry" and ch["name"] == cfg.fighter1["name"]:
        print("You swing for your opponent, but your attack is parried.") 



def auto_atk(ch, vict):
    spd = ch["speed"]
    aps = spd // 40
    ch["speed"] = spd % 40 
    for attacks in range(0, aps):
        rth(ch, vict, "auto")


def victory(ch, vict):
    vict["is_dead"] = True
    print(f"{vict['name']} is incapacitated and will die soon, if not aided.")


def turn_timer(player1, player2):
    print("")
    print(f"<hp: {player1['hp']}/{player1['max_hp']}>")
    tick(player1, player2)
    time.sleep(3)
    turn_queue(player1, player2)


def turn_queue(player1, player2):
    if player1["is_dead"] == False and player2["is_dead"] == False:
        auto_atk(player1, player2)
        auto_atk(player2, player1)
        turn_timer(player1, player2)


def tick(player1, player2):
    player1["speed"] += player1["speed_max"]
    player2["speed"] += player2["speed_max"]


def dice_roll(dice, sides):
    rolls = []
    result = 0
    for i in range(0,dice):
        n = random.randint(0,sides)
        rolls.append(n)
    for x in rolls:
        result += x
    return result


def add_to_queue(method, dmg):
    data = {
        "method": method,
        "damage": dmg,
        "extra": None
    }
    cfg.queue.append(data)


##### Functions that app.py uses to prepare data for the above fight logic #####


def character_dump(username):
    """ Package character list into a JSON with only relevant info """
    cursor = mongo.db.characters.find({"owner": username},
        projection={"name": 1, "chclass": 1})
    return json.dumps(list(cursor),
        cls=MongoJsonEncoder)


def prepare_character(chname, chusername):
    """ FIXME I think the actual stats as affected by body, etc. could be calculated here if not done in the combat code """
    name = mongo.db.characters.find_one({"name": chname})
    if name["owner"] == chusername:
        chclass = name["chclass"]
        stats = {
            "name": name["name"],
            "hp": name["max_hp"],
            "max_hp": name["max_hp"],
            "ac": name["ac"],
            "hitroll": name["hitroll"],
            "dodge": name["dodge"],
            "block": name["block"],
            "parry": name["parry"],
            "speed": name["speed_max"],
            "speed_max": name["speed_max"],
            "damage": name["damage"],
            "dr": name["dr"],
            "is_dead": False
        }
        if chclass == "fist":
            stats["torso"] = name["torso"]
            stats["hands"] = name["hands"]
            stats["arms"] = name["arms"]
            stats["legs"] = name["legs"]
            stats["discipline"] = name["discipline"]
            stats["ki"] = name["ki"]
            stats["max_ki"] = name["ki"]
        return stats
    else:
        return False

def prepare_opponent():
    stats = {
        "name": "Meanie",
        "hp": 100,
        "max_hp": 100,
        "ac": 30,
        "hitroll": [5, 20],
        "dodge": 20,
        "block": 10,
        "parry": 0,
        "speed": 100,
        "speed_max": 100,
        "damage": [2, 40],
        "dr": 0,
        "is_dead": False
    }
    return stats


### SocketIO emit event handlers ###


@socket_.on('query', namespace="/test")
def handle_query(data):
    print(data)
    time.sleep(0.5)
    if cfg.queue == []:
        emit('reply', "empty")
        print("reply (empty)")
    else:
        print("reply (loaded)")
        emit('reply', cfg.queue,
            broadcast=True)
    cfg.queue = []


# SocketIO handler for character list request
@socket_.on('message', namespace="/test")
def handle_message(data):
    """ Handle character list request from char-select"""
    print(session["user"].upper() + " is connected.")
    if data == "requestcharacterlist":
        lookup = character_dump(session["user"])
        emit('response', lookup,
            broadcast=True)


# SocketIO handler for preparing the fight logic
@socket_.on('chardata', namespace="/test")
def chardata(data):
    """ Prepare fighter data for fight instance """
    cfg.fighter1 = prepare_character(data, session["user"])
    cfg.fighter2 = prepare_opponent()
    print(data + " is prepared")
    emit('character', "prepared",
        broadcast=True)


@socket_.on('playdata', namespace="/test")
def playdata(data):
    """ Handle activation of the """
    if data == "play init":
        turn_queue(cfg.fighter1, cfg.fighter2)


@socket_.on('queue', namespace="/test")
def handle_queue(data):
    print(data)
    """ FIXME 
    Here we will have:
    character building from the database (function)
        We can keep this in fightbase.py
    opponent build from template (function)
        same in fightbase.py
    call timer (function)
        I mean start the combat timer/build queue thing
    dump info from combat to frontend




    FIXME
    Receive commands from the frontend and put them in the queue.
    Setup calculations and feed them back through to phaser.
    Determine the winner and add experience.
    Death penalty?
    

    """
####            App routes                 ####
#### This is where app routes for html pages###
#### and sockets will be located           ####


# app route for home page(index)
@app.route("/")
@app.route("/about")
def about():
    return render_template("about.html")


# 404 error handler
@app.errorhandler(404)
def not_found():
    """Page not found."""
    return make_response(render_template("404.html"), 404)


# Library page route
@app.route("/library")
def library():
    return render_template("library.html")


# Play page route
@app.route("/play")
def play():
    return render_template("play.html", sync_mode=socket_.async_mode)


# Process JSON data with objectid intact
class MongoJsonEncoder(json.JSONEncoder):
    """Encode JSON, supporting bson.ObjectID."""
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)


# Library source routes:
@app.route("/library/general")
def general():
    return render_template("library/general.html")


@app.route("/library/chi-xin")
def chi_xin():
    return render_template("library/chi-xin.html")


@app.route("/library/inward-fist")
def inward_fist():
    return render_template("library/inward-fist.html")


@app.route("/library/sorcerer")
def sorcerer():
    return render_template("library/sorcerer.html")


@app.route("/library/outward-fist")
def outward_fist():
    return render_template("library/outward-fist.html")


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
                "current_exp": 99999999,
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
                new_char["max_ki"] = 0
            mongo.db.characters.insert_one(new_char)
            flash("Character Created")
            return redirect(url_for("profile", username=session["user"]))
        
        if form_name == "delete-account":
            user = mongo.db.users.find_one({"username":username})
            if check_password_hash(user["password"], request.form.get("password")) and request.form.get("username").lower() == username:
                    mongo.db.characters.delete_many({"owner": user["username"]})
                    mongo.db.users.remove({"username": user["username"]})
                    session.pop("user")
        

        if form_name == "change-password":
            user = mongo.db.users.find_one({"username":username})
            if check_password_hash(user["password"], request.form.get("password")):
                if request.form.get("new-password") == request.form.get("password2"):
                    passwordupdate = generate_password_hash(request.form.get("new-password"))
                    mongo.db.users.update_one({"username": username}, {"$set": {"password": passwordupdate}})
                    flash("Password updated")
                else:
                    flash("Password not updated: Fields did not match.")
            else:
                flash("Password not updated: Current password entered incorrectly.")


        if form_name == "change-email":
            if request.form.get("email") == request.form.get("confirm-email"):
                mongo.db.user.update_one({"username": username}, {"$set": {"email": request.form.get("email")}})
                flash("Email updated")
            else:
                flash("Email not updated: Fields did not match.")


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
        bodytrain_strings = ["arms", "hands", "legs", "torso"]
        """ Following code block builds four statements to listen for bodytraining POSTs """
        for string in range(len(bodytrain_strings)):
            if form_name == bodytrain_strings[string]:
                training = int(request.form.get('flask-' + bodytrain_strings[string]))
                bodytrain = int(charactername[bodytrain_strings[string]])
                spent_experience = charactername["spent_exp"]
                experience = int(charactername["current_exp"])
                cost = calculateCost(bodytrain, training)
                updatefilter= {"name": charactername["name"]}
                if experience >= cost and training + bodytrain <= 100:
                    submit = {
                        bodytrain_strings[string]: training + bodytrain,
                        "current_exp": experience - cost,
                        "spent_exp": spent_experience + cost              
                    }
                    mongo.db.characters.update_one(updatefilter, {"$set": submit})
                    flash("Training complete")
                    return redirect(url_for("character", charactername=charactername['name']))
                else:
                    flash("Insufficient experience for training")
                    return redirect(url_for("character", charactername=charactername['name']))

        """ Following code block listens for discipline training POSTs """
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
            if request.form.get('delete').lower() == charactername['name']:
                mongo.db.characters.remove({"name": charactername["name"]})
                flash("Character deleted")
                return redirect(url_for("profile", username=session["user"]))
            else:
                flash("Character not deleted, check name and try again.")
 
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


"""
Turns out that this is straight up garbage-trash.
We'll be using APEventscheduler for this.

This is the most elegant way to do it, but we may be forced to do something more... brutish. To maintain the sort of control I want, and make it extensible.

Issues to solve:
    Build it up in a way that it can do this by seconds for queue abilities.
    How does it know which players to be issuing commands for?

THIS is for autoattacks and submitting items from the frontend to the queue
while combat_switch == True:
    curtime = time.time()

    if curtime % 5 == 0:
        execute_command()


THIS will be for player-issued commands. This way speed can JUST be for autoattacks.
while combat_switch == True:
    curtime = time.time()

    for cmd in cmds:
        if curtime % cmd["interval"] == 0:
        execute_command(cmd["command"])
      
cmds = [
    {
        "command": "doNothing",
        "delay": 5
    },
    {
        "command": "doSomething",
        "interval": 3
    }
]
"""


if __name__ == "__main__":  # If the name is valid
    socket_.run(app, host=os.environ.get("IP"),#Setting the ip
            port=int(os.environ.get("PORT")),#setting the port #
            debug=True) #Using debug mode while developing the backend