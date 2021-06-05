![alt text](assets/images/readme/whiteboard-flowchart.png)
# Dominant Chaos

This is a game idea Maxx and I have been kicking around since the end of Static Chaos. The core of the game will be the PvP element, with multiple classes (starting with 4 or 5), a turn-based combat system with 1-2 second ticks. Basic attacks are automated but players will be able to queue one or two more powerful abilities, stance changes and attacks every tick. The specific combat context is set in stone until it is playtested. What needs to be rebuilt is the way the player encounters the world, how players encounter each-other, how PvE content is explored, equipment and cosmetics.

## Scenes 
In traditional MUDs, the world is arranged into a huge matrix of rooms connected by directions. This will not translate to a graphical context well.

"Scenes" will replace this. An unremarkable town will be represented by a single scene. A whole short PvE adventure may be represented by 2 or 3 scenes. You can see what other players inhabit a scene with you; there are no private scenes. The only static global scenes will be major hubs, primarily cities.

## Classes 
The first 5 classes are set in stone. 
Inward Fist: A martial artist who uses the ki energy of the body to drive inward strength and physical abilities.
Outward Fist: A martial artist who uses ki energy to drive outward power. Think a saiyan from DBZ.
Sorcerer: Master of schools of magic, using combinations of chanted words of power to channel their abilities.
Chi-xin Shaman: A warrior who tattoos symbols of elemental power on to their body to gain aspects of their strengths, and empower the weaving of these runes into martial magics.
Demon: A shade from another realm of reality, using their sheer will to instantiate a corporeal form, able to customize their entire body for combat, forming tentacles, blades, armor, or claws.
## PvP 
How do players meet each other? How do they interact?

- Ranked PvP could just be tournaments available in hub cities.

- "Contracts" could allow players to be hired by NPCs to participate in what would otherwise be another player's solo PvE adventure.

- Random encounters in scenes outside of hub cities could allow one player to ambush another, or allow the players to decide how to respond to another.

## Levels/Matchmaking
Players' "levels" should be represented by how much experience they have spent customizing their character, and these interactions should be hard limited to players within their own strata.

## The alignment axes 
Pretty much stolen directly from DnD. Chaos/Order, Good/Evil.
These are adjusted by how a player deals with situations in both PvE and PvP. Does the player rescue the damsel without the promise of reward? That serves good, and order. Did they break the rules to do it? Maybe a little more chaos.

We can use these axes to award unique abilities. The option to set up an ambush on the road could be limited only to sufficiently evil or chaotic characters. Some cities' guard may only protect sufficiently good or lawful characters. Pirate towns' npc muscle might attack an orderly character on sight.

Cosmetic decisions could also be governed by these axes. A good character couldn't look evil and vise versa.

## Procedural persistence and familiarity 
As said above, travel is a scene.

If a character wants to go from Midgaard to Waterdeep, they enter a travel scene. If it is their first time travelling, they need to find their way. Most often, there is a road. Once your player has used the road, it begins to become familiar. Increased familiarity opens new options (like avoiding being seen,) and reduces the chances of negative encounters.

Other scenes like landmarks, random encounters, hidden adventures, hideouts, caves etc. will be found procedurally by "taking the scenic route" as an option while travelling, explicitly exploring, while lost, etc. Procedurally discovered locations become semi-static locations that can be found by others. Finding a good adventure, good hideout, oasis or shortcut could be akin to finding an epic or legendary item in another game and become a closely guarded secret.

Locations could be upgraded by players to become protected, harder to find, etc. Perhaps sorcerers need a location to build a place of power.

## You guys really seem to have this figured out, how can I help? 
If you read this and think of anything to add, change, or remove, TELL ME. I would love ideas. Much of this was Algerothen and Conundrum riffing off of our general ideas. Just put a header on it and talk it through.

## Equipment
I've got little on gear. 
I'm tempted to say gear that impacts stats should be limited to certain classes, and choices between gear should be a choice on style of play rather than finding the most powerful version of a thing. Gear ideas would be very, very welcome.

## Class independent skills 
It was suggested that people could be trailed, it gave me the idea for primary and secondary skills.

### Primary skills
Look at these like trade skills in WoW. You get to pick one and develop it. Perhaps developing these to some arbitrary level gives access to cosmetics? I've only settled on one:
- Thief: Gives the ability to track or trail other players, and infiltrate poorly protected environments. Has impacts on PvE adventure scenes. Maybe traps, poisons.
- Crafter?: Might be cumbersome to implement, but could be an interesting addition to whatever gear system goes in.
- Pilot?: GUNDAAAAAAAAAAAAAAAM

### Secondary skills
Secondary skills will all passively increase.
- Perception: Ability to detect trailing or infiltrating thieves. Affects scene chances passively.
- Exploration: Weights chances on exploratory scenes
- Diplomacy: Weights chances in adventure scenes with appropriate elements. Maybe split it into bluff, something like sense motive, etc.



# I'm working on it, lol


dump to turn queue    

TURN QUEUE
Needs to be set up such that there is a "user" character and a victim.
The messaging needs to be split up so that this can be used once I figure out how to do multiplayer.
The timer will be working for the server as it is.
So the timer doesn't work in terms of ch and vict, it works in terms of individual players and runs both of their combat code

There should be a specific function to deduct HP and check for death at
the same time that is always referenced for damage

Add an argument for attack type so that the RTH can be used for user-initiated attacks.
This would let me build in conditionals for different attack types having different hit chances and damage rolls

"""