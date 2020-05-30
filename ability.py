from random import random
import output

class Ability:

    def __init__(self, name, cooldown, cast, condition = lambda x: True):
        self.name = name
        self.cooldown = cooldown
        self.cooldownCount = 0
        self.cast = cast # cast is a function that takes a caster and a target then casts the ability on the target
        self.condition = condition # condition may return false, for example, when a rogue must be stealthed to perform a certain ability

    def __str__(self):
        turn = "turns" if self.cooldownCount != 1 else "turn"
        return self.name + (" is on cooldown for " + str(self.cooldownCount) + " " + turn if self.onCooldown() else "")

    def onCooldown(self):
        return not self.cooldownCount == 0

    def resetCooldown(self):
        self.cooldownCount = 0

    def updateCooldown(self):
        if self.onCooldown():
            self.cooldownCount -= 1

    def available(self, caster):
        return not self.onCooldown() and self.condition(caster)

    def update(self):
        self.updateCooldown()

    def activate(self, caster, target):
        if self.available(caster):
            self.cast(self, caster, target)
            self.cooldownCount = self.cooldown + 1

def damage(ability, caster, target, lowerBound, upperBound):
    amount = caster.dealDamage(target, lowerBound + random() * (upperBound - lowerBound))
    if amount != 0: # the enemy can dodge
        output.say("You deal " + output.formatNumber(amount) + " damage to " + target.the + " with " + ability.name + "!" if caster.isPlayer else "The " + str(caster) + " does " + output.formatNumber(amount) + " damage to you with " + ability.name + "!")

def heal(ability, caster, target, lowerBound, upperBound):
    amount = caster.recoverHealth(lowerBound + random() * (upperBound - lowerBound))
    output.say("You restore " + output.formatNumber(amount) + " health to yourself with " + ability.name + "." if caster.isPlayer else caster.the + " restores " + output.formatNumber(amount) + " health to itself with " + ability.name + ".")
