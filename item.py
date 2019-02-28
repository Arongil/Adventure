import globals

class Item:

    def __init__(self, name, description, sellCost, buyCost, number = 1, usable = False):
        self.name = name
        self.description = description
        self.number = number
        self.sellCost = sellCost # how much gold the item is worth when sold to a merchant
        self.buyCost = buyCost # how much gold the item costs when bought from a merchant
        self.usable = usable # whether or not the player can use the item, defaulted to False

    def __str__(self):
        return self.name + ("" if self.number == 1 else " (" + str(self.number) + "x)")

    def fullDescription(self):
        if self.description == "":
            return str(self)
        return self.name + (": " if self.number == 1 else " (" + str(self.number) + "x): ") + self.description

    def equals(self, item):
        return item.name == self.name and item.description == self.description and item.sellCost == self.sellCost and item.buyCost == self.buyCost and item.usable == self.usable

    # Check whether an item can stack with this and, if so, stack it. Return whether the operation was successful.
    def stack(self, item):
        if self.equals(item):
            self.number += item.number
            return True
        return False

    def remove(self, item, amount):
        if self.equals(item) and self.number >= amount:
            self.number -= amount
            return True
        return False

    def sell(self, creature, amount):
        # creature is the creature selling the item
        creature.addGold(self.sellCost * amount)
        creature.inventory.removeItem(self, amount)

    def buy(self, creature, amount):
        # creature is the creature buying the item
        if creature.inventory.removeGold(self.buyCost * amount):
            creature.inventory.addItem(self)
            return True
        return False

class UsableItem(Item):

    def __init__(self, name, description, sellCost, buyCost, use, number = 1):
        Item.__init__(self, name, description, sellCost, buyCost, number)
        self.usable = True
        self.use = use # function that takes the creature using the item

    def activate(self, user):
        user.inventory.removeItem(self)
        self.use(user)

class Nothing(Item):

    def __init__(self):
        Item.__init__(self, "nothing", "", 0, 0)
