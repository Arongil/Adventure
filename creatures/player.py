import input
import output
import frequencyList as fList
import creatures.creature as creature
import creatures.classes as classes
import ability
import actions
import effect

class Player(creature.Creature):

    def __init__(self, health, location):
        creature.Creature.__init__(self, "player", health)
        self.location = location # the player's actions derive from its location

        self.settings = {
            "auto-rest": True,
            "auto-scavenge": True,
            "instant-input": True
        }

        # baseActions are actions the player can always take.
        self.baseActions = [
            actions.Menu(self),
            actions.Use(self)
        ]
        self.actions = self.baseActions + self.location.actions
        self.levelBonus = actions.LevelBonus(self, [])
        self.abilities = [actions.Use(self)] # the player's abilities list is not a frequency list because the player chooses abilities

        self.states = {}
        self.classInspect = lambda: "" # additional combat information (ex. rogue could say "Stealthed" or mage could say "Mana 100/100")
        self.classUpdate = lambda: None
        self.combatUpdate = lambda: None

        self.completedQuests = {}

        # The player starts at level 1.
        self.levelUpExperience = [
            # 2  3    4    5    6    7     8     9     10
            100, 200, 400, 600, 800, 1000, 1200, 1400, 1700,
            # 11  12    13    14    15    16    17    18    19    20
            2000, 2300, 2600, 3000, 3400, 3800, 4200, 4600, 5000, 5400,
            # 21  22    23    24    25    26    27    28    29    30
            5800, 6200, 6600, 7000, 7500, 8000, 8500, 9000, 9500, 10000
        ]
        self.maxLevel = len(self.levelUpExperience) + 1
        self.experience = 0
        self.level = 1

        self.isPlayer = True
        self.unique = False
        self.alive = True

    def init(self):
        # initialize player's class (e.g. mage)
        output.say("What class do you want to play?")
        class_name = input.inputFromOptions("class", classes.get_classes())
        # base stats
        self.stats = classes.get_stats(class_name)
        self.health = self.stats.health.getValue()
        # abilities for level 1
        self.abilities = self.abilities + classes.get_abilities(class_name)
        # abilities for higher levels
        self.levelBonus.abilities = classes.get_levelBonus(class_name)
        # extra states (i.e. stealth or mana)
        self.states = classes.get_states(class_name)
        # extra inspect (i.e. "Stealthed" or "Mana 100/100")
        self.classInspect = classes.get_classInspect(class_name)
        # update at the end of each turn (i.e. set stealth to false or regen mana)
        self.classUpdate = classes.get_classUpdate(class_name)
        # update at the end of each turn of combat (i.e. regen mana for mage)
        self.combatUpdate = classes.get_combatUpdate(class_name)

        # get difficulty before outputting class info
        output.proclaim("What difficulty level do you want?")
        difficulty = input.inputFromOptions("difficulty", ["easy", "medium", "hard", "expert"])
        modifier = {"easy": 1.2, "medium": 1.0, "hard": 0.8, "expert": 0.5}[difficulty]
        self.stats.health.value *= modifier
        self.stats.strength.value *= modifier
        self.stats.armor.value *= modifier
        self.health = self.stats.health.getValue()

        # output class information
        output.proclaim(classes.get_classIntro(class_name))

    def updateActions(self):
        self.actions = self.baseActions + self.location.actions
        for i in self.actions:
            if i.name == "menu":
                i.changeTaxi(self.location.taxi)
                return True
        return False

    def hasCompleted(self, questName):
        return questName in self.completedQuests

    def getInteraction(self):
        if not self.alive:
            return actions.Nothing()
        return self.location.getInteraction()

    def act(self, action = None):
        if self.alive == False:
            return
        self.update()
        self.classUpdate(self)
        if action == None:
            input.inputFromOptions("turn", self.actions).activate()
        else:
            action.activate()

    def interact(self):
        if self.alive == False:
            return
        # Make sure the player is up to date.
        self.updateAttributes()
        interaction = self.getInteraction()
        if isinstance(interaction, actions.Nothing):
            output.bar()
            return False
        interaction.activate()
        # Make sure the player is up to date.
        self.updateAttributes()
        output.bar()
        return True

    # Call at the end of an action to attempt automatically taking another if there is no interaction.
    def attemptAutoAct(self, action):
        if self.interact(): # If there is an interaction that interrupts the action, cancel and recover.
            self.act()
        else: # Otherwise, execute the action.
            self.act(action)

    def changeLocation(self, newLocation):
        self.location.leave()
        self.location = newLocation
        self.location.enter()
        self.updateActions()

    def inspect(self):
        extra = self.classInspect(self)
        return "You have " + output.formatNumber(self.health) + "/" + str(self.stats.health) + " health." + (" -- " + extra.upper() + " --" if len(extra) > 0 else "")

    def updateAttributes(self):
        while self.level < self.maxLevel and self.experience >= self.levelUpExperience[self.level - 1]:
            self.levelUp()

    def addExperience(self, amount):
        if self.level < self.maxLevel:
            self.experience += amount

    def levelUp(self):
        self.experience -= self.levelUpExperience[self.level - 1]
        self.level += 1
        self.health = self.stats.health.getValue()
        output.proclaim("A gentle wind restores your health.")
        output.say("You leveled up to level " + str(self.level) + "!" + (" You need " + str(self.levelUpExperience[self.level - 1]) + " experience to level up again." if self.level < self.maxLevel else ""))
        self.levelBonus.activate()

    def die(self):
        self.alive = False
        output.bellow("You died. Game over.")
        gameOver = input.getInput("game over")
        # # # # # # # # # # # # # #
        if gameOver == "debug":
            self.alive = True
            self.health = 1
            return
        # # # # # # # # # # # # # #
        input.close()

    def attack(self, target):
        ability = input.inputFromOptions("attack", self.abilities, lambda ability: str(ability), lambda ability: ability.available(self), "That ability is not available right now.")
        output.separate()
        self.gear.proc(target)
        ability.activate(self, target)
        self.combatUpdate(self)
