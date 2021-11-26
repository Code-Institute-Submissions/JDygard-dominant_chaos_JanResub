import os
import static.py.cfg as cfg
from re import M
from flask import (Flask, render_template,
                   make_response,
                   redirect, request, session, url_for, flash)
from bson.objectid import ObjectId
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from flask_socketio import SocketIO, emit
from threading import Lock
import random
import time
import math
import json
if os.path.exists("env.py"):
    import env


app = Flask(__name__)
app.config.from_object(__name__)

async_mode = None
thread = None
thread_lock = Lock()

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")
app.security_password_salt = os.environ.get("SECURITY_PASSWORD_SALT")

mongo = PyMongo(app)
socket_ = SocketIO(app, async_mode=async_mode)

# Combat system variables
combat_switch = False
curtime = time.time()


#                  Fight instance logic                    #####
# This is where all of the functions related to resolving  #####
# the actual combat instances will be located.             #####
# There is a better solution involving blueprints that was #####
# scrapped due to time constraints. This uglier solution   #####
# will have to suffice.                                    #####


# Roll to hit. "type" will refer to
# different attacks so that this function is multipurpose
def roll_to_hit(ch, vict, type):
    # because of the nature of different
    # classes having some varies hit or damage effects.
    if ch["is_dead"] is not True and vict["is_dead"] is not True:
        if type == "auto":
            hitroll = dice_roll(ch["hitroll"][0], ch["hitroll"][1])
            if hitroll >= vict["ac"]:
                dodge_block_parry(ch, vict, type)
            else:
                miss("miss", ch, type)


# After a hit registers, run the dbp function, short for dodge, block and parry
def dodge_block_parry(ch, vict, type):
    # Check dodge roll
    dodge = vict["dodge"]
    dodgeroll = dice_roll(1, 100)
    if dodgeroll <= dodge:
        miss("dodge", ch, type)
        return

    # Check block roll
    block = vict["block"]
    blockroll = dice_roll(1, 100)
    if blockroll <= block:
        miss("block", ch, type)
        return

    # Check parry roll
    parry = vict["parry"]
    parryroll = dice_roll(1, 100)
    if parryroll <= parry:
        miss("parry", ch, type)
        return

    # If damage isn't prevented, calculate damage
    dmg(ch, vict, type)


def combo_calculator(ch, vict, data):
    if data > 10:
        cfg.fighter1["ki"] = 0
        return
    if data == 10:
        # Quivering palm
        print(data)
        return
    if data == 11:
        # Toe stomp
        return
    if data == 12:
        # Di amon mega rotation death
        return
    if data == 13:
        # Hadoken
        return
    if data == 14:
        # Figure 8
        return
    if data == 15:
        # Jumpkick
        return
    if data == 16:
        # Failed bodyslam
        return
    if data == 17:
        # Fists of fury
        return
    if data == 18:
        return
    if data == 19:
        roll_to_hit(ch, vict, ["jab", "combo", 6, 8])
        roll_to_hit(ch, vict, ["jab", "combo", 6, 8])
        roll_to_hit(ch, vict, ["jab", "combo", 6, 8])
        roll_to_hit(ch, vict, ["uppercut", "combo", 15, 6])
        ch["ki"] = 0
        return
    if data == 20:
        return
    if data == 21:
        return
    if data == 22:
        return
    if data == 23:
        return
    if data == 24:
        return
    if data == 25:
        return
    if data == 26:
        return
    if data == 27:
        return
    if data == 28:
        return
    if data == 29:
        return
    if data == 30:
        return


# dmg( Damage ) function for calculating damage and checking for death
def dmg(ch, vict, type):
    # Going to be calculating different user init attack damage in here.
    # Combo attacks like maiden masher will have to be added
    # into a separate function that calls dmg() multiple times.
    damage_dice = ch["damage"][0]
    damage_sides = ch["damage"][1]
    damage_resistance = ch["dr"]
    extra = None
    damage = 0

    if type == "kick":
        # Calculate the damage of the kick
        # weapon damage *2, weapon damage * 4 + legs * 15
        damage = dice_roll(damage_dice, damage_sides)
        if ch["ch_class"] == "inward_fist":
            damage += 4 + ch["legs"] * 15

    if type == "auto":
        damage = dice_roll(damage_dice, damage_sides)

    # This statement contains all the fist-specific logic
    if ch["ch_class"] == "inward_fist":
        ki = ch["ki"]
        ki_value = 0
        moves = ["shinkick", "jab", "spinkick", "knee", "elbow", "uppercut"]
        for i in moves:
            ki_value += 1
            if type == i:
                result = dice_roll(1, 100)
                max_ki = int(ch["max_ki"])
                ki = int(ch["ki"])
                if result >= 31:
                    ch["ki"] = int(ki) + int(ki_value)
                    extra = int(ki) + int(ki_value)
                    if ch["ki"] > max_ki:
                        subtractVariable = max_ki - ki
                        newKi = ki_value - subtractVariable
                        extra = newKi
                        ch["ki"] = newKi
                elif result <= 15:
                    ch["ki"] = int(ki) + int(ki_value) - 1
                    extra = int(ki) + int(ki_value) - 1
                    if ch["ki"] > max_ki:
                        subtractVariable = max_ki - ki
                        newKi = ki_value - subtractVariable
                        extra = newKi
                        ch["ki"] = newKi
                else:
                    ch["ki"] = int(ki) + int(ki_value) + 1
                    extra = int(ki) + int(ki_value) + 1
                    if ch["ki"] > max_ki:
                        subtractVariable = max_ki - ki
                        newKi = ki_value - subtractVariable
                        extra = newKi
                        ch["ki"] = newKi
                damage = dice_roll(damage_dice, damage_sides) / 2
                break

    if type[1] == "combo":
        damage = dice_roll(int(type[2]), int[type[3]])
        type = type[1]

    damage -= damage_resistance
    vict["hp"] -= damage
    add_to_queue(ch["name"], type, damage, extra)
    if vict["hp"] <= 0:
        victory(ch, vict)


def user_initialized_attack_processing(ch, vict, type):
    # This prepares abilities coming from the frontend
    # and puts them in the userinit queue
    cost = 80
    if type == "kick":
        cost = 80
    data = {
            "ch": ch,
            "vict": vict,
            "type": type,
            "speed_cost": cost
        }

    cfg.user_queue.append(data)


def user_initialized_attack_queue():
    # This function establishes how many attacks the fighter
    # can execute each round and manages the user-initiated attack queue
    speed = cfg.fighter1["ability_speed"]
    max_speed = cfg.fighter1["speed_max"]
    speed += max_speed
    if speed >= 1.5 * max_speed:
        cfg.fighter1["ability_speed"] = max_speed * 1.5
    else:
        cfg.fighter1["ability_speed"] = speed

    speed = cfg.fighter2["ability_speed"]
    max_speed = cfg.fighter2["speed_max"]
    speed += max_speed
    if speed >= 1.5 * max_speed:
        cfg.fighter2["ability_speed"] = 1.5 * max_speed

    if cfg.user_queue != []:
        while True:
            if cfg.user_queue != []:
                ch = cfg.user_queue[0]["ch"]
                vict = cfg.user_queue[0]["vict"]
                type = cfg.user_queue[0]["type"]
                speed_cost = cfg.user_queue[0]["speed_cost"]
            else:
                break

            if ch["ability_speed"] < speed_cost:
                break
            else:
                ch["ability_speed"] = ch["ability_speed"] - speed_cost
                dmg(ch, vict, type)
                cfg.user_queue.pop(0)


def miss(case, ch, method):
    # The miss() method prepares data to be passed to the frontend
    if method[0]:
        method = method[0]
    if case == "miss":
        add_to_queue(ch["name"], method, 0, "miss")
    if case == "dodge":
        add_to_queue(ch["name"], method, 0, "dodge")
    if case == "block":
        add_to_queue(ch["name"], method, 0, "block")
    if case == "parry":
        add_to_queue(ch["name"], method, 0, "parry")


def auto_atk(ch, vict):
    # Auto attacks are executed every round regardless of what the user does.
    spd = ch["speed"]
    aps = spd // 40
    ch["speed"] = spd % 40
    for attacks in range(0, aps):
        roll_to_hit(ch, vict, "auto")


def victory(ch, vict):
    # A function that is invoked when a player reaches 0 hp,
    # signalling the frontend to display a victory message
    # and providing exp to the user character
    vict["is_dead"] = True
    victor = mongo.db.characters.find_one({"name": ch["name"]})
    if victor is None:
        victor = cfg.fighter2["name"]
        loser = {"name": vict["name"]}
        ratio = vict["winloss"]
        ratio[1] += 1
        submit = {"winloss": ratio}
        mongo.db.characters.update_one(loser, {"$set": submit})
    else:
        reward = 100000
        experience = int(victor["current_exp"])
        ratio = victor["winloss"]
        updatefilter = {"name": victor["name"]}
        ratio[0] += 1
        submit = {
            "current_exp": experience + reward,
            "winloss": ratio
            }
        mongo.db.characters.update_one(updatefilter, {"$set": submit})
    add_to_queue(ch["name"], "victor", 0, 100000)


def turn_timer(player1, player2):
    # A timer that activates regeneration.
    # This was intended to cover a lot more
    # ground but the project is cancelled.
    tick(player1, player2)


def turn_queue(player1, player2):
    # The turn queue that is launched every 10 queries,
    # aka 5 seconds. It launches the autoattacks and regeneration tics.
    if player1["is_dead"] is False and player2["is_dead"] is False:
        auto_atk(player1, player2)
        auto_atk(player2, player1)
        turn_timer(player1, player2)


def tick(player1, player2):
    # Regeneration ticks
    player1["speed"] += player1["speed_max"]
    player2["speed"] += player2["speed_max"]


def dice_roll(dice, sides):
    # A simple dice roll function
    rolls = []
    result = 0
    for i in range(0, dice):
        n = random.randint(0, sides)
        rolls.append(n)
    for x in rolls:
        result += x
    return result


def add_to_queue(name, method, dmg, extra):
    # A function used to add simple commands to the queue
    data = {
        "name": name,
        "method": method,
        "damage": dmg,
        "extra": extra
    }
    cfg.queue.append(data)


# Functions that app.py uses to prepare data for the above fight logic #####
def character_dump(username):
    """ Package character list into a JSON with only relevant info """
    cursor = mongo.db.characters.find(
        {"owner": username}, projection={
            "name": 1, "chclass": 1, "max_ki": 1})
    return json.dumps(
        list(cursor), cls=MongoJsonEncoder)


def prepare_character(chname, chusername):
    """ Prepare a character to be used in the combat module. """
    name = mongo.db.characters.find_one({"name": chname})
    if name["owner"] == chusername:
        chclass = name["chclass"]
        stats = {
            "name": name["name"],
            "ch_class": chclass,
            "hp": name["max_hp"],
            "max_hp": name["max_hp"],
            "ac": name["ac"],
            "hitroll": name["hitroll"],
            "dodge": name["dodge"],
            "block": name["block"] + (name["arms"] / 10),
            "parry": name["parry"],
            "speed": name["speed_max"],
            "ability_speed": name["speed_max"],
            "speed_max": name["speed_max"],
            "damage": [name["damage"][0],
                       name["damage"][1] + math.floor((name["hands"] / 5))],
            "dr": name["torso"] / 10,
            "is_dead": False,
            "abilities": name["abilities"]
        }
        if chclass == "inward_fist":
            stats["torso"] = name["torso"]
            stats["hands"] = name["hands"]
            stats["arms"] = name["arms"]
            stats["legs"] = name["legs"]
            stats["discipline"] = name["discipline"]
            stats["ki"] = name["max_ki"]
            stats["max_ki"] = name["max_ki"]
        return stats
    else:
        return False


def prepare_opponent():
    """ Prepare a generic character to be used in the combat module """
    stats = {
        "name": "Meanie",
        "ch_class": None,
        "hp": 1000,
        "max_hp": 1000,
        "ac": 30,
        "hitroll": [5, 20],
        "dodge": 20,
        "block": 10,
        "parry": 0,
        "speed": 100,
        "ability_speed": 100,
        "speed_max": 100,
        "damage": [2, 40],
        "dr": 0,
        "is_dead": False,
        "abilities": {}
    }
    return stats


# SocketIO emit event handlers ###
@socket_.on('character', namespace="/test")
def handle_icons(data):
    """ Handle requests to change icons """
    if data == "character connected":
        print(data)
    else:
        name = {"name": data[1]}
        submit = {
            "icon": data[0]
        }
        mongo.db.characters.update_one(name, {"$set": submit})


@socket_.on('query', namespace="/test")
def handle_query(data):
    """ Handle regular queries from the frontend"""
    if data == "empty":
        cfg.timer += 1
    if cfg.timer >= 10:
        turn_queue(cfg.fighter1, cfg.fighter2)
        user_initialized_attack_queue()
        cfg.timer = 0
        cfg.round += 1

    if cfg.fighter1["is_dead"] is True or cfg.fighter2["is_dead"] is True:
        emit('query', cfg.queue, broadcast=True)
        cfg.queue = []
    elif cfg.queue == []:
        emit(
            'query', "empty", broadcast=True)
    else:
        emit(
            'query', cfg.queue, broadcast=True)
        cfg.queue = []

    if data == "combo":
        combo_calculator(cfg.fighter1, cfg.fighter2, cfg.fighter1["ki"])

    if data != "empty":
        user_initialized_attack_processing(cfg.fighter1, cfg.fighter2, data)


@socket_.on('message', namespace="/test")
def handle_message(data):
    """ Handle character list request from char-select"""
    print(session["user"].upper() + " is connected.")
    if data == "requestcharacterlist":
        lookup = character_dump(session["user"])
        emit(
            'response', lookup, broadcast=True)


@socket_.on('chardata', namespace="/test")
def chardata(data):
    """ Prepare fighter data for fight instance """
    cfg.fighter1 = prepare_character(data, session["user"])
    cfg.fighter2 = prepare_opponent()
    print(data + " is prepared")
    emit(
        'character', "prepared", broadcast=True)


@socket_.on('playdata', namespace="/test")
def playdata(data):
    """ Handle requests for specific data """
    if data == "play init":
        print("play init")
        players = [
            {
                "name": cfg.fighter1["name"],
                "max_hp": cfg.fighter1["max_hp"],
                "ch_class": cfg.fighter1["ch_class"],
                "abilities": cfg.fighter1["abilities"]
            },
            {
                "name": cfg.fighter2["name"],
                "max_hp": cfg.fighter2["max_hp"],
                "ch_class": cfg.fighter2["ch_class"],
                "abilities": cfg.fighter2["abilities"]
            }
        ]
        if cfg.fighter1["ch_class"] == "inward_fist":
            players[0]["max_ki"] = cfg.fighter1["max_ki"]
        if cfg.fighter2["ch_class"] == "inward_fist":
            players[1]["max_ki"] = cfg.fighter1["max_ki"]
        emit('query', players, broadcast=True)


@socket_.on('queue', namespace="/test")
def handle_queue(data):
    print(data)


#            App routes                 ####
# This is where app routes for html pages###
# and sockets will be located           ####


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
    characters = list(mongo.db.characters.find().sort("spent_exp", -1))
    return render_template("leaderboard.html", characters=characters)


@socket_.on('leaderboard', namespace="/test")
def handle_leaderboard(data):
    """ Handle redirects to character page from the leaderboard """
    charactername = data.lower()
    emit('redirect', url_for('character', charactername=charactername))


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
    """POST to DB stuff"""
    if request.method == "POST":
        form_name = request.form['form-name']
        """Create character modal form"""
        if form_name == "create-character":
            existing_char = mongo.db.characters.find_one(
                {"name": request.form.get("name").lower()}
            )

            if existing_char:
                flash(
                    "Character name taken, try again with a different name")
                return redirect(
                        url_for("profile", username=session["user"]))

            new_char = {
                "name": request.form.get("name").lower(),
                "chclass": request.form.get("class"),
                "current_exp": 99999999,
                "spent_exp": 0,
                "max_hp": 1000,
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
                "winloss": [0, 0],
                "abilities": {"kick": "A"},
            }
            if request.form.get("class") == "inward_fist":
                new_char["icon"] = "../static/images/portrait-6.png"
                new_char["hands"] = 0
                new_char["legs"] = 0
                new_char["torso"] = 0
                new_char["arms"] = 0
                new_char["discipline"] = 0
                new_char["max_ki"] = 0
                new_char["abilities"]["shinkick"] = "ONE"
                new_char["abilities"]["jab"] = "TWO"
                new_char["abilities"]["spinkick"] = "THREE"
                new_char["abilities"]["knee"] = "FOUR"
                new_char["abilities"]["elbow"] = "FIVE"
                new_char["abilities"]["uppercut"] = "SIX"
                new_char["abilities"]["combo"] = "S"
            mongo.db.characters.insert_one(new_char)
            flash("Character Created")
            return redirect(url_for("profile", username=session["user"]))

        if form_name == "delete-account":
            """ Delete a user account """
            user = mongo.db.users.find_one({"username": username})
            if check_password_hash(
                user["password"], request.form.get(
                    "password")) and request.form.get(
                        "username").lower() == username:
                            mongo.db.characters.delete_many(
                                {"owner": user["username"]})
                            mongo.db.users.remove(
                                {"username": user["username"]})
                            session.pop("user")
            return render_template(
                "index.html")

        if form_name == "change-password":
            """ Change a password """
            user = mongo.db.users.find_one({"username": username})
            if check_password_hash(
                    user["password"], request.form.get("password")):
                if request.form.get(
                        "new-password") == request.form.get("password2"):
                    passwordupdate = generate_password_hash(
                        request.form.get("new-password"))
                    mongo.db.users.update_one(
                        {"username": username}, {
                            "$set": {"password": passwordupdate}})
                    flash("Password updated")
                else:
                    flash("Password not updated: Fields did not match.")
            else:
                flash(
                    "Password not updated: Password entered incorrectly.")

        if form_name == "change-email":
            """ Change a user email """
            if request.form.get("email") == request.form.get("confirm-email"):
                mongo.db.user.update_one({"username": username}, {
                    "$set": {"email": request.form.get("email")}})
                flash("Email updated")
            else:
                flash("Email not updated: Fields did not match.")

    if session["user"]:
        return render_template(
            "profile.html", username=username, characters=characters)


@app.route("/character/<charactername>", methods=["GET", "POST"])
def character(charactername):
    """ The character page for each character """
    try:
        username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]
    except:
        print("no user")
    finally:
        username = False
    charactername = mongo.db.characters.find_one(
        {"name": charactername}
    )

    if request.method == "POST":
        form_name = request.form['form-name']
        bodytrain_strings = ["arms", "hands", "legs", "torso"]
        """ Following code block builds four
        statements to listen for bodytraining POSTs """
        for string in range(len(bodytrain_strings)):
            if form_name == bodytrain_strings[string]:
                if request.form.get(
                        'flask-' + bodytrain_strings[string]) != '':
                    training = int(request.form.get(
                        'flask-' + bodytrain_strings[string]))
                else:
                    break
                bodytrain = int(charactername[bodytrain_strings[string]])
                spent_experience = charactername["spent_exp"]
                experience = int(charactername["current_exp"])
                cost = calculateCost(bodytrain, training)
                updatefilter = {"name": charactername["name"]}
                if experience >= cost and training + bodytrain <= 100:
                    submit = {
                        bodytrain_strings[string]: training + bodytrain,
                        "current_exp": experience - cost,
                        "spent_exp": spent_experience + cost
                    }
                    mongo.db.characters.update_one(
                        updatefilter, {"$set": submit})
                    flash("Training complete")
                    return redirect(url_for(
                        "character", charactername=charactername['name']))
                else:
                    flash("Insufficient experience for training")
                    return redirect(url_for(
                        "character", charactername=charactername['name']))

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
                mongo.db.characters.update_one(
                    {"name": charactername["name"]}, {"$set": submit})
            else:
                flash("Insufficient experience for training")
                return redirect(url_for(
                    "character", charactername=charactername['name']))

        if form_name == "char-bio":
            submit = {
                "charbio": request.form.get('char-bio')
            }
            mongo.db.characters.update_one(
                {"name": charactername["name"]}, {"$set": submit})
            flash("Bio updated")

        if form_name == "delete":
            """ Delete a character """
            if request.form.get('delete').lower() == charactername['name']:
                mongo.db.characters.remove({"name": charactername["name"]})
                flash("Character deleted")
                return redirect(url_for("profile", username=session["user"]))
            else:
                flash("Character not deleted, check name and try again.")

    return render_template(
        "character.html", username=username, charactername=charactername)


@app.route("/index")
def index():
    """ Route for the index page """
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """ Route for the login page """
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            if check_password_hash(existing_user[
                        "password"], request.form.get("password")):
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
    """ Route for registration page """
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        if request.form.get("password") == request.form.get(
                "password_confirm"):
            register = {
                "username": request.form.get("username").lower(),
                "password": generate_password_hash(
                    request.form.get("password")),
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
    """ Route for logout """
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


def calculateCost(current, iterations):
    """ Calculate the cost of a body training """
    initialValue = current
    result = 0
    i = 0
    while i < int(iterations):
        result += math.sqrt(initialValue) * 1500
        initialValue += 1
        i += 1
    return round(result)


def disciplineCost(current):
    """ Calculate the cost of a discipline training """
    return (current + 1) * 500000


if __name__ == "__main__":
    socket_.run(app, host=os.environ.get("IP"),
                port=int(os.environ.get("PORT")))
