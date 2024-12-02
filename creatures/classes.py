import random
import game.globals as globals
import game.output as output
import creatures.stats as stats
import game.ability as ability
import game.actions as actions
import game.effect as effect

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
def get_combatUpdate(class_name):
    return classes[class_name]["combatUpdate"]
def get_classIntro(class_name):
    return classes[class_name]["classIntro"]

# Current Classes: mage, rogue, paladin

# MAGE

# display after health during combat
def mageInspect(player):
    return "Mana " + output.formatNumber(player.states["mana"]) + "/100"

# mana regen per turn = base regen * spirit, where 1 point of spirit = 0.5 more mana per turn
def regenMana(player):
    modifier = player.stats.spirit.getValue() / player.stats.scale
    newMana = player.states["mana"] + player.states["baseManaRegen"] * modifier
    player.states["mana"] = 100 if newMana > 100 else newMana
def consumeMana(player, amount):
    player.states["mana"] -= amount

def mageUpdate(player):
    regenMana(player)
def mageCombatUpdate(player):
    regenMana(player)

def getFireball():
    manaCost = 10
    def available(player):
        return player.states["mana"] >= manaCost

    def fireballLogic(ablty, player, target):
        consumeMana(player, manaCost)
        ability.damage(ablty, player, target, 5, 15)

    return ability.Ability("fireball", cooldown=0, cast=fireballLogic, condition=available)

def getFrostbolt():
    manaCost = 25
    def available(player):
        return player.states["mana"] >= manaCost

    def frostboltLogic(ablty, player, target):
        consumeMana(player, manaCost)
        ability.damage(ablty, player, target, 5, 7)
        target.addEffect( effect.StrengthBuff("freeze", 3, -0.2) )

    return ability.Ability("frostbolt", cooldown=0, cast=frostboltLogic, condition=available)

def getScorch():
    manaCost = 40
    def available(player):
        return player.states["mana"] >= manaCost

    def scorchLogic(ablty, player, target):
        consumeMana(player, manaCost)
        target.addEffect( effect.DamageOverTime("scorch", duration=8, lowerBound=3, upperBound=6, caster=player, stackable=True) )

    return ability.Ability("scorch", cooldown=0, cast=scorchLogic, condition=available)

def getPyroblast():
    manaCost = 80
    def available(player):
        return player.states["mana"] >= manaCost

    def pyroblastLogic(ablty, player, target):
        consumeMana(player, manaCost)
        ability.damage(ablty, player, target, 28, 36)

    return ability.Ability("pyroblast", cooldown=8, cast=pyroblastLogic, condition=available)

def getIceBarrier():
    manaCost = 60
    def available(player):
        return player.states["mana"] >= manaCost

    def iceBarrierLogic(ablty, player, target):
        consumeMana(player, manaCost)
        player.addEffect( effect.ArmorBuff("ice barrier", duration=4, amount=1) )

    return ability.Ability("ice barrier", cooldown=20, cast=iceBarrierLogic, condition=available)

def getEvocate():
    manaCost = 0
    def available(player):
        return player.states["mana"] >= manaCost

    def evocateLogic(ablty, player, target):
        player.states["mana"] = 100
        output.say("You evocate to refill your mana.")

    return ability.Ability("evocate", cooldown=40, cast=evocateLogic, condition=available)

classes["mage"] = {
    "states": {
        "mana": 100, # max mana is always 100 as well
        "baseManaRegen": 10
    },
    "classInspect": mageInspect,
    "classUpdate": mageUpdate,
    "combatUpdate": mageCombatUpdate,
    "classIntro": "Mages are spell-casters. This uses mana, which ranges from 0 to 100. Cheaper spells let a mage recover mana so the mage can cast expensive spells when necessary. Mages recover 10 mana per turn, increased by a higher spirit stat. FIREBALL does an average of 10 damage and costs 10 mana.",
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
        [getFrostbolt(), "Frostbolt freezes the enemy, dealing an average of 6 damage and reducing enemy's damage output by 20% for 3 turns. It costs 25 mana.", 3],
        [getScorch(), "Scorch burns the enemy, dealing 3 to 6 damage per turn over 8 turns. It costs 40 mana. Stackable.", 6],
        [getPyroblast(), "Pyroblast clobbers the enemy with a gigantic fireball, dealing 28 to 36 damage. It costs 80 mana.", 8],
        [getIceBarrier(), "Ice barrier summons a shield around you that reduces incoming damage by 50% for 4 turns. It has a 20 turn cooldown and costs 60 mana.", 10],
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
    if not player.states["stealth"]:
        player.states["stealth"] = True
        # add dodge buff that will persist until it is removed upon unstealthing
        player.stats.dodge.mult(3)

def exitStealth(player):
    if player.states["stealth"]:
        player.states["stealth"] = False
        # remove dodge buff
        player.stats.dodge.mult(-3)

def rogueUpdate(player):
    exitStealth(player)
def rogueCombatUpdate(player):
    pass

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

        # stab also has a chance (increased with dodge) to put the player in stealth
        if random.random() < 0.25 + player.stats.dodge.value:
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
    "combatUpdate": rogueCombatUpdate,
    "classIntro": "Rogues are quick and adept in poisons. Their abilities are enhanced when they are in stealth. STAB does an average of 10 damage (15 while stealthed), and it has a 25% chance to put a rogue in stealth, increased by 1% per point of dodge. Rogues are 4x as likely to dodge while stealthed.",
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
        [getPoisonDagger(), "Only usable if stealthed: concealed in the shadows, coat your dagger with poison to deal 6 to 9 base damage per turn over 3 turns the next time you stab. Unstealths you.", 3],
        [getSap(), "Only usable if stealthed: sap the enemy to reduce their damage output by 40% for 6 turns. It has a cooldown of 20 turns. Unstealths you.", 6],
        [getEmbraceShadows(), "Draw the shadows near, stealthing yourself and reducing all damage you take by 75% for 3 turns. It has a cooldown of 20 turns.", 9],
        [getRollTheBones(), "Roll the bones puts the duel in the hands of fate, increasing your critical strike chance by 200% for 10 turns. It has a cooldown of 40 turns. Unstealths you.", 12]
    ]
}

# PALADIN

# display after health during combat
def paladinInspect(player):
    return "Holy power " + str(player.states["holy power"]) + "/5"

def generateHolyPower(player, amount):
    player.states["holy power"] += amount
    if player.states["holy power"] > 5:
        player.states["holy power"] = 5
def consumeHolyPower(player, amount):
    player.states["holy power"] -= amount

def paladinUpdate(player):
    if player.states["holy power"] > 0:
        player.states["holy power"] -= 1
def paladinCombatUpdate(player):
    pass

def getSmite():
    def smiteLogic(ablty, player, target):
        ability.damage(ablty, player, target, 6, 10)
        generateHolyPower(player, 1)
        if random.random() < player.stats.criticalChance.getValue():
            output.declare("Smite grants an additional holy power!")
            generateHolyPower(player, 1)

    return ability.Ability("smite", cooldown=0, cast=smiteLogic)

def getJudgment():
    holyPowerCost = 3
    def available(player):
        return player.states["holy power"] >= holyPowerCost

    def judgmentLogic(ablty, player, target):
        consumeHolyPower(player, holyPowerCost)
        ability.damage(ablty, player, target, 13, 21)

    return ability.Ability("judgment", cooldown=0, cast=judgmentLogic, condition=available)

def getHolyTouch():
    # Holy touch requires at least 1 holy power to cast, but it consumes as much holy power as a paladin has.
    # The more holy power the paladin spends, the more powerful the heal will be.
    def available(player):
        return player.states["holy power"] >= 1

    def holyTouchLogic(ablty, player, target):
        holyPower = player.states["holy power"]
        consumeHolyPower(player, holyPower)
        ability.heal(ablty, player, target, 11*holyPower, 15*holyPower)

    return ability.Ability("holy touch", cooldown=0, cast=holyTouchLogic, condition=available)

def getShatteringJustice():
    holyPowerCost = 4
    def available(player):
        return player.states["holy power"] >= holyPowerCost

    def shatteringJusticeLogic(ablty, player, target):
        consumeHolyPower(player, holyPowerCost)
        target.addEffect( effect.ArmorBuff("shattering justice", duration=6, amount=-0.5) )

    return ability.Ability("shattering justice", cooldown=20, cast=shatteringJusticeLogic, condition=available)

def getDivineShield():
    holyPowerCost = 4
    def available(player):
        return player.states["holy power"] >= holyPowerCost

    def divineShieldLogic(ablty, player, target):
        consumeHolyPower(player, holyPowerCost)
        player.addEffect( effect.ArmorBuff("divine shield", duration=2, amount=100) )

    return ability.Ability("divine shield", cooldown=20, cast=divineShieldLogic, condition=available)

classes["paladin"] = {
    "states": {
        "holy power": 0 # max holy power is always 5
    },
    "classInspect": paladinInspect,
    "classUpdate": paladinUpdate,
    "combatUpdate": paladinCombatUpdate,
    "classIntro": "Paladins are warriors of the Light. They generate holy power when they attack, which they channel to use more powerful abilities. SMITE deals an average of 8 damage and generates 1 holy power. Smite also has a chance equal to the paladin's critical strike chance to generate an additional holy power.",
    "stats": stats.Stats(
        health=120,
        armor=0,
        strength=0,
        spirit=0,
        criticalChance=0.05,
        criticalStrike=2,
        dodge=0.02
    ),
    "abilities": [ getSmite() ],
    "levelBonus": [
        # ability, description, levelToGainAbility
        [getJudgment(), "Judgment delivers justice to its target, dealing 13 to 21 damage. It costs 3 holy power.", 3],
        [getHolyTouch(), "Holy touch calls upon all the holy power you have. For each point of holy power consumed, the spell heals the paladin between 11 and 15 health. It costs at least 1 holy power.", 6],
        [getShatteringJustice(), "Shattering justice burns at the enemy's armor with the power of the Light, reducing the enemy's armor by 50% for 6 turns. It costs 4 holy power and has a cooldown of 20 turns.", 9],
        [getDivineShield(), "Divine shield conjures a nearly impenetrable barrier around you, stopping 99% of incoming damage for 2 turns. It costs 4 holy power and has a 40 turn cooldown.", 12]
    ]
}
