"""
class Fist(PlayerCharacter):
    List of trained elements
        Max ki
        trained ki building attacks as an object e.g.:
        ki_attacks = {          ## This will just tell the backend what to load and with what values
            "shinkick": 3,
            "jab": 6,
            "elbow": False or maybe 0, both are falsy
        }
        body parts training levels; also a dict
        trained disciplines
"""

"""
Ki combos
    10 Ki: Quivering palm
        If the class isn't fist, it drains mana
            If it's a saiyan, it can drain a charged attack into healing
                kamehameha and masenkouha
        If it's a fist, drain some of their Ki
    11 Ki: Toe stomp
        10 dice x body
    12 Ki: Di amon mega rotation death
        1 dice x weapon damage / 2
    13 Ki: Hadoken
        body/2 dice ,  weapon damage
    14 Ki: Figure 8 defense (Kiwall?)
        NEW_FIGUREEIGHT
    15 Ki: Jumpkick
        Damage: 1300, body/2 dice, weapon damage x 2/5
    16 Ki: Failed bodyslam
        Unstance
    17 Ki: bodyslam
        Unstance victim
    18 Ki: Failed bodyslam
        Unstance both
    19 Ki: Fists of Fury
        3x jab 1x uppercut: 6dw/4, 6dw/3, 6dw/2, 15dw/2
    20 Ki: Palm thrust
        Breaks defenses
    21 Ki: 6 hit combo
        shin, jab, spin, knee, elbow, uppercut: 3dw/3, 5d2/3, 8dw/3, 10dw/3, 12dw/3, 14dw/3
    22 Ki: Hesitate
        pause
    23 Ki: Touch of death
        2500 max damage, based on victim "hit" value
    24 Ki: Touch of death self
        2500 max damage to self based on "hit"
    25: Maiden masher Failed
        No block 8 tics
    26: Maiden masher
        spin, kiflame, spin, kiflame, spin, kiflame, spin, kiflame, upper, kiflame
        12dw/2, 5dspirit, 14dw/2, 7dspirit, 17dw/2, 8dspirit, 19dw/2, 20dspirit
    27: Gadouken:
        Bullshit.
        1D hit * b/3
    28: Shinkyuu Hadoken
        kiflame x3
        22D b/2 + w/4, 22D b + w/4, 22D b + w/2
    29: Holy Fists
        Gives you some kind of weapon damage thing for your Fists
    30: Instant hell murder
        Does just a ridiculous amount of damage maybe.
        1d4,
            case 1: 10d500
            case 2: 12d500
            case 3: 14d500
            case 4: 16d500

Ki building attacks, 15% +1, 15% -1
    Shinkick
        1 ki
    jab
        2 ki
    Spinkick
        3 ki
    Knee
        4 ki
    elbow
        5 ki
    uppercut
        6 ki

Tiers of aura
    0-9, 10-19, 20-30

Move swaps

Train body parts
    Costs: 1500 * isquare(current value + 1)
    Torso
    hands
    arms
    legs

Discipline training
    truesight
    levitate
        fly
    roundhouse
    inner fire 
        Burns away impurities 
    pheonix fire 
        Increased damage and hit, reduced move
    dim-mak 
        Poison?

finished animations and grid location

spritesheet 1:
0-1: punch 1
8-9: punch 2
16-17: parry
24-25: idle animation
32-35: side kick
40-41: dodge
48-49: block
56-57: Spinkick
4-5: Knee
12-13: shinkick
20-21: - Elbow
28-29: - uppercut
0-1: - Jab maybe use punch1
36-38: Aura tier 1
44-46: aura tier 2
52-54: aura tier 3

spritesheet 2:
17: Palm
18: Toe stomp
19: lame attack
20: Hadoken
21: jumpkick
22: bodyslam
23: touch of death
24: touch of death self
25: death animation
26: kiflame
"""