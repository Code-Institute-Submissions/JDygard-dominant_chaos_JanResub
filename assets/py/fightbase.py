"""
Random number table (DONE)
Initiate combat
dynamic turn queue
apply affects
"""
import math
import numbers
import charbase
aghast = charbase.PlayerCharacter()
skynet = charbase.PlayerCharacter()
char = aghast.stats
victim = skynet.stats

def rth(ch, vict): #Roll to hit
    # This will wind up having to be significantly more complex
    # because of the nature of different classes having some varies hit or damage effects.
    hitroll = numbers.dice_roll( ch["hitroll"][0], ch["hitroll"][1] ) # Call the dice roll function
    if hitroll >= vict["AC"]:   # If it clears their armor class
        dbp(ch, vict)           # Call on the Dodge Block and Parry function
    else:                       # Otherwise
        miss("miss")               # Send it to the miss function with "hit"

def dbp(ch, vict): # dodge block parry
    dodge = vict["dodge"] # Maybe update this into a dict or pair of lists, and compare them in a loop
    block = vict["block"]
    parry = vict["parry"]
    dodgeroll = numbers.dice_roll( 1, 100 )
    if dodgeroll <= dodge:
        miss("dodge")
        return
    blockroll = numbers.dice_roll( 1, 100 )
    if blockroll <= block:
        miss("block")
        return
    parryroll = numbers.dice_roll( 1, 100 )
    if parryroll <= parry:
        miss("parry")
        return
    dmg(ch,vict)
    """
    Possible alternative:
    #if dodge
        #miss(dodge)
    #elif block
        #miss(block)
    #elif parry
        #miss(parry)
    #else:
        #dmg(ch, vict)
    """

def dmg(ch, vict):
    damage_dice = ch["damage"][0]  # Collect the number of damage dice to be rolled
    damage_sides = ch["damage"][1] # and how many facets those dice have
    damage_resistance = ch["DR"]   # Collect the damage resistance
    damage = numbers.dice_roll( damage_dice, damage_sides)    #roll damage
    damage -= damage_resistance   #subtract vict["dr"]
    vict["hp"] -= damage    #apply damage
    print(f"You hit your opponent with some force ({damage})")


def miss(case):
    if case == "miss":
        print("You swing for your opponent, but miss.")
    if case == "dodge":
        print("You swing for your opponent, but your attack is dodged.")
    if case == "block":
        print("You swing for your opponent, but your attack is blocked.")
    if case == "parry":
        print("You swing for your opponent, but your attack is parried.")

rth(char, victim)
            



"""


f1aps = math.floor(ch["speed"] / 50)
determine number of attacks
hit roll
dodge chance
block chance
parry chance
damage roll
damage resistance
dump to turn queue    

dodge block parry should be raw chance. It starts at 0 and is augmented by a player's abilities and state.
I should build a function to check for each one.
I should think of a better way to dig up stat lines out of the characters.
"""