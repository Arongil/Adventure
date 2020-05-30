import random
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
import npcs.npc as npc
import npcs.quest as quest
import location
import actions
import ability
import effect
import item

player = globals.get_player()

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
                [potions.HealthPotion("lean wolf flank", "its owner must not have had enough to eat", 2, 9, 6), 0.25],
                [gear.Gloves("torn wolfhide gloves", "the coarse fabric seems vaguely glovelike", 8, 26, lambda creature: creature.stats.add(armor=2), lambda creature: creature.stats.add(armor=-2)), 0.05]
            ]), [
            # [name, cooldown, caster (always self), cast logic (takes ablty, which means ability but can't be confused with the module, and target)], probability
            [ability.Ability("bite", 0, lambda ablty, caster, target: ability.damage(ablty, caster, target, 2, 6)), 0.5],
            [ability.Ability("snap", 0, lambda ablty, caster, target: ability.damage(ablty, caster, target, 4, 8)), 0.3],
            [ability.Ability("lick wounds", 2, lambda ablty, caster, target: ability.heal(ablty, caster, target, 4, 10)), 0.2]
        ])

class DrunkenTrainee(monster.Monster):

    def __init__(self):
        monster.Monster.__init__(self, "drunken trainee", 60, loot.Loot("the drunken trainee", 5, 30, [
                [item.Nothing(), 0.4],
                [item.UsableItem("cheap whiskey", "it's nearly empty", 5, 19, lambda target: target.addEffect( effect.DamageOverTime("intoxication", 3, 1, 2, self) )), 0.6]
            ]), [
            # [name, cooldown, caster (always self), cast logic (takes ablty, which means ability but can't be confused with the module, and target)], probability
            [ability.Ability("charge", 0, lambda ablty, caster, target: ability.damage(ablty, caster, target, 6, 10)), 0.5],
            [ability.Ability("stumble", 0, lambda ablty, caster, target: self.stumble()), 0.3],
            [ability.Ability("vomit", 4, lambda ablty, caster, target: target.addEffect( effect.DamageOverTime("intoxicated vomit", 2, 3, 5, self) )), 0.2]
        ])

    def stumble(self):
        output.say("The drunken trainee stumbles and attempts to regain balance.")

class GraglisTheGremlin(monster.Monster):

    def __init__(self):
        def voodooFetishProc(wearer, target):
            if random.random() < 0.05:
                output.say(wearer.the.capitalize() + "'s voodoo fetish begins wailing softly, disorienting " + target.the + ".")
                target.addEffect( effect.StrengthBuff("voodoo stun", 2, -0.2) )

        self.voodooFetish = gear.Trinket("voodoo fetish", "the force that governs voodoo is twisted and vague... only strange creatures commune with it well", 29, 99, lambda target: target.stats.add(criticalChance=0.1), lambda target: target.stats.add(criticalChance=-0.1), voodooFetishProc)
        monster.Monster.__init__(self, "Graglis the Gremlin", 80, loot.Loot("Graglis the Gremlin", 16, 140, [
                [self.voodooFetish, 1]
            ]), [
            # [name, cooldown, caster (always self), cast logic (takes ablty, which means ability but can't be confused with the module, and target)], probability
            [ability.Ability("hop and scratch", 0, lambda ablty, caster, target: ability.damage(ablty, caster, target, 7, 16)), 0.5],
            [ability.Ability("mutter nonsense", 0, lambda ablty, caster, target: self.mutterNonsense()), 0.3],
            [ability.Ability("voodoo", 6, lambda ablty, caster, target: self.voodoo()), 0.2]
        ], dodge=0.15, unique=True)
        self.gear.equip(self.voodooFetish)

    def mutterNonsense(self):
        vocabulary = ["fizzle", "crack", "wow", "water", "fun", "bam", "shahoo", "wapwalee", "pow", "rats", "netter", "crab", "mast", "crazy", "polar", "braid", "blubber", "dollop", "doozy", "finagle", "gargoyle", "giggle", "shenanigans", "squabble", "wipee"]
        gibberish = []
        for i in range(6):
            gibberish.append(random.choice(vocabulary))
        output.say("Graglis the Gremlin bursts out into gleeful nonsense: " + ' '.join(gibberish).capitalize() + "!")

    def voodoo(self):
        output.say("Graglis begins to dance frantically, screaming gibberish all the while. Black mist forms reptilian strands in the air.")
        self.addEffect( effect.StrengthBuffAdd("voodoo ritual", 6, 8) )

def getTraineeValley():
    def enter():
        output.proclaim("Trainee Valley: Sparse trees occupy rolling expanses of lush grass. Fort Morning is barely visible in the distant north, while the Silent Forest looms to the east.")
    def exit():
        output.proclaim("You have left Trainee Valley.")

    def getMonster():
        return fList.FrequencyList([
            [Wolf(), 0.8],
            [DrunkenTrainee(), 0.2]
        ]).getOption()

    traineeValleyActions = [
        actions.RestHeal(player),
        actions.Scavenge(player, [
            [actions.ScavengeGold(player, 0, 2), 0.98],
            # health, armor, strength, spirit, criticalChance, criticalStrike, dodge
            [shrine.StatShrine([20, 10, 10, 10, 0.1, 1, 0.2], 50), 0.02]
        ])
    ]
    traineeValleyInteractions = [
        [actions.Nothing(), 0.8],
        [fight.Fight(getMonster), 0.2],
        [fight.Fight(lambda: GraglisTheGremlin()), 0.008, True]
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
            [ability.Ability("pounce", 999, lambda ablty, caster, target: ability.damage(ablty, caster, target, 14, 20)), 999],
            [ability.Ability("claw", 0, lambda ablty, caster, target: ability.damage(ablty, caster, target, 6, 8)), 0.8],
            [ability.Ability("tense", 2, lambda ablty, caster, target: caster.addEffect( effect.StrengthBuff("tense", 1, 0.5) )), 0.2]
        ])

class Owl(monster.Monster):

    def __init__(self):
        monster.Monster.__init__(self, "owl", 30, loot.Loot("the owl", 2, 40, [
                [item.Nothing(), 0.8],
                [item.Item("feather", "it's definitely a feather", 1, 4), 0.2]
            ]), [
            # [name, cooldown, caster (always self), cast logic (takes ablty, which means ability but can't be confused with the module, and target)], probability
            [ability.Ability("peck", 0, lambda ablty, caster, target: ability.damage(ablty, caster, target, 4, 8)), 0.6],
            [ability.Ability("gouge", 0, lambda ablty, caster, target: ability.damage(ablty, caster, target, 8, 12)), 0.4]
        ])

class SorcererOutcast(monster.Monster):

    def __init__(self):
        monster.Monster.__init__(self, "sorcerer outcast", 50, loot.Loot("the sorcerer outcast", 8, 80, [
                [item.Nothing(), 0.4],
                [item.UsableItem("mysterious green brew", "it could be poison, it could be eternal life, it could be stool softener", 9, 49, lambda target: target.addEffect( effect.SpiritBuff("heightened spirits", 20, 2) )), 0.2],
                [item.Item("cryptic spellbook", "the writing looks hasty and is in an elvish tongue", 30, 99), 0.2],
                [gear.Helmet("pointy black hat", "several patches mottle the hat, including a long seam directly above the brim", 19, 49, lambda creature: creature.stats.add(criticalChance=0.05), lambda creature: creature.stats.add(criticalChance=-0.05)), 0.2]
            ]), [
            # [name, cooldown, caster (always self), cast logic (takes ablty, which means ability but can't be confused with the module, and target)], probability
            [ability.Ability("frostbolt", 0, lambda ablty, caster, target: ability.damage(ablty, caster, target, 8, 14)), 0.5],
            [ability.Ability("frigid wind", 2, lambda ablty, caster, target: target.addEffect( effect.StrengthBuff("frigid wind", 2, -0.5) )), 0.3],
            [ability.Ability("icy shield", 4, lambda ablty, caster, target: caster.addEffect( effect.ArmorBuff("icy shield", 3, 1) )), 0.2]
        ], armor=4)

class SkeletonScout(monster.Monster):

    def __init__(self):
        monster.Monster.__init__(self, "skeleton scout", 60, loot.Loot("the skeleton scout", 8, 140, [
                [item.Nothing(), 0.4],
                [item.Item("cracked bone", "dirty gray with a scratch along its middle", 3, 9), 0.6]
            ]), [
            # [name, cooldown, caster (always self), cast logic (takes ablty, which means ability but can't be confused with the module, and target)], probability
            [ability.Ability("charge", 999, lambda ablty, caster, target: ability.damage(ablty, caster, target, 9, 16)), 999],
            [ability.Ability("slash", 0, lambda ablty, caster, target: ability.damage(ablty, caster, target, 6, 15)), 0.8],
            [ability.Ability("fuse bone", 4, lambda ablty, caster, target: ability.heal(ablty, caster, target, 18, 30)), 0.2]
        ])

class DoomPanda(monster.Monster):

    def __init__(self):
        monster.Monster.__init__(self, "doom panda", 500, loot.Loot("the doom panda", 260, 1, [
                [item.UsableItem("big black potion", "this is undoubtedly some bad stuff", 1, 2, lambda target: target.addEffect( effect.StrengthBuff("strength of a doom panda", 8, 30) )), 0.5],
                [gear.Weapon("The Black Scythe", "the sword of the doom panda", 1, 2, lambda target: target.stats.add(strength=10, criticalChance=0.1), lambda target: target.stats.add(strength=-10, criticalChance=-0.1)), 0.5]
            ]), [
            # [name, cooldown, caster (always self), cast logic (takes ablty, which means ability but can't be confused with the module, and target)], probability
            [ability.Ability("cuddle", 0, lambda ablty, caster, target: ability.heal(ablty, caster, target, 1, 5)), 0.9],
            [ability.Ability("DOOOOOOOOOOM", 6, lambda ablty, caster, target: ability.damage(ablty, caster, target, 80, 100)), 0.1],
        ], armor=16, criticalChance=0)

def getTheSilentForest():
    def enter():
        output.proclaim("The Silent Forest: Great oaks sway endlessly to the southerly winds. The air's oppression is lifted but briefly at the occasional rustle. Trees obscure the view to Trainee Valley.")
    def exit():
        output.proclaim("You have left the Silent Forest.")

    def getMonster():
        return fList.FrequencyList([
            [ProwlingFox(), 0.4],
            [Owl(), 0.35],
            [SorcererOutcast(), 0.2],
            [SkeletonScout(), 0.04],
            [DoomPanda(), 0.01]
        ]).getOption()

    theSilentForestActions = [
        actions.RestHeal(player),
        actions.Scavenge(player, [
            [actions.ScavengeGold(player, 0, 4), 0.99],
            # health, armor, strength, spirit, criticalChance, criticalStrike, dodge
            [shrine.StatShrine([20, 10, 10, 10, 0.1, 1, 0.2], 50), 0.01]
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
        monster.Monster.__init__(self, "skeleton warrior", 60, loot.Loot("the skeleton warrior", 4, 80, [
                [item.Nothing(), 0.6],
                [item.Item("cracked bone", "dirty gray with a scratch along its middle", 3, 9), 0.4]
            ]), [
            # [name, cooldown, caster (always self), cast logic (takes ablty, which means ability but can't be confused with the module, and target)], probability
            [ability.Ability("charge", 999, lambda ablty, caster, target: ability.damage(ablty, caster, target, 9, 16)), 999],
            [ability.Ability("slash", 0, lambda ablty, caster, target: ability.damage(ablty, caster, target, 6, 15)), 0.8],
            [ability.Ability("fuse bone", 4, lambda ablty, caster, target: ability.heal(ablty, caster, target, 18, 30)), 0.2]
        ])

class SkeletonArcher(monster.Monster):

    def __init__(self):
        monster.Monster.__init__(self, "skeleton archer", 60, loot.Loot("the skeleton archer", 4, 80, [
                [item.Nothing(), 0.4],
                [item.Item("cracked bone", "dirty gray with a scratch along its middle", 3, 9), 0.3],
                [item.Item("unfeathered arrow", "its tip seems to be made of tempered brown clay", 4, 6), 0.2],
                [gear.Boots("crude sabatons", "probably held together with mud and bone marrow", 15, 44, lambda target: target.stats.add(armor=2, criticalChance=0.02), lambda target: target.stats.add(armor=-2, criticalChance=-0.02)), 0.1]
            ]), [
            # [name, cooldown, caster (always self), cast logic (takes ablty, which means ability but can't be confused with the module, and target)], probability
            [ability.Ability("iron bolt", 0, lambda ablty, caster, target: ability.damage(ablty, caster, target, 9, 14)), 0.5],
            [ability.Ability("arrow as dagger", 0, lambda ablty, caster, target: ability.damage(ablty, caster, target, 1, 3, 21)), 0.4],
            [ability.Ability("archer's resolve", 2, lambda ablty, caster, target: caster.addEffect( effect.CriticalChanceBuffAdd("archer's resolve", 2, 0.6) )), 0.1]
        ])

class Ghoul(monster.Monster):

    def __init__(self):
        monster.Monster.__init__(self, "ghoul", 60, loot.Loot("the ghoul", 5, 120, [
                [item.Nothing(), 0.8],
                [item.Item("decayed fingernail", "dry, brittle, came from a ghoul", 1, 4), 0.2]
            ]), [
            # [name, cooldown, caster (always self), cast logic (takes ablty, which means ability but can't be confused with the module, and target)], probability
            [ability.Ability("knitting flesh", 999, lambda ablty, caster, target: caster.addEffect( effect.HealOverTime("knitting flesh", 9, 4, 10))), 999],
            [ability.Ability("mindless maul", 0, lambda ablty, caster, target: ability.damage(ablty, caster, target, 9, 18)), 0.7],
            [ability.Ability("putrid breath", 5, lambda ablty, caster, target: target.addEffect( effect.ArmorBuff("putrid breath", 4, -0.3) )), 0.3]
        ])

#################### W # A # R # N # I # N # G ####################
LJN = gear.Weapon("Laker-Justin Nunchucks", "You can probably guess the words on each nunchuck", 1000, 1001, lambda target: target.stats.add(strength=1000000, criticalChance=1, criticalStrike=15, armor=1000), lambda target: target.stats.add(strength=-1000000, criticalChance=-1, criticalStrike=-15, armor=-1000))
def addExp(caster, amount):
    caster.experience += amount
expPotions = item.UsableItem("Experience Potion", "The devs shouldn't have added this one", 1000, 1001, lambda caster: addExp(caster, 2000), 99)
if globals.debug:
    player.inventory.addItem(LJN)
    player.inventory.addItem(expPotions)
    player.inventory.addGold(999999)
###################### D # A # N # G # E # R ######################

def getSkeletonCave():
    def enter():
        output.proclaim("Skeleton Cave: The stone walls smell of rotted flesh. Something here chafes with life.")
    def exit():
        output.proclaim("You have left Skeleton Cave.")

    def getMonster():
        return fList.FrequencyList([
            [SkeletonWarrior(), 0.4],
            [SkeletonArcher(), 0.4],
            [Ghoul(), 0.2]
        ]).getOption()

    skeletonCaveActions = [
        actions.RestHeal(player),
        actions.Scavenge(player, [
            [actions.ScavengeGold(player, 2, 6), 0.9],
            [actions.FindItem(player, lambda drop: "While exploring the gloomy cave, you stumble across an small iron chest. You find " + str(drop) + ".", [
                [potions.HealthPotion("health potion", "a ghoul might have taken a swig", 14, 49, 35), 0.6],
                [gear.Trinket("misplaced femur", "where could its owner be?", 19, 59, lambda target: target.stats.add(health=20), lambda target: target.stats.add(health=-20)), 0.1]]), 0.1]
        ])
    ]
    skeletonCaveInteractions = [
        [actions.Nothing(), 0.72],
        [fight.Fight(getMonster), 0.28]
    ]
    return location.Location("Skeleton Cave", enter, exit, skeletonCaveActions, skeletonCaveInteractions)

# END OF SKELETON CAVE

# START OF DAMP LAIR

class BoneHound(monster.Monster):

    def __init__(self):
        monster.Monster.__init__(self, "bone hound", 30, loot.Loot("the bone hound", 0, 0), [
            # [name, cooldown, caster (always self), cast logic (takes ablty, which means ability but can't be confused with the module, and target)], probability
            [ability.Ability("bony bite", 0, lambda ablty, caster, target: ability.damage(ablty, caster, target, 6, 9)), 0.7],
            [ability.Ability("howl", 2, lambda ablty, caster, target: caster.addEffect( effect.StrengthBuffAdd("howl", 2, 12) )), 0.3]
        ])

class AricneaTheSly(monster.Monster):

    def __init__(self):
        def stingProc(wearer, target):
            if random.random() < 0.06:
                amount = wearer.dealDamage(target, 10 + random.random() * 8)
                output.say("Dark tendrils burst from Sting, crushing " + target.the + " and dealing " + output.formatNumber(amount) + " damage to it.")

        self.sting = gear.Weapon("Sting, Bone Reaper", "Aricnea's blade pulses with an ineffable energy", 89, 299, lambda target: target.stats.add(strength=12, criticalStrike=0.8), lambda target: target.stats.add(strength=-12, criticalStrike=-0.8), stingProc)
        monster.Monster.__init__(self, "Aricnea the Sly", 220, loot.Loot("Aricnea the Sly", 38, 1460, [
                [item.Item("undead invasion plans", "someone at Fort Morning would want to see this", 9, 99), 1],
                [self.sting, 1]
            ], True), [ # the True signifies Aricnea will drop all items in his loot table, every time.
            # [name, cooldown, caster (always self), cast logic (takes ablty, which means ability but can't be confused with the module, and target)], probability
            [ability.Ability("stab", 0, lambda ablty, caster, target: ability.damage(ablty, caster, target, 11, 19)), 0.6],
            [ability.Ability("fan of knives", 0, lambda ablty, caster, target: ability.damage(ablty, caster, target, 18, 26)), 0.2],
            [ability.Ability("draw shadows", 3, lambda ablty, caster, target: caster.addEffect( effect.ArmorBuff("draw shadows", 3, 0.8) )), 0.2]
        ], unique=True)
        self.gear.equip(self.sting)
        self.calledDogs = False
        self.dogs = fList.FrequencyList([[BoneHound(), 1]])
        self.dogFight = fight.Fight(lambda: self.dogs.getOption())

    def attack(self, target):
        if self.health < 100 and not self.calledDogs:
            # The player fights two of Aricnea's dogs when Aricnea gets low on health.
            self.calledDogs = True
            output.bar()
            output.exclaim("Ha! You insect think to best me? Finish the swine, dogs!")
            output.bar()
            player.update()
            self.dogFight.activate()
            player.update()
            self.dogFight.activate()
            output.exclaim("Aaaah! You shall not defeat the forces of the undead... we are eternal!")
            self.addEffect( effect.HealOverTime("glory for the undead", 2, 30, 50) )
            self.addEffect( effect.StrengthBuff("battle rage", 9, 0.6) )
        else:
            self.abilities.getOption(lambda ability: not ability.onCooldown()).activate(self, target)

def getDampLair():
    def enter():
        output.proclaim("Damp Lair: Cave moss grows on the arched ceiling of the cavern. A faint light glows in distance. The huge skeleton turns to face you.")
    def exit():
        output.proclaim("You have left Damp Lair.")

    def getMonster():
        return fList.FrequencyList([
            [AricneaTheSly(), 1]
        ]).getOption()

    skeletonCaveActions = [
        actions.RestHeal(player)
    ]
    skeletonCaveInteractions = [
        [fight.Fight(getMonster), 999999999, True],
        [actions.Nothing(), 1]
    ]
    return location.Location("Damp Lair", enter, exit, skeletonCaveActions, skeletonCaveInteractions)

# END OF DAMP LAIR

# START OF FORT MORNING

class GiantSewerRat(monster.Monster):

    def __init__(self):
        monster.Monster.__init__(self, "giant sewer rat", 40, loot.Loot("the giant sewer rat", 3, 30, [
                [item.Nothing(), 0.9],
                [item.Item("strange doubloon", "cracked and faded, but it looks to be made of gold", 19, 84), 0.1]
            ]), [
            # [name, cooldown, caster (always self), cast logic (takes ablty, which means ability but can't be confused with the module, and target)], probability
            [ability.Ability("gnaw", 0, lambda ablty, caster, target: ability.damage(ablty, caster, target, 8, 14)), 0.4],
            [ability.Ability("bite", 0, lambda ablty, caster, target: ability.damage(ablty, caster, target, 4, 12)), 0.4],
            [ability.Ability("sewer plague", 1, lambda ablty, caster, target: target.addEffect( effect.DamageOverTime("sewer plague", 3, 4, 6, self) )), 0.2]
        ])

class UnholyOoze(monster.Monster):

    def __init__(self):
        monster.Monster.__init__(self, "unholy ooze", 60, loot.Loot("the unholy ooze", 2, 70, [
                [item.Nothing(), 0.8],
                [gear.Ring("unholy band", "an irregular loop formed from the hard core of an ancient ooze", 24, 99, lambda target: target.stats.add(criticalStrike=0.5, dodge=0.01), lambda target: target.stats.add(criticalStrike=-0.5, dodge=-0.01)), 0.2]
            ]), [
            # [name, cooldown, caster (always self), cast logic (takes ablty, which means ability but can't be confused with the module, and target)], probability
            [ability.Ability("spit slime", 0, lambda ablty, caster, target: ability.damage(ablty, caster, target, 6, 10)), 0.7],
            [ability.Ability("jellification", 3, lambda ablty, caster, target: caster.addEffect( effect.ArmorBuff("jellification", 2, 1.4) )), 0.3]
        ])
        self.size = 3

    def attack(self, target):
        if self.health > 0:
            self.abilities.getOption(lambda ability: not ability.onCooldown()).activate(self, target)
        elif self.size > 1:
            self.size -= 1
            self.stats.health.value /= 2
            self.health = self.stats.health.getValue()
            output.proclaim("The unholy ooze sheds a layer of goo and rises again!")


def boozeStainedWarglaivesProc(wearer, target):
    if random.random() < 0.15:
        target.addEffect( effect.DamageOverTime("contagious intoxication", 3, 4, 6, caster=wearer) )
boozeStainedWarglaives = gear.Weapon("booze-stained warglaives", "they seriously smell like cheap whisky, but hey, they're warglaives!", 19, 31, lambda target: target.stats.add(armor=6, health=15), lambda target: target.stats.add(armor=-6, health=-15), boozeStainedWarglaivesProc)

captainJorna = npc.NPC("Captain Jorna", "Fort Morning never pays its hardest workers enough. They give me a pittance, I tell you! It's barely enough to buy rations and drink.", [
    quest.Quest(
        "Drunkards and Me",
        "The trainees are all out staggering and drunk at this time of year, trampling wildflowers and scaring away the rabbits. I don't get paid enough to go and round them up, of course. But I could probably figure something out for you if you went and taught them a lesson.\n\nGo to trainee valley and bring me three of their bottles of cheap whiskey to prove you've done your job, will you?",
        "Do you have the three bottles of whiskey yet? I'm getting jittery waiting.",
        "Wonderful! You have the whiskey right? Ah, here, perfect.\n\nAnd your compensation, how could I forget? All right, now you be off. Thanks for your help and all.",
        lambda player: player.checkAndRemove("cheap whiskey", 3),
        loot.Loot("Captain Jorna", 40, 600, [
            [item.UsableItem("mysterious box", "open it!", 1, 4, lambda target: target.inventory.addItem(
                item.UsableItem("smaller mysterious box", "now you have to see what's inside", 1, 3, lambda target: target.inventory.addItem(
                    item.UsableItem("tiny mysterious box", "russian dolls confirmed", 1, 2, lambda target: target.inventory.addItem(
                        item.UsableItem("miniscule flask", "there's hardly a drop of liquid in it", 1, 1, lambda target: target.addEffect( effect.SpiritBuff("drunken", 2, 4) ))
                    ))
                ))
            )), 1]
        ], True),
        lambda player: True
    ), quest.Quest(
        "The Bold Undead",
        "The skeletons are starting to form in larger groups in the Silent Forest. All my trainees are drunk, as you know, so I think we'll have to settle for you and your meager skills.\n\nThe skeletons will spare you no mercy, adventurer. Bring your strongest armor, and purchase health potions from the town shop to prepare yourself.\n\nGo to the Silent Forest and find the Skeleton Cave. From there, bring me four cracked bones from the skeletons to prove your deeds and worth.",
        "Have you killed them skellers yetters? I'm sober fur suuure, why doo you ask?",
        "Niiiice jooob. Speeeaking o' which, do you haaave aaany cheap whiiisky fooor meee?\n\nOh, I waaas supppooooosed to give yooou somethin'. Okay, then, here yooou aaare. Now gooo awaaaay yooaauu nincompoop.",
        lambda player: player.checkAndRemove("cracked bone", 4),
        loot.Loot("Captain Jorna", 60, 1000, [
            [gear.Chest("booze-stained cuirass", "all drunken trainees are required to wear it for their weekly shame sessions, but it's surprisingly strong", 23, 54, lambda target: target.stats.add(armor=6, health=15), lambda target: target.stats.add(armor=-6, health=-15)), 1],
            [potions.HealthPotion("stale bread", "there's already a bite missing...", 1, 9, 12), 1],
            [boozeStainedWarglaives, 1]
        ], True),
        lambda player: player.level >= 5
    ), quest.Quest(
        "Invasion",
        "", # This quest is only visible if it's already completed, so no need for original text.
        "",
        "You found an invasion map, eh? Let me see what we have coming at us.\n\n*Captain Jorna scans the torn page. Her eyes widen halfway through.*\n\nThe undead plan to come tonight. They have a northern siege engine, too, by the looks of this diagram. Thank you for bringing me this.",
        lambda player: player.checkAndRemove("undead invasion plans", 1),
        loot.Loot("Captain Jorna", 80, 1200, []),
        lambda player: player.has("undead invasion plans", 1),
        True # the True here signifies that this quest can jump straight to completion if the condition is satisfied, which it will be if the player is seeing the quest
    )
])

morningWares = shop.Shop("Morning Wares", "Welcome to Morning Wares, traveller. We carry all manner of artifacts and armor.", [
    potions.HealthPotion("lesser health potion", "better than resting", 6, 19, 20),
    potions.HealthPotion("health potion", "an over-the-counter prescription for all dying heroes", 9, 29, 30),
    item.UsableItem("strength potion", "induces rage, overwhelming power, and possibly constipation", 7, 34, lambda target: target.addEffect( effect.StrengthBuffAdd("strength potion", 8, 6, stackable=True))),
    gear.Weapon("old knife", "short, rusted, but sharp", 6, 24, lambda target: target.stats.add(strength=3), lambda target: target.stats.add(strength=-3)),
    gear.Boots("leather boots", "they put a barrier between your feet and the ground", 12, 35, lambda target: target.stats.add(health=5, armor=3), lambda target: target.stats.add(health=-5, armor=-3))
])
villageArmory = shop.Shop("Village Armory", "You'll find weapons from across the land in the Village Armory.", [
    gear.Gloves("dull chain gloves", "scratchy", 13, 52, lambda target: target.stats.add(armor=3, strength=3), lambda target: target.stats.add(armor=-3, strength=-3)),
    gear.Helmet("green crown of healing", "warm to the touch, it inspires tender care and enhanced recovery", 19, 64, lambda target: target.stats.add(health=5, armor=1, spirit=4), lambda target: target.stats.add(health=-5, armor=-1, spirit=-4))
])

def getFortMorning():
    def enter():
        output.proclaim("Fort Morning: Rough cobblestones pattern the streets of Fort Morning. The din of the market carries loudly to the Southern gate, whose wall protrudes ten feet from the earth below. Merchants frequent the fort, but the eastern wizards rarely visit.")
    def exit():
        output.proclaim("You have left the Fort Morning.")

    def getMonster():
        return fList.FrequencyList([
            [GiantSewerRat(), 0.8],
            [UnholyOoze(), 0.2]
        ]).getOption()

    fortMorningActions = [
        actions.RestHeal(player),
        actions.Scavenge(player, [
            [actions.ScavengeGold(player, 0, 3), 1]
        ]),
        actions.Talk(player, [captainJorna]),
        actions.Shop(player, [morningWares, villageArmory])
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
# TAXI STRATEGY: keep prices low so players are motivated to do quests that require travel. Players are implicitly motivated to not travel to zones out of their level range, where the monsters could easily kill them.
traineeValley.setTaxi(actions.Taxi(player, "Hello, " + str(player) + ". I hear you'd like to travel. What can I do for you?", [[traineeValley, 0], [fortMorning, 4], [theSilentForest, 9]]))
traineeValley.interactions.add(actions.OfferLocationChange(player, "A merchant's caravan approaches you. Its leader asks whether you want a ride to Fort Morning, where they are heading to sell western fish. Do you want to travel with them?", [fortMorning]), 0.01)

theSilentForest.setTaxi(actions.Taxi(player, "We must tread cautiously in these woods, " + str(player) + ". If you need transit, I may be able to aid you. Where do you wish to travel?", [[theSilentForest, 0], [traineeValley, 9]]))
theSilentForest.interactions.add(actions.OfferLocationChange(player, "You spy a cave behind a crooked, dead tree. A faint clicking can be heard from within. Do you want to enter the cave?", [skeletonCave]), 0.015)
skeletonCave.setTaxi(actions.Taxi(player, "Do you want to retrace your steps and leave the dark cave?", [[skeletonCave, 0], [theSilentForest, 0]]))
skeletonCave.interactions.add(actions.OfferLocationChange(player, "An ominous darkness makes you shiver. In the distance, you see a large cavern occupied by a towering skeleton with a blue glowing sword. Do you want to enter the Damp Lair?", [dampLair]), 0.04, True)
dampLair.setTaxi(actions.Taxi(player, "You see a soft beam of light faintly in the distance. If you follow it, you'll make your way out of the skeleton cave. Do you want to leave?", [[dampLair, 0], [theSilentForest, 0]]))

fortMorning.setTaxi(actions.Taxi(player, "If you wish to travel, sir, then there's no better than the Fort Morning Coach Company. Where to?", [[fortMorning, 0], [traineeValley, 4]]))
