import copy
import globals
import input
import output
import item

class Shop:

    def __init__(self, name, message, wares):
        self.player = globals.player
        self.name = name
        self.message = message
        self.wares = wares # list of items

    def __str__(self):
        return self.name

    def sell(self):
        if len(self.player.inventory.items) == 0:
            output.say("You don't have anything you can sell.")
            return
        while True:
            output.say("What do you want to sell? You have " + str(self.player.inventory.gold) + " gold.")
            choice = input.inputFromOptions("sell", ["back"] + self.player.inventory.items, lambda choice: "sell " + str(choice) + " for " + str(choice.sellCost) + " gold" + (" each" if choice.number > 1 else "") if isinstance(choice, item.Item) else str(choice))
            if choice == "back":
                break
            if choice.number == 1:
                self.player.inventory.removeItem(choice)
                self.player.inventory.addGold(choice.sellCost)
            else:
                output.say("How many do you want to sell?")
                number = input.getInt("amount", 1, choice.number)
                self.player.inventory.removeItem(choice, number)
                self.player.inventory.addGold(choice.sellCost * number)
            output.say("Now you have " + str(self.player.inventory.gold) + " gold.")

    def itemString(self, choice):
        return "buy " + str(choice) + " for " + str(choice.buyCost) + " gold" if isinstance(choice, item.Item) else str(choice)

    def itemValid(self, choice):
        return self.player.inventory.removeGold(choice.buyCost) if isinstance(choice, item.Item) else True

    def activate(self):
        output.proclaim(self.message)
        output.say("You have " + str(self.player.inventory.gold) + " gold.")
        while True:
            choice = input.inputFromOptions("buy", ["leave", "sell"] + self.wares, self.itemString, self.itemValid, "Please buy an item you can afford.")
            if choice == "leave":
                break
            elif choice == "sell":
                self.sell()
            else:
                self.player.inventory.addItem(copy.deepcopy(choice))
                output.say("Purchased " + str(choice) + " for " + str(choice.buyCost) + " gold!")
                output.say("Now you have " + str(self.player.inventory.gold) + " gold.")
