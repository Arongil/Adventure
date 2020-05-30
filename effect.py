import output
from random import random

class Effect:

    def __init__(self, name, duration, start, end, tick, stackable=False):
        self.name = name
        self.duration = duration
        self.start = start
        self.end = end
        self.tick = tick
        self.stackable = stackable
        self.count = 0 # count starts at zero then counts up to duration

    def startNotification(self, target):
        return self.name.capitalize() + " on " + target.the + " for " + str(self.duration) + " turns!"

    def endNotification(self, target):
        return self.name.capitalize() + " on " + target.the + " has ended!"

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

    def __init__(self, name, duration, amount, stackable=False):
        Effect.__init__(self, name, duration,
                lambda target: self.addHealth(target),
                lambda target: self.removeHealth(target),
                lambda target: None,
                stackable
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
        return self.name.capitalize() + ": " + target.the + "'s health is " + self.verb + " by " + output.formatNumber(abs(self.amount)) + " for " + str(self.duration) + " turns. " + target.the.capitalize() + "'s maximum health is now " + str(target.stats.health) + "."

# MULTIPLICATIVE BUFFS

class ArmorBuff(Effect):

    def __init__(self, name, duration, amount, stackable=False):
        Effect.__init__(self, name, duration,
                lambda target: target.stats.armor.mult(amount),
                lambda target: target.stats.armor.mult(-amount),
                lambda target: None,
                stackable
        )
        self.amount = amount
        self.verb = "increased" if self.amount > 0 else "reduced"

    def startNotification(self, target):
        return self.name.capitalize() + ": " + target.the + "'s armor is " + self.verb + " by " + output.formatNumber(abs(100 * self.amount)) + "% for " + str(self.duration) + " turns. " + target.the.capitalize() + "'s armor is now " + str(target.stats.armor) + "."

class StrengthBuff(Effect):

    def __init__(self, name, duration, amount, stackable=False):
        Effect.__init__(self, name, duration,
                lambda target: target.stats.strength.mult(amount),
                lambda target: target.stats.strength.mult(-amount),
                lambda target: None,
                stackable
        )
        self.amount = amount
        self.verb = "increased" if self.amount > 0 else "reduced"

    def startNotification(self, target):
        return self.name.capitalize() + ": " + target.the + "'s strength is " + self.verb + " by " + output.formatNumber(abs(100 * self.amount)) + "% for " + str(self.duration) + " turns. " + target.the.capitalize() + "'s strength is now " + str(target.stats.strength) + "."

class SpiritBuff(Effect):

    def __init__(self, name, duration, amount, stackable=False):
        Effect.__init__(self, name, duration,
                lambda target: target.stats.spirit.mult(amount),
                lambda target: target.stats.spirit.mult(-amount),
                lambda target: None,
                stackable
        )
        self.amount = amount
        self.verb = "increased" if self.amount > 0 else "reduced"

    def startNotification(self, target):
        return self.name.capitalize() + ": " + target.the + "'s spirit is " + self.verb + " by " + output.formatNumber(abs(100 * self.amount)) + "% for " + str(self.duration) + " turns. " + target.the.capitalize() + "'s spirit is now " + str(target.stats.spirit) + "."

class CriticalChanceBuff(Effect):

    def __init__(self, name, duration, amount, stackable=False):
        Effect.__init__(self, name, duration,
                lambda target: target.stats.criticalChance.mult(amount),
                lambda target: target.stats.criticalChance.mult(-amount),
                lambda target: None,
                stackable
        )
        self.amount = amount
        self.verb = "increased" if self.amount > 0 else "reduced"

    def startNotification(self, target):
        return self.name.capitalize() + ": " + target.the + "'s critical hit chance is " + self.verb + " by " + output.formatNumber(abs(100 * self.amount)) + "% for " + str(self.duration) + " turns. " + target.the.capitalize() + "'s critical hit chance is now " + target.stats.criticalChance.percent() + "%."

class CriticalStrikeBuff(Effect):

    def __init__(self, name, duration, amount, stackable=False):
        Effect.__init__(self, name, duration,
                lambda target: target.stats.criticalStrike.mult(amount),
                lambda target: target.stats.criticalStrike.mult(-amount),
                lambda target: None,
                stackable
        )
        self.amount = amount
        self.verb = "increased" if self.amount > 0 else "reduced"

    def startNotification(self, target):
        return self.name.capitalize() + ": " + target.the + "'s critical hit damage is " + self.verb + " by " + output.formatNumber(abs(100 * self.amount)) + "% for " + str(self.duration) + " turns. " + target.the.capitalize() + "'s critical hit damage is now " + str(target.stats.criticalStrike) + "."

class ArmorBuffAdd(Effect):

    def __init__(self, name, duration, amount, stackable=False):
        Effect.__init__(self, name, duration,
                lambda target: target.stats.armor.add(amount),
                lambda target: target.stats.armor.add(-amount),
                lambda target: None,
                stackable
        )
        self.amount = amount
        self.verb = "increased" if self.amount > 0 else "reduced"

    def startNotification(self, target):
        return self.name.capitalize() + ": " + target.the + "'s armor is " + self.verb + " by " + output.formatNumber(abs(self.amount)) + " for " + str(self.duration) + " turns. " + target.the.capitalize() + "'s armor is now " + str(target.stats.armor) + "."

class StrengthBuffAdd(Effect):

    def __init__(self, name, duration, amount, stackable=False):
        Effect.__init__(self, name, duration,
                lambda target: target.stats.strength.add(amount),
                lambda target: target.stats.strength.add(-amount),
                lambda target: None,
                stackable
        )
        self.amount = amount
        self.verb = "increased" if self.amount > 0 else "reduced"

    def startNotification(self, target):
        return self.name.capitalize() + ": " + target.the + "'s strength is " + self.verb + " by " + output.formatNumber(abs(self.amount)) + " for " + str(self.duration) + " turns. " + target.the.capitalize() + "'s strength is now " + str(target.stats.strength) + "."

class SpiritBuffAdd(Effect):

    def __init__(self, name, duration, amount, stackable=False):
        Effect.__init__(self, name, duration,
                lambda target: target.stats.spirit.add(amount),
                lambda target: target.stats.spirit.add(-amount),
                lambda target: None,
                stackable
        )
        self.amount = amount
        self.verb = "increased" if self.amount > 0 else "reduced"

    def startNotification(self, target):
        return self.name.capitalize() + ": the " + target.the + "'s spirit is " + self.verb + " by " + output.formatNumber(abs(self.amount)) + " for " + str(self.duration) + " turns. " + target.the.capitalize() + "'s spirit is now " + str(target.stats.spirit) + "."

class CriticalChanceBuffAdd(Effect):

    def __init__(self, name, duration, amount, stackable=False):
        Effect.__init__(self, name, duration,
                lambda target: target.stats.criticalChance.add(amount),
                lambda target: target.stats.criticalChance.add(-amount),
                lambda target: None,
                stackable
        )
        self.amount = amount
        self.verb = "increased" if self.amount > 0 else "reduced"

    def startNotification(self, target):
        return self.name.capitalize() + ": " + target.the + "'s critical hit chance is " + self.verb + " by " + output.formatNumber(abs(self.amount)) + " for " + str(self.duration) + " turns. " + target.the.capitalize() + "'s critical hit chance is now " + target.stats.criticalChance.percent() + "%."

class CriticalStrikeBuffAdd(Effect):

    def __init__(self, name, duration, amount, stackable=False):
        Effect.__init__(self, name, duration,
                lambda target: target.stats.criticalStrike.add(amount),
                lambda target: target.stats.criticalStrike.add(-amount),
                lambda target: None,
                stackable
        )
        self.amount = amount
        self.verb = "increased" if self.amount > 0 else "reduced"

    def startNotification(self, target):
        return self.name.capitalize() + ": " + target.the + "'s critical hit damage is " + self.verb + " by " + output.formatNumber(abs(self.amount)) + " for " + str(self.duration) + " turns. " + target.the.capitalize() + "'s critical hit damage is now " + str(target.stats.criticalStrike) + "."

# EFFECTS OVER TIME

class HealOverTime(Effect):

    def __init__(self, name, duration, lowerBound, upperBound, stackable=False):
        Effect.__init__(self, name, duration,
                lambda target: None,
                lambda target: None,
                lambda target: output.say(target.the.capitalize() + " recovers " + output.formatNumber(target.recoverHealth(lowerBound + random() * (upperBound - lowerBound))) + " health from " + self.name + "."),
                stackable
        )
        self.lowerBound = lowerBound
        self.upperBound = upperBound

    def startNotification(self, target):
        return self.name.capitalize() + ": " + target.the + " will recover between " + output.formatNumber(abs(self.lowerBound)) + " and " + output.formatNumber(abs(self.upperBound)) + " health for " + str(self.duration) + " turns."

class DamageOverTime(Effect):

    def __init__(self, name, duration, lowerBound, upperBound, stackable=False):
        Effect.__init__(self, name, duration,
                lambda target: None,
                lambda target: None,
                lambda target: output.say(target.the.capitalize() + " takes " + output.formatNumber(target.takeDamage(lowerBound + random() * (upperBound - lowerBound))) + " damage from " + self.name + "."),
                stackable
        )
        self.lowerBound = lowerBound
        self.upperBound = upperBound

    def startNotification(self, target):
        return self.name.capitalize() + ": " + target.the + " will take between " + output.formatNumber(abs(self.lowerBound)) + " and " + output.formatNumber(abs(self.upperBound)) + " damage for " + str(self.duration) + " turns."
