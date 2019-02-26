from random import random
import output

class Ability:

    def __init__(self, name, cooldown, caster, cast):
        self.name = name
        self.cooldown = cooldown
        self.cooldownCount = 0
        self.caster = caster
        self.cast = cast # cast is a function that takes a caster and a target then casts the ability on the target

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

    def update(self):
        self.updateCooldown()

    def activate(self, target):
        if not self.onCooldown():
            self.cast(self, target)
            self.cooldownCount = self.cooldown + 1

def damage(ability, target, lowerBound, upperBound):
    amount = ability.caster.dealDamage(target, lowerBound + random() * (upperBound - lowerBound))
    output.say("You deal " + output.formatNumber(amount) + " damage to " + target.the + " with " + ability.name + "!" if ability.caster.isPlayer else "The " + str(ability.caster) + " does " + output.formatNumber(amount) + " damage to you with " + ability.name + "!")

def heal(ability, target, lowerBound, upperBound):
    amount = ability.caster.recoverHealth(lowerBound + random() * (upperBound - lowerBound))
    output.say("You restore " + output.formatNumber(amount) + " health to yourself with " + ability.name + "." if ability.caster.isPlayer else ability.caster.the + " restores " + output.formatNumber(amount) + " health to itself with " + ability.name + ".")
