# Adventure 

Welcome to the deep, dark terminal... home of the text adventure.

* Play as mage, rogue, or paladin
* Level up to learn new abilities
* Fight monsters and complete quests
* Gear up your character to get powerful
* Explore three zones and their secrets

Is that hermit really so nice?

## Zones

Trainee Valley: land of wolves and the hermit. Level up a while, do a few quests. Don't get too drunk, will you?

Fort Morning: bastion of the shop and the slime. And Captain Jorna has bigger plans in store.

Silent Forest: home to the doom panda and wily fox. Seekers here never returned alive from the skeleton cave...

## How to play

1. `pip install -r requirements.txt`
2. `python Adventure.py`
3. Choose which class to play.
4. Choose a difficulty level.

On Mac you may need to allow "Settings > Privacy > Accessibility > Terminal" for instant keypress reads.

## The thirteen elements

The journal of the gamemasters... here to give you your bearings.

<...>

	(1/13)
	Welcome to Adventure!

<...> 

	(2/13)
	Your goal is to stay alive in this uncompromising world. While you're at it, you will fight
	monsters, level up, and complete quests. Here's a quick overview of how it all works.

<...> 

	(3/13)
	REST AND SCAVENGE:
	The main two actions you'll take are to rest (recover health) and to scavenge (look for
	gold). You'll want to recover your health after fighting monsters so you aren't weak when
	the next one attacks you. You'll need gold to buy items from different shops, so save up.

<...> 

	(4/13)
	COMBAT:
	Monsters will attack you at random in different zones. When you're fighting, you can cast
	your abilities or use an item. You attack, then the monster attacks. The first to die
	concludes the fight. Defeating a monster will reward gold, experience, and possibly items.
	You can navigate to your inventory in the menu to see descriptions of items.

<...> 

	(5/13)
	LEVELS:
	As you fight monsters and gain experience, you will level up. This restores you to full
	health and gives you the option to increase a stat by a small increment. Every few levels,
	you will learn a new ability depending on your class.

<...> 

	(6/13)
	STATS:
	You have seven stats. Health is your maximum health. Armor reduces damage taken. Strength
	increases damage done. Spirit increases healing. Critical strike chance and critical strike
	damage modify the frequency and potency of critical hits. Finally, dodge increases the
	chance of fully avoiding incoming damage. Armor, strength, and spirit all operate on a
	20-point scale, which means that each 20 points of strength you get is another multiple of
	your base damage.

<...> 

	(7/13)
	GEAR:
	Quests give gear, and monsters drop it. Equipping it makes you stronger. Opening your
	inventory displays the specific stats a piece of gear has. Certain items also have procs,
	which are events that occur at random when they are equipped. For example, a weapon might
	have a proc that triggers on 5% of your attacks that deals 10 damage. There are eight types
	of gear: weapon, helmet, chest, gloves, legs, boots, ring, trinket. You can wear one piece
	of each type of gear at once.

<...> 

	(8/13)
	QUESTS:
	Questgivers are scattered across different zones and will reward you for completing certain
	objectives. Find them under the 'talk' option. Completing a quest always gives experience,
	and it often gives gold and special items as well.

<...> 

	(9/13)
	TRAVEL:
	Under the 'taxi' option in the menu, you can travel between locations. New areas may have
	more powerful monsters, so be sure to level up enough before you go.

<...> 

	(10/13)
	CLASSES:
	You choose a class when you first start the game. Each class is centered around a certain
	theme: for example, mages have mana, rogues have stealth, and paladins have holy power.
	Each class has a different set of abilities that it unlocks as it levels up.

<...> 

	(11/13)
	DIFFICULTY LEVEL:
	At the start of the game you choose to play either easy, normal, hard, expert, master, or
	torment mode. Each mode either boosts or lowers your health, strength, and armor. For
	example, hard mode cuts each by 10%. Normal mode leaves all your stats the same.

<...> 

	(12/13)
	DEATH:
	If you die with the permadeath setting as False, then you will revive and possibly get
	teleported to a safer location. If you are level 5 or higher, you will receive a summoning
	sickness debuff for health, strength, and armor that lasts 100 turns.

<...> 

	(13/13)
	SETTINGS:
	You can customize your adventure with settings in the menu tab. Auto-rest and auto-scavenge
	make your rest and scavenge actions repeat until otherwise stopped. Instant input
	eliminates the need to press <enter> after each turn. Permadeath removes the chance to
	revive when killed. Warning: if you die with permadeath set to True, your run will
	terminate.

## History

This game started in 2016 as an [app](
https://lakernewhouse_9283.trinket.io/sites/adventure) I wrote in middle school. Early in high school I rebuilt it from scratch, adding more levels, more zones, better combat mechanics, and a storyline. It takes about an hour to play through start-to-finish, and of course then there's the challenge to beat the game (read: defeat the boss in the skeleton cave) at ever higher difficulty levels. Let me know if you beat the game on torment mode -- you'll make a world first.
