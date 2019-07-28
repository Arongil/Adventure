from random import random
import creatures.stats as stats
import creatures.gear as gear
import creatures.inventory as inventory

class Creature:

    def __init__(self, name, health, **kwargs):
        self.name = name
        self.health = health
        self.stats = stats.Stats(
            health,
            kwargs.get("armor") if "armor" in kwargs else 0,
            kwargs.get("strength") if "strength" in kwargs else 0,
            kwargs.get("spirit") if "spirit" in kwargs else 0,
            kwargs.get("criticalChance") if "criticalChance" in kwargs else 0.1,
            kwargs.get("criticalStrike") if "criticalStrike" in kwargs else 2
        )
        self.inventory = inventory.Inventory()
        self.gear = gear.Gear(self)
        self.abilities = None # FrequencyList or regular list of abilities that are used in combat
        self.effects = [] # list of effects (curses, blessings, etc.)
        self.unique = True # default is to be referred to as "the ..."

    def __str__(self):
        return self.name

    # output grammar: "an ogre attacks you" vs "Folloro attacks you" and "the wolf bites you" vs "Marmadon bites you"
    @property
    def a(self):
        return ("" if self.unique else ("an " if self.name[0].lower() in ["a", "e", "i", "o", "u"] else "a ")) + str(self)
    @property
    def the(self):
        return ("" if self.unique else "the ") + str(self)

    # returns whether the creature has any number of items in their inventory, and removes them if they do
    def checkAndRemove(self, itemName, number):
        return self.inventory.checkAndRemove(itemName, number)

    # returns the same as checkAndRemove, but doesn't remove
    def has(self, itemName, number):
        return self.inventory.has(itemName, number)

    def dealDamage(self, target, damage):
        amount = self.stats.damageDealt(damage)
        return target.takeDamage(amount)

    def takeDamage(self, damage):
        amount = self.stats.damageTaken(damage)
        self.health -= amount
        return amount

    def recoverHealth(self, health):
        amount = self.stats.healthRecovered(health)
        self.health += amount
        if self.health > self.stats.health.getValue():
            self.health = self.stats.health.getValue()
        return amount

    def addEffect(self, effect):
        self.effects.append(effect)

    def removeEffect(self, effect):
        self.effects.remove(effect)

    def updateEffects(self):
        for i in self.effects:
            i.update(self)

    def updateCooldowns(self):
        for i in self.abilities:
            i.update()

    def update(self):
        self.updateCooldowns()
        self.updateEffects()
