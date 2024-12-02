import game.globals as globals
import game.input as input
import game.output as output

# Quest holds all the information to give and complete an arbitrary quest in game.
# openerText is the quest description when an NPC first offers it.
# incompleteText is the dialogue for if the player returns to the NPC before completing the quest.
# completeText is the dialogue for when the player returns to the NPC and has completed the quest.
# completionCheck is a function that determines whether the player has completed the quest. If the quest involves collecting items, then this must also delete the items from the player's inventory if the completion succeeds (use creature.checkAndRemove(itemName, number)).
# rewards is a function that gives the player the rewards promised.
# condition is a loot object.
# given is a boolean that stores whether the player has accepted the quest yet
# autoGive is a boolean that tells the quest whether to automatically jump to given = True if the condition is met. We can't just set given equal to True, because that could mess up future checks on whether the quest is in the players quest log etc.

# Once the player completes the quest, we run completionCheck = lambda: False. That way, the player never sees completed quests again.

class Quest:

    def __init__(self, name, openerText, incompleteText, completeText, completionCheck, rewards, condition = lambda player: True, autoGive = False):
        self.name = name
        self.openerText = openerText
        self.incompleteText = incompleteText
        self.completeText = completeText
        self.completionCheck = completionCheck
        self.rewards = rewards
        self.condition = condition

        self.given = False
        self.autoGive = autoGive

    def getName(self):
        return self.name if not self.given else self.name + " (in progress)"

    def activate(self):
        output.proclaim("-- " + self.name + " --")

        if self.autoGive:
            self.given = True

        if not self.given:
            output.proclaim(self.openerText)
            while True:
                choice = input.inputFromOptions("quest", ["decline", "accept"])
                if choice == "accept":
                    self.given = True
                    break
                elif choice == "decline":
                    output.say("Are you sure you want to decline the quest?")
                    if input.yesNo():
                        break
            return


        player = globals.get_player()
        if self.completionCheck(player):
            output.proclaim(self.completeText)
            output.exclaim("You have completed the quest " + self.name + "!")
            self.rewards.activate()
            self.condition = lambda player: False
            player.completedQuests[self.name] = True
        else:
            output.proclaim(self.incompleteText)
