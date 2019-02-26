from random import random
import output
import creatures.stat as stat

class Stats:

    def __init__(self, health, armor, strength, spirit, criticalChance, criticalStrike):
        self.scale = 20 # Every scale points gained in a stat is equivalent to adding 1 in a formula.
        self.health = stat.Stat("health", health) # maximum health
        self.armor = stat.Stat("armor", armor) # reduces damage taken
        self.strength = stat.Stat("strength", strength) # increases damage done
        self.spirit = stat.Stat("spirit", spirit) # increases healing done
        self.criticalChance = stat.Stat("critical hit chance", criticalChance) # chance of critical strike
        self.criticalStrike = stat.Stat("critical hit damage", criticalStrike) # multiplies damage done by critical strikes

    def __str__(self):
        return output.formatNumber(self.health.getValue()) + " maximum health\n" + output.formatNumber(self.armor.getValue()) + " armor (reduces damage taken)\n" + output.formatNumber(self.strength.getValue()) + " strength (increases damage done)\n" + output.formatNumber(self.spirit.getValue()) + " spirit (increases healing done)\n" + output.formatNumber(self.criticalChance.getValue()*100) + "% chance of critical hits\n" + output.formatNumber(self.criticalStrike.getValue()*100) + "% damage done by critical hits"

    def add(self, **kwargs):
        self.health.add(kwargs.get("health") if "health" in kwargs else 0)
        self.armor.add(kwargs.get("armor") if "armor" in kwargs else 0)
        self.strength.add(kwargs.get("strength") if "strength" in kwargs else 0)
        self.spirit.add(kwargs.get("spirit") if "spirit" in kwargs else 0)
        self.criticalChance.add(kwargs.get("criticalChance") if "criticalChance" in kwargs else 0)
        self.criticalStrike.add(kwargs.get("criticalStrike") if "criticalStrike" in kwargs else 0)

    def mult(self, **kwargs):
        self.health.mult(kwargs.get("health") if "health" in kwargs else 0)
        self.armor.mult(kwargs.get("armor") if "armor" in kwargs else 0)
        self.strength.mult(kwargs.get("strength") if "strength" in kwargs else 0)
        self.spirit.mult(kwargs.get("spirit") if "spirit" in kwargs else 0)
        self.criticalChance.mult(kwargs.get("criticalChance") if "criticalChance" in kwargs else 0)
        self.criticalStrike.mult(kwargs.get("criticalStrike") if "criticalStrike" in kwargs else 0)

    # modify the damage done by an attack
    def damageDealt(self, damage):
        modifier = 1 + self.strength.getValue() / self.scale
        if random() < self.criticalChance.getValue():
            modifier = modifier * self.criticalStrike.getValue()
        return damage * modifier

    # modify the damage taken
    def damageTaken(self, hit):
        modifier = 1 / (1 + self.armor.getValue() / self.scale)
        return hit * modifier

    # modify the healing done by a heal
    def healthRecovered(self, health):
        modifier = 1 + self.spirit.getValue() / self.scale
        if random() < self.criticalChance.getValue():
            modifier = modifier * self.criticalStrike.getValue()
        return health * modifier