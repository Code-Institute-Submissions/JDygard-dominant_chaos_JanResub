![alt text](assets/images/readme/whiteboard-flowchart.png)
# Dominant Chaos

This is a game idea Maxx and I have been kicking around since the end of Static Chaos. The core of the game will be the PvP element, with multiple classes (starting with 4 or 5), a turn-based combat system with 1-2 second ticks. Basic attacks are automated but players will be able to queue one or two more powerful abilities, stance changes and attacks every tick. The specific combat context is set in stone until it is playtested. What needs to be rebuilt is the way the player encounters the world, how players encounter each-other, how PvE content is explored, equipment and cosmetics.

## Scenes 
In traditional MUDs, the world is arranged into a huge matrix of rooms connected by directions. This will not translate to a graphical context well.

"Scenes" will replace this. An unremarkable town will be represented by a single scene. A whole short PvE adventure may be represented by 2 or 3 scenes. You can see what other players inhabit a scene with you; there are no private scenes. The only static global scenes will be major hubs, primarily cities.

### Some thoughts on scenes as a concept.
The idea of this aspect of the game is to, in order of importance:
1. Give the player a sense of a vast, interconnected world
2. Give the player a sense that their choices impact their player
2. Give the player a sense of exploration
3. Give the player a sense of opportunity
4. Give the player a sense of danger

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

## The front end
![alt text](assets/images/readme/color-scheme.png)

### Front page:
Typical splash page. 
- Header, navbar
- hero image with small blurb and "start playing".
- Scroll down for a more elaborated version of the small blurb in the hero

### Play page
- Canvas with whatever graphics I can scrounge. 
- Mutable control scheme below.

### Character page
- Contains all training and upgrades for the character
- Contains all control scheme customization
- Maybe has a small canvas that shows the character and highlights parts when hovering over elements

### About page
- Info about meeeeeeeee

### Library page
- Contains learning materials pertinent to playing the game, and maybe information about coming updates and additions.

## Deployment plans? Maybe?

Load into amazon s3 bucket.
Use amazon gamelift for combat server.

## dump to turn queue    

TURN QUEUE
Needs to be set up such that there is a "user" character and a victim.
The messaging needs to be split up so that this can be used once I figure out how to do multiplayer.
The timer will be working for the server as it is.
So the timer doesn't work in terms of ch and vict, it works in terms of individual players and runs both of their combat code

There should be a specific function to deduct HP and check for death at
the same time that is always referenced for damage

Add an argument for attack type so that the RTH can be used for user-initiated attacks.
This would let me build in conditionals for different attack types having different hit chances and damage rolls


Alright, I know how we will do the modular combat system.
Every discrete portion of the combat system will be housed in classes in a big pyramid, with the basic system on top. Every subsequent breakdown will have the methods we want for that fight, i.e. in fist v saiyan it would gather the basic system, the fist system, and the fist v saiyan system. This last part may not be necessary because the statements involved with fist v saiyan might have to be integrated.
The possibility of building separate systems into the third tier of subclass would mean a lot of organization.

## We'll break it down like this
Everything between the bars is kind of deprecated.
First tier will work as originally intended, containing the core autoattack and combat queue system.
Second tier will consist of subclasses with chclass specific code.
Third tier will be mixins and decorators for augmenting the code with matchup-specific modifiers.

***
first tier is fight logic
second tier is class logic
third tier is specific fight logic

### Bottom-loaded system
1. 2nd tier logic would be limited to very general stuff that doesn't affect other classes
2. 3rd tier logic would contain a version of every matchup specific logic, even if the class isn't involved, to keep from loading multiple versions of the same thing

### Middle-loaded system
1. 2nd tier logic would be primary. Conditional trees would be more complex but more centralized. Repetitive code would be limited.
2. 3rd tier logic would be very specific and limited. Some of these classes would be empty, especially at the beginning.

### Limited tier system
1. Logic would be based on composites and mixins with the basic logic as the super.
2. I.E: The fist class would inherit the fight class, and then mixin the specific code for a saiyan fight.

## Training and the front-end
1. We will keep the code light by keeping all the combat abilities separate from each character. The chclass and a chsheet itself will only carry a list of what items to load into it on generation.
2. So what will actually happen when the user is training in the front-end, is that they are modifying the list of elements on their loadout in the database. When loading a combat instance, the list is read and the associated elements are added. This limits the ability of malicious users to submit unauthorized commands, keeps instance code lighter, and keeps database information load lighter.
***

# Some code notes to remember:
## Subclassing
class JobListing():
    """
    Creates an instance of JobListing
    """
    def __init__(self, job_title, department):
        self.job_title = job_title
        self.department = department
    
    def description(self):
        return f"Job opening for {self.job_title} in {self.department} department"

- class SalesManager(JobListing): # Define the new class
    - def __init__(self, salary): # Define the initialization procedures for the class
        - JobListing.__init__(self, "Sales Manager", "Sales") # Call the __init__ method from the parent and define that stuff
        - self.salary = salary # Define the new salary argument from salesmanager class

## Unpacking a tuple

        c, d = a # Unpacks the tuple a into variables c and d