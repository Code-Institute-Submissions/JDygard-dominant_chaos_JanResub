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
