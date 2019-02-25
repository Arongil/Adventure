import globals
import output
import frequencyList as fList
import interactions.fight as fight
import interactions.loot as loot
import interactions.shop as shop
import interactions.shrine as shrine
import creatures.monster as monster
import creatures.gear as gear
import items.potions as potions
import location
import actions
import ability
import effect
import item

'''
Morning Fields is the starting zone. It has three locations: Trainee Valley, The Silent Forest, and Fort Morning. The connections are as follows.
TRAINEE VALLEY ---> THE SILENT FOREST, FORT MORNING
THE SILENT FOREST ---> TRAINEE VALLEY
FORT MORNING ---> TRAINEE VALLEY
'''

# START OF TRAINEE VALLEY

class Wolf(monster.Monster):

    def __init__(self):
        monster.Monster.__init__(self, "wolf", 40, loot.Loot("the wolf", 2, 20, [
                [item.Nothing(), 0.7],
                [item.Item("lean wolf flank", "its owner must not have had enough to eat", 2, 9), 0.25],
                [gear.Gloves("torn wolfhide gloves", "the coarse fabric seems vaguely glovelike", 8, 26, lambda creature: creature.stats.armor.add(2), lambda creature: creature.stats.armor.add(-2)), 0.05]
            ]), [
            # [name, cooldown, caster (always self), cast logic (takes ablty, which means ability but can't be confused with the module, and target)], probability
            [ability.Ability("bite", 0, self, lambda ablty, target: ability.damage(ablty, target, 2, 6)), 0.5],
            [ability.Ability("snap", 0, self, lambda ablty, target: ability.damage(ablty, target, 4, 8)), 0.3],
            [ability.Ability("lick wounds", 2, self, lambda ablty, target: ability.heal(ablty, target, 4, 10)), 0.2]
        ])

class DrunkenTrainee(monster.Monster):

    def __init__(self):
        monster.Monster.__init__(self, "drunken trainee", 60, loot.Loot("the drunken trainee", 5, 30, [
                [item.Nothing(), 0.7],
                [item.UsableItem("cheap whiskey", "it's nearly empty", 5, 19, lambda target: target.addEffect( effect.DamageOverTime("intoxication", 3, 1, 2) )), 0.3]
            ]), [
            # [name, cooldown, caster (always self), cast logic (takes ablty, which means ability but can't be confused with the module, and target)], probability
            [ability.Ability("charge", 0, self, lambda ablty, target: ability.damage(ablty, target, 6, 10)), 0.5],
            [ability.Ability("stumble", 0, self, lambda ablty, target: self.stumble()), 0.3],
            [ability.Ability("vomit", 4, self, lambda ablty, target: target.addEffect( effect.DamageOverTime("intoxicated vomit", 2, 3, 5) )), 0.2]
        ])

    def stumble(self):
        output.say("The drunken trainee stumbles and attempts to regain balance.")

def getTraineeValley():
    def getMonster():
        monsters = fList.FrequencyList([
            [Wolf(), 0.8],
            [DrunkenTrainee(), 0.2]
        ])
        return monsters.getOption()
    def enter():
        output.proclaim("Trainee Valley: Sparse trees occupy rolling expanses of lush grass. Fort Morning is barely visible in the distant north, while the Silent Forest looms to the east.")
    def exit():
        output.proclaim("You have left Trainee Valley.")

    traineeValleyActions = [
        actions.RestHeal(globals.player),
        actions.Scavenge(globals.player, [
            [actions.ScavengeGold(globals.player, 0, 2), 0.98],
            # health, armor, strength, spirit, criticalChance, criticalStrike
            [shrine.StatShrine([20, 10, 10, 10, 0.1, 1], 50), 0.02]
        ])
    ]
    traineeValleyInteractions = [
        [actions.Nothing(), 0.8],
        [fight.Fight(getMonster), 0.2]
    ]
    return location.Location("Trainee Valley", enter, exit, traineeValleyActions, traineeValleyInteractions)

# END OF TRAINEE VALLEY

# START OF SILENT FOREST

class ProwlingFox(monster.Monster):

    def __init__(self):
        monster.Monster.__init__(self, "prowling fox", 60, loot.Loot("the prowling fox", 5, 50, [
                [item.Nothing(), 0.9],
                [item.Item("bushy tail", "a muddled red to blend in with the trees", 4, 19), 0.1]
            ]), [
            # [name, cooldown, caster (always self), cast logic (takes ablty, which means ability but can't be confused with the module, and target)], probability
            [ability.Ability("pounce", 999, self, lambda ablty, target: ability.damage(ablty, target, 14, 20)), 999],
            [ability.Ability("claw", 0, self, lambda ablty, target: ability.damage(ablty, target, 6, 8)), 0.8],
            [ability.Ability("tense", 2, self, lambda ablty, target: ablty.caster.addEffect( effect.StrengthBuff("tense", 1, 0.5) )), 0.2]
        ])

class Owl(monster.Monster):

    def __init__(self):
        monster.Monster.__init__(self, "owl", 30, loot.Loot("the owl", 2, 40, [
                [item.Nothing(), 0.8],
                [item.Item("feather", "", 1, 4), 0.2]
            ]), [
            # [name, cooldown, caster (always self), cast logic (takes ablty, which means ability but can't be confused with the module, and target)], probability
            [ability.Ability("peck", 0, self, lambda ablty, target: ability.damage(ablty, target, 4, 8)), 0.6],
            [ability.Ability("gouge", 0, self, lambda ablty, target: ability.damage(ablty, target, 8, 12)), 0.4]
        ])

class SorcererOutcast(monster.Monster):

    def __init__(self):
        monster.Monster.__init__(self, "sorcerer outcast", 50, loot.Loot("the sorcerer outcast", 8, 80, [
                [item.Nothing(), 0.4],
                [item.UsableItem("mysterious green brew", "it could be poison, it could be eternal life, it could be stool softener", 9, 49, lambda target: target.addEffect( effect.SpiritBuff("heightened spirits", 20, 2) )), 0.2],
                [item.Item("cryptic spellbook", "the writing looks hasty and is in an elvish tongue", 30, 99), 0.2],
                [gear.Helmet("pointy black hat", "several patches mottle the hat, including a long seam directly above the brim", 19, 49, lambda creature: creature.stats.criticalChance.add(0.1), lambda creature: creature.stats.criticalChance.add(-0.1)), 0.2]
            ]), [
            # [name, cooldown, caster (always self), cast logic (takes ablty, which means ability but can't be confused with the module, and target)], probability
            [ability.Ability("frostbolt", 0, self, lambda ablty, target: ability.damage(ablty, target, 8, 14)), 0.5],
            [ability.Ability("frigid wind", 2, self, lambda ablty, target: target.addEffect( effect.StrengthBuff("frigid wind", 2, -0.5) )), 0.3],
            [ability.Ability("icy shield", 4, self, lambda ablty, target: ablty.caster.addEffect( effect.ArmorBuff("icy shield", 3, 1) )), 0.2]
        ], armor=4)

def getTheSilentForest():
    def getMonster():
        monsters = fList.FrequencyList([
            [ProwlingFox(), 0.4],
            [Owl(), 0.4],
            [SorcererOutcast(), 0.2]
        ])
        return monsters.getOption()
    def enter():
        output.proclaim("The Silent Forest: Great oaks sway endlessly to the southerly winds. The air's oppression is lifted but briefly at the occasional rustle. Trees obscure the view to Trainee Valley.")
    def exit():
        output.proclaim("You have left the Silent Forest.")

    theSilentForestActions = [
        actions.RestHeal(globals.player),
        actions.Scavenge(globals.player, [
            [actions.ScavengeGold(globals.player, 0, 4), 0.99],
            # health, armor, strength, spirit, criticalChance, criticalStrike
            [shrine.StatShrine([20, 10, 10, 10, 0.1, 1], 50), 0.01]
        ])
    ]
    theSilentForestInteractions = [
        [actions.Nothing(), 0.8],
        [fight.Fight(getMonster), 0.2]
    ]
    return location.Location("The Silent Forest", enter, exit, theSilentForestActions, theSilentForestInteractions)

# END OF SILENT FOREST

# START OF SKELETON CAVE

class SkeletonWarrior(monster.Monster):

    def __init__(self):
        monster.Monster.__init__(self, "unholy ooze", 60, loot.Loot("the unholy ooze", 2, 40, [
                [item.Nothing(), 0.8],
                [gear.Ring("unholy band", "an irregular loop formed from the hard core of an ancient ooze", 24, 99, lambda target: target.stats.criticalStrike.add(0.5), lambda target: target.stats.criticalStrike.add(-0.5)), 0.2]
            ]), [
            # [name, cooldown, caster (always self), cast logic (takes ablty, which means ability but can't be confused with the module, and target)], probability
            [ability.Ability("spit slime", 0, self, lambda ablty, target: ability.damage(ablty, target, 6, 10)), 0.7],
            [ability.Ability("jellification", 3, self, lambda ablty, target: ablty.caster.addEffect( effect.ArmorBuffAdd("jellification", 2, 40) )), 0.3]
        ])
        self.size = 3

    def attack(self, target):
        if self.health > 0:
            self.abilities.getOption(lambda ability: not ability.onCooldown()).activate(target)
        elif self.size > 1:
            self.size -= 1
            self.stats.health.value /= 2
            self.health = self.stats.health.getValue()
            output.proclaim("The unholy ooze sheds a layer of goo and rises again!")

class SkeletonArcher(monster.Monster):

    def __init__(self):
        monster.Monster.__init__(self, "unholy ooze", 60, loot.Loot("the unholy ooze", 2, 40, [
                [item.Nothing(), 0.8],
                [gear.Ring("unholy band", "an irregular loop formed from the hard core of an ancient ooze", 24, 99, lambda target: target.stats.criticalStrike.add(0.5), lambda target: target.stats.criticalStrike.add(-0.5)), 0.2]
            ]), [
            # [name, cooldown, caster (always self), cast logic (takes ablty, which means ability but can't be confused with the module, and target)], probability
            [ability.Ability("spit slime", 0, self, lambda ablty, target: ability.damage(ablty, target, 6, 10)), 0.7],
            [ability.Ability("jellification", 3, self, lambda ablty, target: ablty.caster.addEffect( effect.ArmorBuffAdd("jellification", 2, 40) )), 0.3]
        ])
        self.size = 3

    def attack(self, target):
        if self.health > 0:
            self.abilities.getOption(lambda ability: not ability.onCooldown()).activate(target)
        elif self.size > 1:
            self.size -= 1
            self.stats.health.value /= 2
            self.health = self.stats.health.getValue()

class Ghoul(monster.Monster):

    def __init__(self):
        monster.Monster.__init__(self, "unholy ooze", 60, loot.Loot("the unholy ooze", 2, 40, [
                [item.Nothing(), 0.8],
                [gear.Ring("unholy band", "an irregular loop formed from the hard core of an ancient ooze", 24, 99, lambda target: target.stats.criticalStrike.add(0.5), lambda target: target.stats.criticalStrike.add(-0.5)), 0.2]
            ]), [
            # [name, cooldown, caster (always self), cast logic (takes ablty, which means ability but can't be confused with the module, and target)], probability
            [ability.Ability("spit slime", 0, self, lambda ablty, target: ability.damage(ablty, target, 6, 10)), 0.7],
            [ability.Ability("jellification", 3, self, lambda ablty, target: ablty.caster.addEffect( effect.ArmorBuffAdd("jellification", 2, 40) )), 0.3]
        ])
        self.size = 3

    def attack(self, target):
        if self.health > 0:
            self.abilities.getOption(lambda ability: not ability.onCooldown()).activate(target)
        elif self.size > 1:
            self.size -= 1
            self.stats.health.value /= 2
            self.health = self.stats.health.getValue()


def getSkeletonCave():
    def getMonster():
        monsters = fList.FrequencyList([
            [SkeletonWarrior(), 0.4],
            [SkeletonArcher(), 0.4],
            [Ghoul(), 0.2]
        ])
        return monsters.getOption()
    def enter():
        output.proclaim("Skeleton Cave: The stone walls smell of rotted flesh. Something here chafes with life.")
    def exit():
        output.proclaim("You have left Skeleton Cave.")

    skeletonCaveActions = [
        actions.RestHeal(globals.player),
        actions.Scavenge(globals.player, [
            [actions.ScavengeGold(globals.player, 2, 6), 0.9],
            [actions.FindItem(globals.player, lambda drop: "While exploring the gloomy cave, you stumble across an small iron chest. You find " + str(drop) + ".", [
                [potions.HealthPotion("health potion", "a ghoul might have taken a swig", 14, 49, 35), 0.6],
                [item.Item("undead invasion plans", "someone at Fort Morning would want to see this", 9, 99), 0.3, True], # the True signifies that this is a unique drop, i.e. it can only ever drop once
                [gear.Trinket("misplaced femur", "where could its owner be?", 19, 59, lambda target: target.stats.health.add(20), lambda target: target.stats.health.add(-20)), 0.1]]), 0.1]
        ])
    ]
    skeletonCaveInteractions = [
        [fight.Fight(getMonster), 0.3],
        [actions.Nothing(), 0.7]
    ]
    return location.Location("Skeleton Cave", enter, exit, skeletonCaveActions, skeletonCaveInteractions)

# END OF SKELETON CAVE

# START OF DAMP LAIR

class AricneaTheSly(monster.Monster):

    def __init__(self):
        monster.Monster.__init__(self, "Aricnea the Sly", 120, loot.Loot("Aricnea the Sly", 2, 40, [
                [item.Nothing(), 0.8],
                [gear.Ring("unholy band", "an irregular loop formed from the hard core of an ancient ooze", 24, 99, lambda target: target.stats.strength.add(25.5), lambda target: target.stats.strength.add(-25.5)), 0.2]
            ]), [
            # [name, cooldown, caster (always self), cast logic (takes ablty, which means ability but can't be confused with the module, and target)], probability
            [ability.Ability("spit slllliiiiime", 0, self, lambda ablty, target: ability.damage(ablty, target, 6, 20)), 0.7],
            [ability.Ability("jellification", 3, self, lambda ablty, target: ablty.caster.addEffect( effect.ArmorBuffAdd("jellification", 2, 40) )), 0.3]
        ], unique=True)
        self.size = 4

    def attack(self, target):
        if self.health > 0:
            self.abilities.getOption(lambda ability: not ability.onCooldown()).activate(target)
        elif self.size > 1:
            self.size -= 1
            self.stats.health.value /= 2
            self.health = self.stats.health.getValue()


def getDampLair():
    def getMonster():
        monsters = fList.FrequencyList([
            [AricneaTheSly(), 1]
        ])
        return monsters.getOption()
    def enter():
        output.proclaim("Skeleton Cave: The stone walls smell of rotted flesh. Something here chafes with life.")
    def exit():
        output.proclaim("You have left Skeleton Cave.")

    skeletonCaveActions = [
        actions.RestHeal(globals.player),
        actions.Scavenge(globals.player, [
            [actions.ScavengeGold(globals.player, 2, 6), 0.9],
            [actions.FindItem(globals.player, lambda drop: "While exploring the gloomy cave, you stumble across an small iron chest. You find " + str(drop), [
                [potions.HealthPotion("health potion", "a ghoul might have taken a swig", 14, 49, 35), 0.6],
                [item.Item("undead invasion plans", "someone at Fort Morning would want to see this", 9, 99), 0.3, True], # the True signifies that this is a unique drop, i.e. it can only ever drop once
                [gear.Trinket("misplaced femur", "where could its owner be?", 19, 59, lambda target: target.stats.health.add(20), lambda target: target.stats.health.add(-20)), 0.1]]), 0.1]
        ])
    ]
    skeletonCaveInteractions = [
        [fight.Fight(getMonster), 9999999, True],
        [actions.Nothing(), 1]
    ]
    return location.Location("Skeleton Cave", enter, exit, skeletonCaveActions, skeletonCaveInteractions)

# END OF DAMP LAIR

# START OF FORT MORNING

class GiantSewerRat(monster.Monster):

    def __init__(self):
        monster.Monster.__init__(self, "giant sewer rat", 40, loot.Loot("the giant sewer rat", 2, 20, [
                [item.Nothing(), 0.9],
                [item.Item("strange doubloon", "cracked and faded, but it looks to be made of gold", 19, 84), 0.1]
            ]), [
            # [name, cooldown, caster (always self), cast logic (takes ablty, which means ability but can't be confused with the module, and target)], probability
            [ability.Ability("gnaw", 0, self, lambda ablty, target: ability.damage(ablty, target, 8, 14)), 0.4],
            [ability.Ability("bite", 0, self, lambda ablty, target: ability.damage(ablty, target, 4, 12)), 0.4],
            [ability.Ability("sewer plague", 1, self, lambda ablty, target: target.addEffect( effect.DamageOverTime("sewer plague", 3, 4, 6) )), 0.2]
        ])

class UnholyOoze(monster.Monster):

    def __init__(self):
        monster.Monster.__init__(self, "unholy ooze", 60, loot.Loot("the unholy ooze", 2, 40, [
                [item.Nothing(), 0.8],
                [gear.Ring("unholy band", "an irregular loop formed from the hard core of an ancient ooze", 24, 99, lambda target: target.stats.criticalStrike.add(0.5), lambda target: target.stats.criticalStrike.add(-0.5)), 0.2]
            ]), [
            # [name, cooldown, caster (always self), cast logic (takes ablty, which means ability but can't be confused with the module, and target)], probability
            [ability.Ability("spit slime", 0, self, lambda ablty, target: ability.damage(ablty, target, 6, 10)), 0.7],
            [ability.Ability("jellification", 3, self, lambda ablty, target: ablty.caster.addEffect( effect.ArmorBuffAdd("jellification", 2, 40) )), 0.3]
        ])
        self.size = 3

    def attack(self, target):
        if self.health > 0:
            self.abilities.getOption(lambda ability: not ability.onCooldown()).activate(target)
        elif self.size > 1:
            self.size -= 1
            self.stats.health.value /= 2
            self.health = self.stats.health.getValue()
            output.proclaim("The unholy ooze sheds a layer of goo and rises again!")

MorningWares = shop.Shop("Morning Wares", "Welcome to Morning Wares, traveller. We carry all manner of artifacts and armor.", [
    potions.HealthPotion("lesser health potion", "better than resting", 6, 19, 20),
    potions.HealthPotion("health potion", "an over-the-counter prescription for all dying heroes", 9, 29, 30),
    item.UsableItem("strength potion", "induces rage, overwhelming power, and possibly constipation", 7, 34, lambda target: target.addEffect( effect.StrengthBuffAdd("strength potion", 8, 10))),
    gear.Weapon("old knife", "short, rusted, but sharp", 6, 24, lambda target: target.stats.strength.add(4), lambda target: target.stats.strength.add(-4)),
    gear.Boots("leather boots", "they put a barrier between your feet and the ground", 12, 35, lambda target: target.stats.armor.add(4), lambda target: target.stats.armor.add(-4))
])

def getFortMorning():
    def getMonster():
        monsters = fList.FrequencyList([
            [GiantSewerRat(), 0.8],
            [UnholyOoze(), 0.2]
        ])
        return monsters.getOption()
    def enter():
        output.proclaim("Fort Morning: Rough cobblestones pattern the streets of Fort Morning. The din of the market carries loudly to the Southern gate, whose wall protrudes ten feet from the earth below. Merchants frequent the fort, but the eastern wizards rarely visit.")
    def exit():
        output.proclaim("You have left the Fort Morning.")

    fortMorningActions = [
        actions.RestHeal(globals.player),
        actions.Scavenge(globals.player, [
            [actions.ScavengeGold(globals.player, 0, 4), 1]
        ]),
        actions.Shop(globals.player, [MorningWares])
    ]
    fortMorningInteractions = [
        [actions.Nothing(), 0.93],
        [fight.Fight(getMonster), 0.07]
    ]
    return location.Location("Fort Morning", enter, exit, fortMorningActions, fortMorningInteractions)

traineeValley = getTraineeValley()

theSilentForest = getTheSilentForest()
skeletonCave = getSkeletonCave()
dampLair = getDampLair()

fortMorning = getFortMorning()

# Add connections between locations. It's always free to stay put.
################ UNLOCK ZONES BY LEVEL AND GOLD
traineeValley.setTaxi(actions.Taxi(globals.player, "Hello, " + str(globals.player) + ". I hear you'd like to travel. What can I do for you?", [[traineeValley, 0], [fortMorning, 49], [theSilentForest, 99]]))
traineeValley.interactions.add(actions.OfferLocationChange(globals.player, "A merchant's caravan approaches you. Its leader asks whether you want a ride to Fort Morning, where they are heading to sell western fish. Do you want to travel with them?", [fortMorning]), 0.01)

theSilentForest.setTaxi(actions.Taxi(globals.player, "We must tread cautiously in these woods, " + str(globals.player) + ". If you need transit, I may be able to aid you. Where do you wish to travel?", [[theSilentForest, 0], [traineeValley, 49]]))
theSilentForest.interactions.add(actions.OfferLocationChange(globals.player, "You spy a cave behind a crooked, dead tree. A faint clicking can be heard from within. Do you want to enter the cave?", [skeletonCave]), 0.015)
skeletonCave.setTaxi(actions.NullTaxi(globals.player))
skeletonCave.interactions.add(actions.OfferLocationChange(globals.player, "An ominous darkness makes you shiver. In the distance, you see a large cavern occupied by a skeleton eight feet tall. Do you want to enter the Damp Lair?", [dampLair]), 0.04, True)
#dampLair.setTaxi(actions.NullTaxi(globals.player))

fortMorning.setTaxi(actions.Taxi(globals.player, "If you wish to travel, sir, then there's no better than the Fort Morning Coach Company. Where to?", [[fortMorning, 0], [traineeValley, 49]]))
