import output
from random import random

class Effect:

    def __init__(self, name, duration, start, end, tick, stackable=False, notify=True):
        self.name = name
        self.duration = duration
        self.start = start
        self.end = end
        self.tick = tick
        self.stackable = stackable
        self.notify = notify
        self.count = 0 # count starts at zero then counts up to duration

    def startNotification(self, target):
        return self.name.capitalize() + " on " + target.the + " for " + str(self.duration) + " turns!"

    def endNotification(self, target):
        return self.name.capitalize() + " on " + target.the + " has ended!"

    def update(self, target):
        if self.count == 0:
            self.start(target)
            if self.notify:
                output.say(self.startNotification(target))
        elif self.count >= self.duration:
            self.end(target)
            target.effects.remove(self)
            if self.notify:
                output.say(self.endNotification(target))
            return
        self.tick(target)
        self.count = self.count + 1

# stat buffs

class HealthBuff(Effect):

    def __init__(self, name, duration, amount, stackable=False, notify=True):
        effect.__init__(self, name, duration,
                lambda target: self.addHealth(target),
                lambda target: self.removeHealth(target),
                lambda target: None,
                stackable,
                notify
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

    def __init__(self, name, duration, amount, stackable=False, notify=True):
        Effect.__init__(self, name, duration,
                lambda target: target.stats.armor.mult(amount),
                lambda target: target.stats.armor.mult(-amount),
                lambda target: None,
                stackable,
                notify
        )
        self.amount = amount
        self.verb = "increased" if self.amount > 0 else "reduced"

    def startNotification(self, target):
        return self.name.capitalize() + ": " + target.the + "'s armor is " + self.verb + " by " + output.formatNumber(abs(100 * self.amount)) + "% for " + str(self.duration) + " turns."

class StrengthBuff(Effect):

    def __init__(self, name, duration, amount, stackable=False, notify=True):
        Effect.__init__(self, name, duration,
                lambda target: target.stats.strength.mult(amount),
                lambda target: target.stats.strength.mult(-amount),
                lambda target: None,
                stackable,
                notify
        )
        self.amount = amount
        self.verb = "increased" if self.amount > 0 else "reduced"

    def startNotification(self, target):
        return self.name.capitalize() + ": " + target.the + "'s strength is " + self.verb + " by " + output.formatNumber(abs(100 * self.amount)) + "% for " + str(self.duration) + " turns."

class SpiritBuff(Effect):

    def __init__(self, name, duration, amount, stackable=False, notify=True):
        Effect.__init__(self, name, duration,
                lambda target: target.stats.spirit.mult(amount),
                lambda target: target.stats.spirit.mult(-amount),
                lambda target: None,
                stackable,
                notify
        )
        self.amount = amount
        self.verb = "increased" if self.amount > 0 else "reduced"

    def startNotification(self, target):
        return self.name.capitalize() + ": " + target.the + "'s spirit is " + self.verb + " by " + output.formatNumber(abs(100 * self.amount)) + "% for " + str(self.duration) + " turns."

class CriticalChanceBuff(Effect):

    def __init__(self, name, duration, amount, stackable=False, notify=True):
        Effect.__init__(self, name, duration,
                lambda target: target.stats.criticalChance.mult(amount),
                lambda target: target.stats.criticalChance.mult(-amount),
                lambda target: None,
                stackable,
                notify
        )
        self.amount = amount
        self.verb = "increased" if self.amount > 0 else "reduced"

    def startNotification(self, target):
        return self.name.capitalize() + ": " + target.the + "'s critical hit chance is " + self.verb + " by " + output.formatNumber(abs(100 * self.amount)) + "% for " + str(self.duration) + " turns."

class CriticalStrikeBuff(Effect):

    def __init__(self, name, duration, amount, stackable=False, notify=True):
        Effect.__init__(self, name, duration,
                lambda target: target.stats.criticalStrike.mult(amount),
                lambda target: target.stats.criticalStrike.mult(-amount),
                lambda target: None,
                stackable,
                notify
        )
        self.amount = amount
        self.verb = "increased" if self.amount > 0 else "reduced"

    def startNotification(self, target):
        return self.name.capitalize() + ": " + target.the + "'s critical hit damage is " + self.verb + " by " + output.formatNumber(abs(100 * self.amount)) + "% for " + str(self.duration) + " turns."

class DodgeBuff(Effect):

    def __init__(self, name, duration, amount, stackable=False, notify=True):
        Effect.__init__(self, name, duration,
                lambda target: target.stats.dodge.mult(amount),
                lambda target: target.stats.dodge.mult(-amount),
                lambda target: None,
                stackable,
                notify
        )
        self.amount = amount
        self.verb = "increased" if self.amount > 0 else "reduced"

    def startNotification(self, target):
        return self.name.capitalize() + ": " + target.the + "'s dodge chance is " + self.verb + " by " + output.formatNumber(abs(100 * self.amount)) + "% for " + str(self.duration) + " turns."

class ArmorBuffAdd(Effect):

    def __init__(self, name, duration, amount, stackable=False, notify=True):
        Effect.__init__(self, name, duration,
                lambda target: target.stats.armor.add(amount),
                lambda target: target.stats.armor.add(-amount),
                lambda target: None,
                stackable,
                notify
        )
        self.amount = amount
        self.verb = "increased" if self.amount > 0 else "reduced"

    def startNotification(self, target):
        return self.name.capitalize() + ": " + target.the + "'s armor is " + self.verb + " by " + output.formatNumber(abs(self.amount)) + " for " + str(self.duration) + " turns."

class StrengthBuffAdd(Effect):

    def __init__(self, name, duration, amount, stackable=False, notify=True):
        Effect.__init__(self, name, duration,
                lambda target: target.stats.strength.add(amount),
                lambda target: target.stats.strength.add(-amount),
                lambda target: None,
                stackable,
                notify
        )
        self.amount = amount
        self.verb = "increased" if self.amount > 0 else "reduced"

    def startNotification(self, target):
        return self.name.capitalize() + ": " + target.the + "'s strength is " + self.verb + " by " + output.formatNumber(abs(self.amount)) + " for " + str(self.duration) + " turns."

class SpiritBuffAdd(Effect):

    def __init__(self, name, duration, amount, stackable=False, notify=True):
        Effect.__init__(self, name, duration,
                lambda target: target.stats.spirit.add(amount),
                lambda target: target.stats.spirit.add(-amount),
                lambda target: None,
                stackable,
                notify
        )
        self.amount = amount
        self.verb = "increased" if self.amount > 0 else "reduced"

    def startNotification(self, target):
        return self.name.capitalize() + ": the " + target.the + "'s spirit is " + self.verb + " by " + output.formatNumber(abs(self.amount)) + " for " + str(self.duration) + " turns."

class CriticalChanceBuffAdd(Effect):

    def __init__(self, name, duration, amount, stackable=False, notify=True):
        Effect.__init__(self, name, duration,
                lambda target: target.stats.criticalChance.add(amount),
                lambda target: target.stats.criticalChance.add(-amount),
                lambda target: None,
                stackable,
                notify
        )
        self.amount = amount
        self.verb = "increased" if self.amount > 0 else "reduced"

    def startNotification(self, target):
        return self.name.capitalize() + ": " + target.the + "'s critical hit chance is " + self.verb + " by " + output.formatNumber(abs(self.amount)) + " for " + str(self.duration) + " turns."

class CriticalStrikeBuffAdd(Effect):

    def __init__(self, name, duration, amount, stackable=False, notify=True):
        Effect.__init__(self, name, duration,
                lambda target: target.stats.criticalStrike.add(amount),
                lambda target: target.stats.criticalStrike.add(-amount),
                lambda target: None,
                stackable,
                notify
        )
        self.amount = amount
        self.verb = "increased" if self.amount > 0 else "reduced"

    def startNotification(self, target):
        return self.name.capitalize() + ": " + target.the + "'s critical hit damage is " + self.verb + " by " + output.formatNumber(abs(self.amount)) + " for " + str(self.duration) + " turns."

class DodgeBuffAdd(Effect):

    def __init__(self, name, duration, amount, stackable=False, notify=True):
        Effect.__init__(self, name, duration,
                lambda target: target.stats.dodge.add(amount),
                lambda target: target.stats.dodge.add(-amount),
                lambda target: None,
                stackable,
                notify
        )
        self.amount = amount
        self.verb = "increased" if self.amount > 0 else "reduced"

    def startNotification(self, target):
        return self.name.capitalize() + ": " + target.the + "'s dodge chance is " + self.verb + " by " + output.formatNumber(abs(self.amount)) + " for " + str(self.duration) + " turns."

# EFFECTS OVER TIME

class HealOverTime(Effect):

    def __init__(self, name, duration, lowerBound, upperBound, stackable=False, notify=True):
        Effect.__init__(self, name, duration,
                lambda target: None,
                lambda target: None,
                lambda target: output.say(target.the.capitalize() + " recovers " + output.formatNumber(target.recoverHealth(lowerBound + random() * (upperBound - lowerBound))) + " health from " + self.name + "."),
                stackable,
                notify
        )
        self.lowerBound = lowerBound
        self.upperBound = upperBound

    def startNotification(self, target):
        return self.name.capitalize() + ": " + target.the + " will recover between " + output.formatNumber(abs(self.lowerBound)) + " and " + output.formatNumber(abs(self.upperBound)) + " health for " + str(self.duration) + " turns."

class DamageOverTime(Effect):

    # DoTs also need to know the caster so they can apply strength buffs, for example
    def __init__(self, name, duration, lowerBound, upperBound, caster, stackable=False, notify=True):
        Effect.__init__(self, name, duration,
                lambda target: None,
                lambda target: None,
                lambda target: output.say(target.the.capitalize() + " takes " + output.formatNumber(caster.dealDamage(target, lowerBound + random() * (upperBound - lowerBound), dodgeable=False)) + " damage from " + self.name + "."),
                stackable,
                notify
        )
        self.lowerBound = lowerBound
        self.upperBound = upperBound

    def startNotification(self, target):
        return self.name.capitalize() + ": " + target.the + " will take between " + output.formatNumber(abs(self.lowerBound)) + " and " + output.formatNumber(abs(self.upperBound)) + " base damage for " + str(self.duration) + " turns."
