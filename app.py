import os                       # To access the operating system
import static.py.cfg as cfg     # A module with useful variables
from re import M # os module for accessing the os on the machine running flask
from flask import (Flask, render_template, make_response,  #Importing Flask and the ability to render templates
    redirect, request, session, url_for, flash) # Importing the ability to redirect users to other templates, request form data, use session cookies, standin urls with python and jinja, and flash information
from bson.objectid import ObjectId #Importing the ability to reference MongoDB object ids
from flask_pymongo import PyMongo   # Importing a module to use python with MongoDB
from werkzeug.security import generate_password_hash, check_password_hash   # Importing the ability to hash passwords and check hashed passwords
import datetime # For... you know. The date... and the time.
from flask_socketio import SocketIO, emit, disconnect
from threading import Lock
import random                   # Used for the dice_roll() method
import time
import math                     # Used to calculate damage, experience, block values and more
import json                     # Used to format data sent to the frontend
if os.path.exists("env.py"):    # If statement so that the program works without env.py present
    import env                  # import secret information


app = Flask(__name__)           # setting flask to the standard __name__
app.config.from_object(__name__)

async_mode = None               # Async mode is a bit complex for a beginner
thread = None                   # No threading
thread_lock = Lock()            # With locked threads

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
def roll_to_hit(ch, vict, type): 
    # because of the nature of different classes having some varies hit or damage effects.
    if ch["is_dead"] != True and vict["is_dead"] != True:
        if type == "auto":
            hitroll = dice_roll( ch["hitroll"][0], ch["hitroll"][1] ) # Call the dice roll function
            if hitroll >= vict["ac"]:   # If it clears their armor class
                dodge_block_parry(ch, vict, type)           # Call on the Dodge Block and Parry function
            else:                       # Otherwise
                miss("miss", ch, type)               # Send it to the miss function with "hit"


# After a hit registers, run the dbp function, short for dodge, block and parry
def dodge_block_parry(ch, vict, type): # dodge block parry
    # Check dodge roll
    dodge = vict["dodge"]               # Gather the victim's dodge value
    dodgeroll = dice_roll( 1, 100 )     # Roll the dice
    if dodgeroll <= dodge:              # Check if it hits
        miss("dodge", ch, type)         # And send them to the miss() method if it misses
        return

    # Check block roll
    block = vict["block"]               # Gather the victim's block value
    blockroll = dice_roll( 1, 100 )     # Roll the dice
    if blockroll <= block:              # Check if it hits
        miss("block", ch, type)         # If it doesn't, send them to the miss() method
        return

    # Check parry roll
    parry = vict["parry"]               # Gather the victim's parry value
    parryroll = dice_roll( 1, 100 )     # Roll the dice
    if parryroll <= parry:              # If it misses
        miss("parry", ch, type)         # send them to the miss() method
        return

    # If damage isn't prevented, calculate damage
    dmg(ch, vict, type)                 # If they don't dodge, block or parry, go calculate damage


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
    # Combo attacks like maiden masher will have to be added into a separate function that calls dmg() multiple times.
    damage_dice = ch["damage"][0]  # Collect the number of damage dice to be rolled
    damage_sides = ch["damage"][1] # and how many facets those dice have
    damage_resistance = ch["dr"]  # Collect the damage resistance
    extra = None
    damage = 0

    if type == "kick":
        #Calculate the damage of the kick
        # weapon damage *2, weapon damage * 4 + legs * 15
        damage = dice_roll( damage_dice, damage_sides )
        if ch["ch_class"] == "inward_fist":
            damage += 4 + ch["legs"] * 15
    

    if type == "auto":
        damage = dice_roll( damage_dice, damage_sides )    #roll damage
    
    if ch["ch_class"] == "inward_fist": # If it's a fist
        ki = ch["ki"]   # Establish current ki cost
        ki_value = 0    # Establish an iterable that also is used in calculating the value of the relevant move
        moves = ["shinkick", "jab", "spinkick", "knee", "elbow", "uppercut"] # An array of the ki-gaining moves this function is testing for
        for i in moves: # Go through the array
            ki_value += 1 # Iterate the iterable
            if type == i:   # If the command being processed is one of those being targeted, calculate it
                result = dice_roll( 1, 100) # Gather a 1-100 dice roll
                max_ki = int(ch["max_ki"])
                ki = int(ch["ki"])               # Establish the character's current ki
                if result >= 31:            # If the result is not going to be modified
                    ch["ki"] = int(ki) + int(ki_value) # Give them the advertised ki amount
                    extra = int(ki) + int(ki_value)
                    if ch["ki"] > max_ki:
                        subtractVariable = max_ki - ki
                        newKi = ki_value - subtractVariable
                        extra = newKi
                        ch["ki"] = newKi
                elif result <= 15:          # Test for 1-15
                    ch["ki"] = int(ki) + int(ki_value) - 1    # If it's there, then one less ki is gained
                    extra = int(ki) + int(ki_value) -1
                    if ch["ki"] > max_ki:
                        subtractVariable = max_ki - ki
                        newKi = ki_value - subtractVariable
                        extra = newKi
                        ch["ki"] = newKi
                else:
                    ch["ki"] = int(ki) + int(ki_value) + 1    # If it's in the 16-30 range, they get a bonus ki
                    extra = int(ki) + int(ki_value) + 1
                    if ch["ki"] > max_ki:
                        subtractVariable = max_ki - ki
                        newKi = ki_value - subtractVariable
                        extra = newKi
                        ch["ki"] = newKi
                damage = dice_roll( damage_dice, damage_sides ) / 2 # Roll the paltry damage these moves inflict
                break # Stop the for loop for efficiency, since there can't be two positive results
    
    print(type)
    if type[1] == "combo":
        damage = dice_roll(int(type[2]), int[type[3]])
        type = type[1]

    damage -= damage_resistance   #subtract vict["dr"]
    vict["hp"] -= damage    #apply damage
    add_to_queue(ch["name"], type, damage, extra)
    if vict["hp"] <= 0:
        victory(ch, vict)


def user_initialized_attack_processing(ch, vict, type):
    #This prepares abilities coming from the frontend and puts them in the userinit queue
    cost = 80 # Standard speed cost
    if type == "kick":
        cost = 80 # Variable speed cost for kick
    data = { # Prepare unit data for processing
            "ch": ch, # The character initiating
            "vict": vict, # The victim
            "type": type, # Type of attack
            "speed_cost": cost # And the cost
        }
    
    cfg.user_queue.append(data) # Put the command in the queue


def user_initialized_attack_queue():
    speed = cfg.fighter1["ability_speed"] #Gather attacker speed
    max_speed = cfg.fighter1["speed_max"] #Gather attacker maximum speed
    speed += max_speed #Regenerate max ki
    if speed >= 1.5 * max_speed: #If ki is more than 150% max
        cfg.fighter1["ability_speed"] = max_speed * 1.5 #Set it to 150% max
    else:                                               #Otherwise
        cfg.fighter1["ability_speed"] = speed           #Just leave it alone

    speed = cfg.fighter2["ability_speed"]               # And do the same with fighter2
    max_speed = cfg.fighter2["speed_max"]
    speed += max_speed
    if speed >= 1.5 * max_speed:
        cfg.fighter2["ability_speed"] = 1.5 * max_speed
    
    if cfg.user_queue != []: # If the user queue isn't empty
        while True:         # Start going through the queue
            if cfg.user_queue != []: # Check every iteration that it isn't empty
                ch = cfg.user_queue[0]["ch"] # And package the values into something the dmg() function can parse
                vict = cfg.user_queue[0]["vict"]
                type = cfg.user_queue[0]["type"]
                speed_cost = cfg.user_queue[0]["speed_cost"]
            else:
                break

            if ch["ability_speed"] < speed_cost: # If the player runs out of speed, stop the loop
                break
            else:   # Otherwise send it to the dmg() function and pop the item off the queue
                ch["ability_speed"] = ch["ability_speed"] - speed_cost
                dmg(ch, vict, type)
                cfg.user_queue.pop(0)



# The miss() method prepares data to be passed to the frontend
def miss(case, ch, method):
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


# Auto attacks are executed every round regardless of what the user does.
def auto_atk(ch, vict):
    spd = ch["speed"]       # The number of attacks is based on the speed stat
    aps = spd // 40         # Calculate the number of attacks
    ch["speed"] = spd % 40  # Retain whatever speed was not used
    for attacks in range(0, aps):       #Resolve the number of attacks
        roll_to_hit(ch, vict, "auto")   # at the roll_to_hit() method


# A function that is invoked when a player reaches 0 hp, signalling the frontend to display a victory message and providing exp to the user character
def victory(ch, vict):
    vict["is_dead"] = True
    victor = mongo.db.characters.find_one({"name": ch["name"]}) # Look up the character who won
    if victor == None:  # If they don't exist in the database then it's the enemy
        victor = cfg.fighter2["name"] # Put the name of the opponent in the victory variable
        loser = {"name": vict["name"]}
        ratio = vict["winloss"]
        ratio[1] += 1
        print(ratio)
        submit = {"winloss": ratio}
        mongo.db.characters.update_one(loser, {"$set": submit})
    else:
        reward = 100000
        experience = int(victor["current_exp"])
        ratio = victor["winloss"]
        updatefilter = {"name": victor["name"]}
        ratio[0] += 1
        print(ratio)
        submit = {
            "current_exp": experience + reward,
            "winloss": ratio
            }
        mongo.db.characters.update_one(updatefilter, {"$set": submit})
    add_to_queue(ch["name"], "victor", 0, 100000)


# A timer that activates regeneration. This was intended to cover a lot more ground but the project is cancelled.
def turn_timer(player1, player2):
    tick(player1, player2)


# The turn queue that is launched every 10 queries, aka 5 seconds. It launches the autoattacks and regeneration tics.
def turn_queue(player1, player2):
    if player1["is_dead"] == False and player2["is_dead"] == False: # Gotta make sure they're not dead
        auto_atk(player1, player2)
        auto_atk(player2, player1)
        turn_timer(player1, player2)


# Regeneration ticks
def tick(player1, player2):
    player1["speed"] += player1["speed_max"]
    player2["speed"] += player2["speed_max"]


# A simple dice roll function
def dice_roll(dice, sides):
    rolls = []
    result = 0
    for i in range(0,dice):
        n = random.randint(0,sides)
        rolls.append(n)
    for x in rolls:
        result += x
    return result


# A function used to add simple commands to the queue
def add_to_queue(name, method, dmg, extra):
    data = {
        "name": name,
        "method": method,
        "damage": dmg,
        "extra": extra
    }
    cfg.queue.append(data)


##### Functions that app.py uses to prepare data for the above fight logic #####


def character_dump(username):
    """ Package character list into a JSON with only relevant info """
    cursor = mongo.db.characters.find({"owner": username},
        projection={"name": 1, "chclass": 1, "max_ki": 1,})
    return json.dumps(list(cursor),
        cls=MongoJsonEncoder)


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
            "damage": [name["damage"][0], name["damage"][1] + math.floor((name["hands"] / 5))],
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


### SocketIO emit event handlers ###
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
    if data == "empty": # Empty queries are used by the frontend to request data and to coordinate timing
        cfg.timer += 1  # Measuring how many queries have elaapsed
    if cfg.timer >= 10: # When it gets to 10 (5ish seconds)
        turn_queue(cfg.fighter1, cfg.fighter2) # Initiate the round with the turn queue
        user_initialized_attack_queue()        # Tell the queue function to check how much the character can do with the remaining speed 
        cfg.timer = 0                           # Reset the timer
        cfg.round += 1                          # Keep track of how many rounds have elapsed

    if cfg.fighter1["is_dead"] == True or cfg.fighter2["is_dead"] == True: #If someone has died
        emit('query', cfg.queue, broadcast=True)                            # Let the frontend know
        cfg.queue = []                                                      # And empty the queue
    elif cfg.queue == []:                                                   # If there's nothing to submit,
        emit('query', "empty",                                              # Just send an empty message
            broadcast=True)
    else:                                       
        emit('query', cfg.queue,                                            # Otherwise, send the commands to be executed on the frontend
            broadcast=True)
        cfg.queue = []                                                      # and empty the queue
    
    if data == "combo":
        combo_calculator(cfg.fighter1, cfg.fighter2, cfg.fighter1["ki"])    # This is used to separate the combos from other, less complex commands

    if data != "empty":
        user_initialized_attack_processing(cfg.fighter1, cfg.fighter2, data) # This is, in a sense, some placeholder code since it only permits the user character to execute command attacks.


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
    #####     POST to DB stuff     #####
    if request.method == "POST":
        form_name = request.form['form-name']
        #####      Create character modal form      #####
        if form_name == "create-character":
            existing_char = mongo.db.characters.find_one( # Check and see if the name already exists
                {"name": request.form.get("name").lower()}
            )

            if existing_char:   # And let the user know, redirecting them back to the form
                flash("Character name taken, try again with a more differenter name")
                return redirect(
                        url_for("profile", username=session["user"]))

            new_char = { # Setting all the stats for a base character
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
            if request.form.get("class") == "inward_fist": # Tacking on all the specific stuff for a fist
                new_char["icon"] = "images/fist-icon.png"
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
        
        if form_name == "delete-account":   # Deleting a user account
            user = mongo.db.users.find_one({"username":username})
            if check_password_hash(user["password"], request.form.get("password")) and request.form.get("username").lower() == username:
                    mongo.db.characters.delete_many({"owner": user["username"]})
                    mongo.db.users.remove({"username": user["username"]})
                    session.pop("user")
        

        if form_name == "change-password":  # Changing a user password
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


        if form_name == "change-email": # Changing a user email
            if request.form.get("email") == request.form.get("confirm-email"):
                mongo.db.user.update_one({"username": username}, {"$set": {"email": request.form.get("email")}})
                flash("Email updated")
            else:
                flash("Email not updated: Fields did not match.")


    if session["user"]:
        return render_template("profile.html", username=username, characters=characters)


@app.route("/character/<charactername>", methods=["GET", "POST"])
def character(charactername):
    """ The character page for each character """
    username = mongo.db.users.find_one( # Find the user
        {"username": session["user"]})["username"]
    charactername = mongo.db.characters.find_one( # Find the selected character
        {"name": charactername}
    )

    if request.method == "POST":
        form_name = request.form['form-name'] # Get the form-name
        bodytrain_strings = ["arms", "hands", "legs", "torso"] # Setting up the strings for the following for loop
        """ Following code block builds four statements to listen for bodytraining POSTs """
        for string in range(len(bodytrain_strings)):
            if form_name == bodytrain_strings[string]:  # If it's a bodytraining form
                training = int(request.form.get('flask-' + bodytrain_strings[string]))  # Collect how much is being trained
                bodytrain = int(charactername[bodytrain_strings[string]])   # Collect the current training
                spent_experience = charactername["spent_exp"]   # Collect the current experience level
                experience = int(charactername["current_exp"])  # Collect the unspent experience
                cost = calculateCost(bodytrain, training)       # Calculate the cost of what is being trained
                updatefilter= {"name": charactername["name"]}   # Make a filter for finding items in the database
                if experience >= cost and training + bodytrain <= 100:  # If they have enough experience and this wouldn't train them any higher than the maximum (100)
                    submit = {                                          # prepare the information
                        bodytrain_strings[string]: training + bodytrain,# Using the data from above
                        "current_exp": experience - cost,               # While deducting the right amount of experience
                        "spent_exp": spent_experience + cost            # And adding to the spent experience
                    }
                    mongo.db.characters.update_one(updatefilter, {"$set": submit}) # Get the character in the db
                    flash("Training complete")                                      # Let the user know it worked
                    return redirect(url_for("character", charactername=charactername['name']))  # And send them back to the page
                else:
                    flash("Insufficient experience for training") #Otherwise tell them it didn't work and send them back
                    return redirect(url_for("character", charactername=charactername['name']))

        """ Following code block listens for discipline training POSTs """
        if form_name == "discipline":                               #If it's a discipline form
            discipline = int(charactername["discipline"])           # Collect current discipline
            cost = disciplineCost(discipline)                       # Calculate the cost
            spent_experience = int(charactername["spent_exp"])      # Collect spent exp
            experience = int(charactername["current_exp"])          # Collect current unspent exp
            if experience > cost:                                   # If they have enough exp
                submit = {                                          # Prepare some data
                    "discipline": discipline + 1,                   # Add a discipline
                    "current_exp": experience - cost,               # Subtract the cost
                    "spent_exp": spent_experience + cost            # Add the spent exp
                }
                mongo.db.characters.update_one({"name": charactername["name"]}, {"$set": submit})   # Update the DB
            else:
                flash("Insufficient experience for training")                               # Otherwise let the user know it didn't work
                return redirect(url_for("character", charactername=charactername['name']))  # And send them back to the page

            
        if form_name == "char-bio": # If they are updating their bio
            submit = {              # Prepare some data
                "charbio": request.form.get('char-bio')
            }
            mongo.db.characters.update_one({"name": charactername["name"]}, {"$set": submit}) # Submit it to the db
            flash("Bio updated")    # And let the user know it worked

        if form_name == "delete":                                           # If the user is deleting a character
            if request.form.get('delete').lower() == charactername['name']: # Get the name of the character and make sure it matches
                mongo.db.characters.remove({"name": charactername["name"]}) # Remove the character from the DB
                flash("Character deleted")                                  # Let the user know it worked
                return redirect(url_for("profile", username=session["user"])) # And take them back to the profile page to make a new one
            else:
                flash("Character not deleted, check name and try again.")   # Otherwise let them know it didn't work for some reason
 
    return render_template("character.html", username=username, charactername=charactername) # No matter what happens, we're sending them back to the character page.


@app.route("/index")
def index():
    """ Route for the index page """
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """ Route for the login page """
    if request.method == "POST":
        existing_user = mongo.db.users.find_one( # Check the username
            {"username": request.form.get("username").lower()})

        if existing_user: # If they exists, check the password
            if check_password_hash(existing_user["password"], request.form.get("password")):
                    session["user"] = request.form.get("username").lower()
                    flash("Welcome, {}".format(request.form.get("username"))) # Let the user know it worked out
                    return redirect(    #And redirect them to the profile page
                        url_for("profile", username=session["user"]))
            else:
                flash("Incorrect Username and/or Password") #Otherwise indicate failure
                return redirect(url_for("login"))   # And send them back to login page

        else:
            flash("Incorrect Username and/or Password") # Same error for other failures
            return redirect(url_for("login"))   # Redirect to login
            
    return render_template("login.html")    


@app.route("/register", methods=["POST", "GET"])
def register():
    """ Route for registration page """
    if request.method == "POST":    # If they're posting something
        existing_user = mongo.db.users.find_one(    # Get that name
            {"username": request.form.get("username").lower()})# Check if the username already exists

        if existing_user:   # If it exists
            flash("Username already exists") # Let them know
            return redirect(url_for("register")) # and redirect
        
        if request.form.get("password") == request.form.get("password_confirm"): # If the passwords match
            register = {    # Prepare some data
                "username": request.form.get("username").lower(),
                "password": generate_password_hash(request.form.get("password")),
                "email": request.form.get("email"),
                "registered_on": datetime.datetime.now(),
            }
            mongo.db.users.insert_one(register) # And put it in the DB
        else:
            flash("Password fields do not match")   # Otherwise let them know the field didn't match
            return redirect(url_for("register"))    # And send them back

        session["user"] = request.form.get("username").lower()  # Set the session user
        flash("Registration Successful")    # Let them know it worked out
        return redirect(url_for("profile", username=session["user"]))   # And redirect them to the profile page
    return render_template("register.html") # Display the registration form


@app.route("/logout")
def logout():
    """ Route for logout """
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


def calculateCost(current, iterations): # Calculate the cost of a body training
    initialValue = current
    result = 0
    i = 0
    while i < int(iterations): # This is capable of calculating any number of simultaneous trainings
        result += math.sqrt(initialValue) * 1500
        initialValue += 1
        i += 1
    return round(result)


def disciplineCost(current): # Calculate the cost of a discipline training
    return (current + 1) * 500000


if __name__ == "__main__":  # If the name is valid
    socket_.run(app, host=os.environ.get("IP"),#Setting the ip
            port=int(os.environ.get("PORT")),#setting the port #
            debug=True) #Using debug mode while developing the backend