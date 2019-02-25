import output
import effect
import item

class HealthPotion(item.UsableItem):

    def __init__(self, name, description, sellCost, buyCost, amount):
        item.UsableItem.__init__(self, name, description, sellCost, buyCost, lambda target: self.drink(target))
        self.amount = amount

    def drink(self, target):
        target.health += self.amount # bypass armor because steel can't stop potions
        if target.health > target.stats.health.getValue():
            target.health = target.stats.health.getValue()
        if self.amount > 0:
            output.proclaim("The " + str(target) + " recovers " + str(self.amount) + " health after drinking " + self.name + ". You now have " + output.formatNumber(target.health) + "/" + str(target.stats.health.getValue()) + " health.")
        elif self.amount < 0:
            output.proclaim("The " + str(target) + " is drained " + str(self.amount) + " health after drinking " + self.name + ". You now have " + output.formatNumber(target.health) + "/" + str(target.stats.health.getValue()) + " health.")
