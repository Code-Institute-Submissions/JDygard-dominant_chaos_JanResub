import random
def dice_roll(dice, sides): # I love this
    rolls = []
    result = 0
    for i in range(0,dice):
        n = random.randint(0,sides)
        rolls.append(n)
    for x in rolls:
        result += x
    return result



"""
TO DO:
Functions for dodge block parry:
    Maybe even just one function that gathers information based on the inputs
    It should start with a 0 chance for the roll, and add the player's bonus to it.
Function for hitrolls:
    Maybe. It'll be way less verbose in the actual script if they're isolated in here.

"""
