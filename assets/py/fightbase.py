import math
import numbers
import charbase

aghast = charbase.PlayerCharacter()
skynet = charbase.PlayerCharacter()
char = aghast.stats
victim = skynet.stats

def rth(ch, vict, type): #Roll to hit. "type" will refer to different attacks so that this function is multipurpose
    # This will wind up having to be significantly more complex
    # because of the nature of different classes having some varies hit or damage effects.
    if type == "auto":
        hitroll = numbers.dice_roll( ch["hitroll"][0], ch["hitroll"][1] ) # Call the dice roll function
        if hitroll >= vict["AC"]:   # If it clears their armor class
            dbp(ch, vict)           # Call on the Dodge Block and Parry function
        else:                       # Otherwise
            miss("miss")               # Send it to the miss function with "hit"

def dbp(ch, vict): # dodge block parry
    dodge = vict["dodge"] # Maybe update this into a dict or pair of lists, and compare them in a loop
    dodgeroll = numbers.dice_roll( 1, 100 )
    if dodgeroll <= dodge:
        miss("dodge")
        return
    block = vict["block"]
    blockroll = numbers.dice_roll( 1, 100 )
    if blockroll <= block:
        miss("block")
        return
    parry = vict["parry"]
    parryroll = numbers.dice_roll( 1, 100 )
    if parryroll <= parry:
        miss("parry")
        return
    dmg(ch,vict)

def dmg(ch, vict):
    damage_dice = ch["damage"][0]  # Collect the number of damage dice to be rolled
    damage_sides = ch["damage"][1] # and how many facets those dice have
    damage_resistance = ch["DR"]   # Collect the damage resistance
    damage = numbers.dice_roll( damage_dice, damage_sides)    #roll damage
    damage -= damage_resistance   #subtract vict["dr"]
    vict["hp"] -= damage    #apply damage
    print(f"You hit your opponent with some force ({damage})") # this will someday refer to a function full of different descriptors for different damage amounts
    if vict["hp"] <= 0:
        victory(ch, vict)

def miss(case):
    if case == "miss":
        print("You swing for your opponent, but miss.")
    if case == "dodge":
        print("You swing for your opponent, but your attack is dodged.")
    if case == "block":
        print("You swing for your opponent, but your attack is blocked.")
    if case == "parry":
        print("You swing for your opponent, but your attack is parried.")


def auto_atk(ch, vict):
    spd = ch["speed"]
    aps = spd // 40
    ch["speed"] = spd % 40 
    for attacks in range(0, aps):
        rth(ch, vict, "auto")


def turn_queue(player1, player2):
    if player1["is_dead"] == False and player2["is_dead"] == False:
        auto_atk(player1, player2)
        auto_atk(player2, player1)

turn_queue(char, victim)
