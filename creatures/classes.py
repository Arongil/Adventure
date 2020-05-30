import random
import globals
import output
import creatures.stats as stats
import ability
import actions
import effect

classes = dict()

def get_classes():
    return list(classes.keys())

def get_stats(class_name):
    return classes[class_name]["stats"]
def get_abilities(class_name):
    return classes[class_name]["abilities"]
def get_levelBonus(class_name):
    return classes[class_name]["levelBonus"]
def get_states(class_name):
    return classes[class_name]["states"]
def get_classInspect(class_name):
    return classes[class_name]["classInspect"]
def get_classUpdate(class_name):
    return classes[class_name]["classUpdate"]
def get_classIntro(class_name):
    return classes[class_name]["classIntro"]

# Current Classes: mage, rogue, paladin

# structure: states (i.e. stealth or mana), classInspect (i.e. returns "Mana 100/100), stats, abilities (that player has at level 1), levelBonus (abilities player gains they level)
'''
classes["generic-example"] = {
    "stats": stats.Stats(
        health=100,
        armor=0,
        strength=0,
        spirit=0,
        criticalChance=0.1,
        criticalStrike=2
    ),
    "abilities": [
        # name, cooldown, cast logic (takes ablty, which means ability but can't be confused with the module, and target)
        ability.Ability("punch", 0, lambda ablty, caster, target: ability.damage(ablty, caster, target, 5, 15))
    ],
    "levelBonus": [
        # [name, cooldown, cast logic (takes ablty, which means ability but can't be confused with the module, and target)], levelToGainAbility
        [ability.Ability("fireball", 2, lambda ablty, caster, target: ability.damage(ablty, caster, target, 10, 20)), "Fireball burns the enemy between 10 and 20 base damage.", 3],
        [ability.Ability("iron heart", 20, lambda ablty, caster, target: caster.addEffect( effect.ArmorBuff("iron heart", 4, 1) )), "Iron heart strengthens your resolve, halving the damage you take for four turns.", 8],
        [ability.Ability("frenzy", 20, lambda ablty, caster, target: caster.addEffect( effect.StrengthBuff("frenzy", 6, 0.4) )), "Frenzy makes you wild and powerful, increasing the damage you deal by 40% for six turns.", 15]
    ]
}
'''

# MAGE
def mageInspect(player):
    return "Mana " + str(player.states["mana"]) + "/100"

# mana regen per turn = base regen * spirit, where 1 point of spirit = 0.5 more mana per turn
def regenMana(player):
    modifier = player.stats.spirit.getValue() / player.stats.scale
    newMana = player.states["mana"] + player.states["baseManaRegen"] * modifier
    player.states["mana"] = 100 if newMana > 100 else newMana
def consumeMana(player, amount):
    player.states["mana"] -= amount

def mageUpdate(player):
    regenMana(player)

def getFireball():
    manaCost = 5
    def available(player):
        return player.states["mana"] >= manaCost

    def fireballLogic(ablty, player, target):
        consumeMana(player, manaCost)
        regenMana(player)
        ability.damage(ablty, player, target, 5, 15)

    return ability.Ability("fireball", cooldown=0, cast=fireballLogic, condition=available)

def getFrostbolt():
    manaCost = 15
    def available(player):
        return player.states["mana"] >= manaCost

    def frostboltLogic(ablty, player, target):
        consumeMana(player, manaCost)
        regenMana(player)
        ability.damage(ablty, player, target, 5, 11)
        target.addEffect( effect.StrengthBuff("freeze", 3, -0.15) )

    return ability.Ability("frostbolt", cooldown=0, cast=frostboltLogic, condition=available)

def getScorch():
    manaCost = 30
    def available(player):
        return player.states["mana"] >= manaCost

    def scorchLogic(ablty, player, target):
        consumeMana(player, manaCost)
        regenMana(player)
        target.addEffect( effect.DamageOverTime("scorch", duration=8, lowerBound=2, upperBound=5, caster=player, stackable=True) )

    return ability.Ability("scorch", cooldown=0, cast=scorchLogic, condition=available)

def getIceBarrier():
    manaCost = 50
    def available(player):
        return player.states["mana"] >= manaCost

    def iceBarrierLogic(ablty, player, target):
        consumeMana(player, manaCost)
        regenMana(player)
        player.addEffect( effect.ArmorBuff("ice barrier", duration=4, amount=1) )

    return ability.Ability("ice barrier", cooldown=20, cast=iceBarrierLogic, condition=available)

def getEvocate():
    manaCost = 0
    def available(player):
        return player.states["mana"] >= manaCost

    def evocateLogic(ablty, player, target):
        player.states["mana"] = 100
        output.say("You evocate to refill your mana.")

    return ability.Ability("evocate ", cooldown=40, cast=evocateLogic, condition=available)

classes["mage"] = {
    "states": {
        "mana": 100, # max mana is always 100 as well
        "baseManaRegen": 10
    },
    "classInspect": mageInspect,
    "classUpdate": mageUpdate,
    "classIntro": "Mages are spell-casters. This uses mana, which ranges from 0 to 100. Cheaper spells let a mage recover mana so the mage can cast expensive spells when necessary. Mages recover 10 mana per turn, increased by a higher spirit stat. FIREBALL does an average of 10 damage and costs 5 mana.",
    "stats": stats.Stats(
        health=80,
        armor=0,
        strength=0,
        spirit=0,
        criticalChance=0.1,
        criticalStrike=2.1,
        dodge=0.02
    ),
    "abilities": [ getFireball() ],
    "levelBonus": [
        # ability, description, levelToGainAbility
        [getFrostbolt(), "Frostbolt freezes the enemy, dealing an average of 8 damage and reducing enemy's damage output by 15% for 3 turns. It costs 15 mana.", 3],
        [getScorch(), "Scorch burns the enemy, dealing 2 to 5 damage per turn over 8 turns. It costs 30 mana. Stackable.", 6],
        [getIceBarrier(), "Ice barrier summons a shield around you that reduces incoming damage by 50% for 4 turns. It has a 20 turn cooldown and costs 50 mana.", 9],
        [getEvocate(), "Evocate restores your mana to full. It has a 40 turn cooldown.", 12]
    ]
}

# ROGUE
def rogueInspect(player):
    info = [
        # [displayed, state name]
        ["Stealthed.", "stealth"],
        ["Dagger poisoned.", "daggerPoisoned"]
    ]
    displayInfo = filter(lambda i: player.states[i[1]], info)
    return ' '.join(i[0] for i in displayInfo)

def enterStealth(player):
    player.states["stealth"] = True
    # add dodge buff that will persist until it is removed upon unstealthing
    player.addEffect( effect.DodgeBuff("stealth", duration=99999, amount=3, notify=False) )

def exitStealth(player):
    player.states["stealth"] = False
    player.removeEffect( effect.DodgeBuff("stealth", duration=99999, amount=3, notify=False) )

def rogueUpdate(player):
    exitStealth(player)

def getStab():
    def stabLogic(ablty, player, target):
        # stab deals 50% more damage if stealthed
        if player.states["stealth"]:
            ability.damage(ablty, player, target, 13, 17)
        else:
            ability.damage(ablty, player, target, 8, 12)

        # if the player coated their dagger with poison, apply it
        if player.states["daggerPoisoned"]:
            player.states["daggerPoisoned"] = False
            target.addEffect( effect.DamageOverTime("poison", duration=3, lowerBound=6, upperBound=9, caster=player) )

        # stab takes the player out of stealth
        exitStealth(player)

        # stab also has 30% to put the player in stealth
        if random.random() < 0.3:
            enterStealth(player)
            output.declare("Stab triggers stealth!")

    return ability.Ability("stab", cooldown=0, cast=stabLogic)

def getPoisonDagger():
    def available(player):
        return player.states["stealth"]

    def poisonLogic(ablty, player, target):
        # poison can only be cast when stealthed
        exitStealth(player)
        player.states["daggerPoisoned"] = True
        output.say("You coat your dagger in poison.")

    return ability.Ability("poison dagger", cooldown=0, cast=poisonLogic, condition=available)

def getSap():
    def available(player):
        return player.states["stealth"]

    def sapLogic(ablty, player, target):
        exitStealth(player)
        target.addEffect( effect.StrengthBuff("sap", duration=6, amount=-0.4) )

    return ability.Ability("sap", cooldown=20, cast=sapLogic, condition=available)

def getEmbraceShadows():
    def embraceShadowsLogic(ablty, player, target):
        enterStealth(player)
        player.addEffect( effect.ArmorBuff("embrace shadows", duration=3, amount=3) )

    return ability.Ability("embrace shadows", cooldown=20, cast=embraceShadowsLogic)

def getRollTheBones():
    def rollTheBonesLogic(ablty, player, target):
        exitStealth(player)
        player.addEffect( effect.CriticalChanceBuff("roll the bones", duration=10, amount=2) )

    return ability.Ability("roll the bones", cooldown=40, cast=rollTheBonesLogic)

classes["rogue"] = {
    "states": {
        "stealth": False,
        "daggerPoisoned": False
    },
    "classInspect": rogueInspect,
    "classUpdate": rogueUpdate,
    "classIntro": "Rogues are quick and adept in poisons. Their abilities are enhanced when they are in stealth. STAB does an average of 10 damage (15 while stealthed), and it has a 30% chance to put a rogue in stealth. Rogues are 4x as likely to dodge while stealthed.",
    "stats": stats.Stats(
        health=100,
        armor=0,
        strength=0,
        spirit=0,
        criticalChance=0.15,
        criticalStrike=2,
        dodge=0.05
    ),
    "abilities": [ getStab() ],
    "levelBonus": [
        # ability, description, levelToGainAbility
        [getPoisonDagger(), "Only usable if stealthed: concealed in the shadows, coat your dagger with poison to deal 6 to 9 damage per turn over 3 turns the next time you stab. Unstealths you.", 3],
        [getSap(), "Only usable if stealthed: sap the enemy to reduce their damage output by 40% for 6 turns. It has a cooldown of 20 turns.", 6],
        [getEmbraceShadows(), "Draw the shadows near, stealthing yourself and reducing all damage you take by 75% for 3 turns. It has a cooldown of 20 turns.", 9],
        [getRollTheBones(), "Roll the bones puts the duel in the hands of fate, increasing your critical strike chance by 200% for 10 turns. It has a cooldown of 40 turns.", 12]
    ]
}
