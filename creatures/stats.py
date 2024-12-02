from random import random
import game.output as output
import creatures.stat as stat

class Stats:

    def __init__(self, health, armor, strength, spirit, criticalChance, criticalStrike, dodge):
        self.scale = 20 # Every scale points gained in a stat is equivalent to adding 1 in a formula.
        self.health = stat.Stat("health", health) # maximum health
        self.armor = stat.Stat("armor", armor, self.scale) # reduces damage taken
        self.strength = stat.Stat("strength", strength, self.scale) # increases damage done
        self.spirit = stat.Stat("spirit", spirit, self.scale) # increases healing done
        self.criticalChance = stat.Stat("critical hit chance", criticalChance) # chance of critical strike
        self.criticalStrike = stat.Stat("critical hit damage", criticalStrike) # multiplies damage done by critical strikes
        self.dodge = stat.Stat("dodge", dodge) # chance of dodging incoming damage

    def __str__(self):
        return str(self.health) + " maximum health\n" + str(self.armor) + " armor (reduces damage taken)\n" + str(self.strength) + " strength (increases damage done)\n" + str(self.spirit) + " spirit (increases healing done)\n" + self.criticalChance.percent() + "% chance of critical hits\n" + self.criticalStrike.percent() + "% damage done by critical hits\n" + self.dodge.percent() + "% chance of dodge"

    def getStats(self):
        return [
            self.health,
            self.armor,
            self.strength,
            self.spirit,
            self.criticalChance,
            self.criticalStrike,
            self.dodge
        ]

    def add(self, **kwargs):
        self.health.add(kwargs.get("health") if "health" in kwargs else 0)
        self.armor.add(kwargs.get("armor") if "armor" in kwargs else 0)
        self.strength.add(kwargs.get("strength") if "strength" in kwargs else 0)
        self.spirit.add(kwargs.get("spirit") if "spirit" in kwargs else 0)
        self.criticalChance.add(kwargs.get("criticalChance") if "criticalChance" in kwargs else 0)
        self.criticalStrike.add(kwargs.get("criticalStrike") if "criticalStrike" in kwargs else 0)
        self.dodge.add(kwargs.get("dodge") if "dodge" in kwargs else 0)

    def mult(self, **kwargs):
        self.health.mult(kwargs.get("health") if "health" in kwargs else 0)
        self.armor.mult(kwargs.get("armor") if "armor" in kwargs else 0)
        self.strength.mult(kwargs.get("strength") if "strength" in kwargs else 0)
        self.spirit.mult(kwargs.get("spirit") if "spirit" in kwargs else 0)
        self.criticalChance.mult(kwargs.get("criticalChance") if "criticalChance" in kwargs else 0)
        self.dodge.mult(kwargs.get("dodge") if "dodge" in kwargs else 0)

    # modify the damage done by an attack
    def damageDealt(self, damage):
        modifier = self.strength.getValue() / self.scale
        if random() < self.criticalChance.getValue():
            modifier = modifier * self.criticalStrike.getValue()
        return damage * modifier

    # modify the damage taken
    def damageTaken(self, hit):
        modifier = 1 / (self.armor.getValue() / self.scale)
        return hit * modifier

    # modify the healing done by a heal
    def healthRecovered(self, health):
        modifier = self.spirit.getValue() / self.scale
        if random() < self.criticalChance.getValue():
            modifier = modifier * self.criticalStrike.getValue()
        return health * modifier
