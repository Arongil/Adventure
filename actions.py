from random import randint
import copy
import input
import output
import frequencyList as fList
import item
import interaction
import action

# Nothing is a null action; it does nothing.
class Nothing(action.Action):

    def __init__(self, name = "nothing"):
        action.Action.__init__(self, name, None)

class Quit(action.Action):

    def __init__(self, player):
        action.Action.__init__(self, "quit", player)

    def activate(self):
        output.say("Are you sure you want to quit?")
        if input.yesNo():
            self.player.alive = False
            output.exclaim("Thank you for playing!")

class Settings(action.Action):

    def __init__(self, player):
        action.Action.__init__(self, "settings", player)

    def activate(self):
        output.say("Toggle any of the following settings.")
        while True:
            option = input.inputFromOptions("option", ["back"] + list(self.player.settings), lambda setting: setting if setting == "back" else str(setting) + " = " + str(self.player.settings[setting]))
            if option == "back":
                break
            self.player.settings[option] = not self.player.settings[option]
            output.proclaim(str(option).capitalize() + " toggled to " + str(self.player.settings[option]) + ".")

class Stats(action.Action):

    def __init__(self, player):
        action.Action.__init__(self, "stats", player)

    def activate(self):
        output.proclaim("You are level " + str(self.player.level) + "" + (" with " + str(self.player.experience) + "/" + str(self.player.levelUpExperience[self.player.level - 1]) + " experience." if self.player.level < self.player.maxLevel else ", maximum level."))
        output.say("---------------- Stats ----------------")
        output.say(str(self.player.stats))
        output.say("---------------------------------------")

class Inventory(action.Action):

    def __init__(self, player):
        action.Action.__init__(self, "inventory", player)

    def activate(self):
        output.proclaim("")
        output.say("-------------- Inventory --------------")
        output.proclaim("You have " + str(self.player.inventory.gold) + " gold.\n")
        output.outputList(self.player.inventory.items, lambda i: str(i) + ": " + str(i.description))
        output.say("---------------------------------------")

class Taxi(action.Action):

    def __init__(self, player, greeting, locations):
        action.Action.__init__(self, "taxi", player)
        self.greeting = greeting # the message the player sees when they call the taxi
        self.locations = locations # locations is a 2D list with locations and prices (ex: [["The Silent Forest", 49], ["Fort Morning", 99]])

    def locationToString(self, location, cost):
        if location.name == self.player.location.name and cost == 0:
            return "back"
        return "Travel to " + str(location) + " for " + str(cost) + " gold."

    def activate(self):
        output.proclaim(self.greeting)
        if len(self.locations) == 0:
            return
        output.say("You have " + str(self.player.inventory.gold) + " gold.")
        location = input.inputFromOptions(self.name, self.locations, lambda location: self.locationToString(location[0], location[1]), lambda location: self.player.inventory.gold >= location[1], "Please select an option that you can afford.")
        if location[0].name != self.player.location.name:
            # If the player chooses to travel to a new location, move them and charge them.
            self.player.inventory.removeGold(location[1])
            self.player.changeLocation(location[0])

class NullTaxi(Taxi):

    def __init__(self, player):
        Taxi.__init__(self, player, "There is no taxi here.", [])

class Menu(action.Action):

    def __init__(self, player):
        action.Action.__init__(self, "menu", player)
        self.options = [
            Nothing("back"),
            Taxi(self.player, "", []),
            Stats(self.player),
            Inventory(self.player),
            Settings(self.player),
            Quit(self.player)
        ]

    def changeTaxi(self, taxi):
        for i in range(len(self.options)):
            if self.options[i].name == "taxi":
                self.options[i] = taxi
                return True
        return False

    def activate(self):
        input.inputFromOptions("menu", self.options).activate()

class Use(action.Action):

    def __init__(self, player):
        action.Action.__init__(self, "use", player)

    # define an update method and an onCooldown method so that Use can pass as an ability and an action
    def onCooldown(self):
        return False

    def update(self):
        pass

    def activate(self, optionalSecondArgument = None): # optionalSecondArgument is so Use can pass as an ability
        while True:
            use = input.inputFromOptions(self.name, ["back"] + self.player.inventory.getUsableItems())
            if use == "back":
                break
            use.activate(self.player)

class LevelBonus(action.Action):

    def __init__(self, player, abilities):
        action.Action.__init__(self, "bonus", player)
        # the stats offered and their associated bonuses
        self.stats = [
            self.player.stats.health,
            self.player.stats.armor,
            self.player.stats.strength,
            self.player.stats.spirit,
            self.player.stats.criticalChance,
            self.player.stats.criticalStrike
        ]
        self.bonuses = {
            "health": 5,
            "armor": 2,
            "strength": 2,
            "spirit": 2,
            "critical hit chance": 0.01,
            "critical hit damage": 0.2
        }
        self.abilities = abilities # array with abilities, descriptions, and level numbers for when to award them

    def activate(self):
        output.say("Which stat do you want to boost?")
        while True:
            stat = input.inputFromOptions(self.name, self.stats, lambda stat: stat.name + " by " + str(self.bonuses[stat.name]) + ", currently at " + str(stat) + ".")
            output.say("Are you sure you want to boost " + str(stat.name) + " by " + str(self.bonuses[stat.name]) + "?")
            if input.yesNo():
                stat.add(self.bonuses[stat.name])
                break
        if len(self.abilities) > 0 and self.player.level == self.abilities[0][2]: # check if level is correct
            output.exclaim("You learn a new ability: " + str(self.abilities[0][0]).upper() + "!")
            output.declare(self.abilities[0][1]) # skill description
            self.player.abilities.append(self.abilities[0][0])
            self.abilities.pop(0)

class RestHeal(action.Action):

    def __init__(self, player, lowerBound = 5, upperBound = 5):
        action.Action.__init__(self, "rest", player)
        self.lowerBound = lowerBound
        self.upperBound = upperBound

    def activate(self):
        amount = self.player.recoverHealth(randint(self.lowerBound, self.upperBound))
        if self.player.health == self.player.stats.health.getValue():
            output.declare("You are at full health after resting!")
        else:
            output.declare("You recover " + output.formatNumber(amount) + " health from resting. You now have " + output.formatNumber(self.player.health) + "/" + str(self.player.stats.health.getValue()) + " health.")
        # check player setting: auto-rest
        if self.player.settings["auto-rest"]:
            if self.player.health < self.player.stats.health.getValue():
                self.player.attemptAutoAct(self)

class ScavengeGold(action.Action):

    def __init__(self, player, lowerBound, upperBound):
        action.Action.__init__(self, "scavenge", player)
        self.lowerBound = lowerBound
        self.upperBound = upperBound

    def activate(self):
        amount = randint(self.lowerBound, self.upperBound)
        self.player.inventory.addGold(amount)
        if amount == 0:
            output.declare("You find nothing while scavenging.")
        else:
            output.declare("You find " + output.formatNumber(amount) + " gold while scavenging.")
        # check player setting: auto-scavenge
        if self.player.settings["auto-scavenge"]:
            self.player.attemptAutoAct(self)

class FindItem(action.Action):

    def __init__(self, player, message, items):
        action.Action.__init__(self, "find", player)
        self.message = message # function, takes item
        self.items = fList.FrequencyList(items)

    def activate(self):
        drop = copy.deepcopy(self.items.getOption())
        output.exclaim(self.message(drop))
        self.player.inventory.addItem(drop)

class OfferLocationChange(action.Action):

    def __init__(self, player, message, locations):
        action.Action.__init__(self, "go", player)
        self.message = message
        self.locations = locations

    def activate(self):
        output.proclaim(self.message)
        if len(self.locations) > 1:
            choice = input.inputFromOptions("go", ["stay"] + self.locations)
            if choice != "stay":
                self.player.changeLocation(choice)
        else:
            if input.yesNo():
                self.player.changeLocation(self.locations[0])

class Scavenge(action.Action):

    def __init__(self, player, interactions):
        action.Action.__init__(self, "scavenge", player)
        self.interactions = fList.FrequencyList(interactions)

    def activate(self):
        self.interactions.getOption().activate()

class Shop(action.Action):

    def __init__(self, player, shops):
        action.Action.__init__(self, "shop", player)
        self.shops = shops

    def activate(self):
        if len(self.shops) == 1:
            self.shops[0].activate()
        else:
            input.inputFromOptions("visit", self.shops).activate()

class Talk(action.Action):

    def __init__(self, player, npcs):
        action.Action.__init__(self, "talk", player)
        self.npcs = npcs

    def activate(self):
        choice = input.inputFromOptions("talk", ["back"] + self.npcs, lambda npc: npc if npc == "back" else str(npc.getName()))
        if choice == "back":
            return
        choice.activate()
