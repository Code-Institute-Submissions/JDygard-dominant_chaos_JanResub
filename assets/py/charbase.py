class PlayerCharacter:
    hp = 100
    max_hp = 100
    energy = 100
    ac = 30
    hitroll = [5, 20]
    dodge = 20
    block = 10
    parry = 0
    speed = 100
    speed_max = 100
    damage = [2, 40]
    dr = 0
    is_dead = False

class Aghast(PlayerCharacter):
    name = "Aghast"

class Skynet(PlayerCharacter):
    name = "Skynet"
 