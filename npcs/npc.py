import globals
import input
import output

# The NPC stores three pieces of data. The name is the NPC's name. The opener is what the NPC says no matter what. Quests is an optional array that contains Quest objects. Example:
# name = "Barton the Grizzled"
# opener = "Traveller, I have struggled to find mushrooms as of late."
# quests = [Quest( ... ), Quest( ... ), ...]

class NPC:

    def __init__(self, name, opener, quests):
        self.name = name
        self.opener = opener
        self.quests = quests

    def getQuests(self):
        return [quest for quest in self.quests if quest.condition(globals.player)]

    def getName(self):
        return self.name if len(self.getQuests()) == 0 else self.name + " *"

    def activate(self):
        output.proclaim(self.name + ":")
        output.say(self.opener)

        quests = self.getQuests()
        if len(quests) == 0:
            return

        output.proclaim("Quests:")
        choice = input.inputFromOptions("quest", ["back"] + quests, lambda quest: quest if quest == "back" else str(quest.getName()))
        if choice == "back":
            return

        choice.activate()
