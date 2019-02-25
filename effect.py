import output
from random import random

class Effect:

    def __init__(self, name, duration, start, end, tick):
        self.name = name
        self.duration = duration
        self.start = start
        self.end = end
        self.tick = tick
        self.count = 0 # count starts at zero then counts up to duration

    def startNotification(self, target):
        return self.name.capitalize() + " on the " + str(target) + " for " + str(self.duration) + " turns!"

    def endNotification(self, target):
        return self.name.capitalize() + " on the " + str(target) + " has ended!"

    def update(self, target):
        if self.count == 0:
            self.start(target)
            output.say(self.startNotification(target))
        elif self.count > self.duration:
            self.end(target)
            output.say(self.endNotification(target))
            target.effects.remove(self)
        else:
            self.tick(target)
        self.count = self.count + 1

# STAT BUFFS

class HealthBuff(Effect):

    def __init__(self, name, duration, amount):
        Effect.__init__(self, name, duration,
                lambda target: self.addHealth(target),
                lambda target: self.removeHealth(target),
                lambda target: None
        )
        self.amount = amount
        self.verb = "increased" if self.amount > 0 else "reduced"

    def addHealth(self, target):
        target.stats.health.add(amount)
        target.health += amount

    def removeHealth(self, target):
        target.stats.health.add(-amount)
        if target.health > target.stats.health.getValue():
            target.health = target.stats.health.getValue()

    def startNotification(self, target):
        return self.name.capitalize() + ": the " + str(target) + "'s health is " + self.verb + " by " + output.formatNumber(abs(self.amount)) + " for " + str(self.duration) + " turns. The " + str(target) + "'s maximum health is now " + output.formatNumber(target.stats.health.getValue()) + "."

# MULTIPLICATIVE BUFFS

class ArmorBuff(Effect):

    def __init__(self, name, duration, amount):
        Effect.__init__(self, name, duration,
                lambda target: target.stats.armor.mult(amount),
                lambda target: target.stats.armor.mult(-amount),
                lambda target: None
        )
        self.amount = amount
        self.verb = "increased" if self.amount > 0 else "reduced"

    def startNotification(self, target):
        return self.name.capitalize() + ": the " + str(target) + "'s armor is " + self.verb + " by " + output.formatNumber(abs(100 * self.amount)) + "% for " + str(self.duration) + " turns. The " + str(target) + "'s armor is now " + output.formatNumber(target.stats.armor.getValue()) + "."

class StrengthBuff(Effect):

    def __init__(self, name, duration, amount):
        Effect.__init__(self, name, duration,
                lambda target: target.stats.strength.mult(amount),
                lambda target: target.stats.strength.mult(-amount),
                lambda target: None
        )
        self.amount = amount
        self.verb = "increased" if self.amount > 0 else "reduced"

    def startNotification(self, target):
        return self.name.capitalize() + ": the " + str(target) + "'s strength is " + self.verb + " by " + output.formatNumber(abs(100 * self.amount)) + "% for " + str(self.duration) + " turns. The " + str(target) + "'s strength is now " + output.formatNumber(target.stats.strength.getValue()) + "."

class SpiritBuff(Effect):

    def __init__(self, name, duration, amount):
        Effect.__init__(self, name, duration,
                lambda target: target.stats.spirit.mult(amount),
                lambda target: target.stats.spirit.mult(-amount),
                lambda target: None
        )
        self.amount = amount
        self.verb = "increased" if self.amount > 0 else "reduced"

    def startNotification(self, target):
        return self.name.capitalize() + ": the " + str(target) + "'s spirit is " + self.verb + " by " + output.formatNumber(abs(100 * self.amount)) + "% for " + str(self.duration) + " turns. The " + str(target) + "'s spirit is now " + output.formatNumber(target.stats.spirit.getValue()) + "."

class CriticalChanceBuff(Effect):

    def __init__(self, name, duration, amount):
        Effect.__init__(self, name, duration,
                lambda target: target.stats.criticalChance.mult(amount),
                lambda target: target.stats.criticalChance.mult(-amount),
                lambda target: None
        )
        self.amount = amount
        self.verb = "increased" if self.amount > 0 else "reduced"

    def startNotification(self, target):
        return self.name.capitalize() + ": the " + str(target) + "'s critical hit chance is " + self.verb + " by " + output.formatNumber(abs(100 * self.amount)) + "% for " + str(self.duration) + " turns. The " + str(target) + "'s critical hit chance is now " + output.formatNumber(target.stats.criticalChance.getValue()) + "."

class CriticalStrikeBuff(Effect):

    def __init__(self, name, duration, amount):
        Effect.__init__(self, name, duration,
                lambda target: target.stats.criticalStrike.mult(amount),
                lambda target: target.stats.criticalStrike.mult(-amount),
                lambda target: None
        )
        self.amount = amount
        self.verb = "increased" if self.amount > 0 else "reduced"

    def startNotification(self, target):
        return self.name.capitalize() + ": the " + str(target) + "'s critical hit damage is " + self.verb + " by " + output.formatNumber(abs(100 * self.amount)) + "% for " + str(self.duration) + " turns. The " + str(target) + "'s critical hit damage is now " + output.formatNumber(target.stats.criticalStrike.getValue()) + "."

class ArmorBuffAdd(Effect):

    def __init__(self, name, duration, amount):
        Effect.__init__(self, name, duration,
                lambda target: target.stats.armor.add(amount),
                lambda target: target.stats.armor.add(-amount),
                lambda target: None
        )
        self.amount = amount
        self.verb = "increased" if self.amount > 0 else "reduced"

    def startNotification(self, target):
        return self.name.capitalize() + ": the " + str(target) + "'s armor is " + self.verb + " by " + output.formatNumber(abs(self.amount)) + " for " + str(self.duration) + " turns. The " + str(target) + "'s armor is now " + output.formatNumber(target.stats.armor.getValue()) + "."

class StrengthBuffAdd(Effect):

    def __init__(self, name, duration, amount):
        Effect.__init__(self, name, duration,
                lambda target: target.stats.strength.add(amount),
                lambda target: target.stats.strength.add(-amount),
                lambda target: None
        )
        self.amount = amount
        self.verb = "increased" if self.amount > 0 else "reduced"

    def startNotification(self, target):
        return self.name.capitalize() + ": the " + str(target) + "'s strength is " + self.verb + " by " + output.formatNumber(abs(self.amount)) + " for " + str(self.duration) + " turns. The " + str(target) + "'s strength is now " + output.formatNumber(target.stats.strength.getValue()) + "."

class SpiritBuffAdd(Effect):

    def __init__(self, name, duration, amount):
        Effect.__init__(self, name, duration,
                lambda target: target.stats.spirit.add(amount),
                lambda target: target.stats.spirit.add(-amount),
                lambda target: None
        )
        self.amount = amount
        self.verb = "increased" if self.amount > 0 else "reduced"

    def startNotification(self, target):
        return self.name.capitalize() + ": the " + str(target) + "'s spirit is " + self.verb + " by " + output.formatNumber(abs(self.amount)) + " for " + str(self.duration) + " turns. The " + str(target) + "'s spirit is now " + output.formatNumber(target.stats.spirit.getValue()) + "."

class CriticalChanceBuffAdd(Effect):

    def __init__(self, name, duration, amount):
        Effect.__init__(self, name, duration,
                lambda target: target.stats.criticalChance.add(amount),
                lambda target: target.stats.criticalChance.add(-amount),
                lambda target: None
        )
        self.amount = amount
        self.verb = "increased" if self.amount > 0 else "reduced"

    def startNotification(self, target):
        return self.name.capitalize() + ": the " + str(target) + "'s critical hit chance is " + self.verb + " by " + output.formatNumber(abs(self.amount)) + " for " + str(self.duration) + " turns. The " + str(target) + "'s critical hit chance is now " + output.formatNumber(target.stats.criticalChance.getValue()) + "."

class CriticalStrikeBuffAdd(Effect):

    def __init__(self, name, duration, amount):
        Effect.__init__(self, name, duration,
                lambda target: target.stats.criticalStrike.add(amount),
                lambda target: target.stats.criticalStrike.add(-amount),
                lambda target: None
        )
        self.amount = amount
        self.verb = "increased" if self.amount > 0 else "reduced"

    def startNotification(self, target):
        return self.name.capitalize() + ": the " + str(target) + "'s critical hit damage is " + self.verb + " by " + output.formatNumber(abs(self.amount)) + " for " + str(self.duration) + " turns. The " + str(target) + "'s critical hit damage is now " + output.formatNumber(target.stats.criticalStrike.getValue()) + "."

# EFFECTS OVER TIME

class HealOverTime(Effect):
    
    def __init__(self, name, duration, lowerBound, upperBound):
        Effect.__init__(self, name, duration,
                lambda target: None,
                lambda target: None,
                lambda target: output.say("The " + str(target) + " recovers " + output.formatNumber(target.recoverHealth(lowerBound + random() * (upperBound - lowerBound))) + " health from " + self.name + ".")
        )
        self.lowerBound = lowerBound
        self.upperBound = upperBound

    def startNotification(self, target):
        return self.name.capitalize() + ": the " + str(target) + " will recover between " + output.formatNumber(abs(self.lowerBound)) + " and " + output.formatNumber(abs(self.upperBound)) + " health for " + str(self.duration) + " turns."

class DamageOverTime(Effect):
    
    def __init__(self, name, duration, lowerBound, upperBound):
        Effect.__init__(self, name, duration,
                lambda target: None,
                lambda target: None,
                lambda target: output.say("The " + str(target) + " takes " + output.formatNumber(target.takeDamage(lowerBound + random() * (upperBound - lowerBound))) + " damage from " + self.name + ".")
        )
        self.lowerBound = lowerBound
        self.upperBound = upperBound

    def startNotification(self, target):
        return self.name.capitalize() + ": the " + str(target) + " will take between " + output.formatNumber(abs(self.lowerBound)) + " and " + output.formatNumber(abs(self.upperBound)) + " damage for " + str(self.duration) + " turns."
