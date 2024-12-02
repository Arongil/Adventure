import copy
import game.output as output
import game.frequencyList as fList
import game.interaction as interaction
import game.item as item

class Loot(interaction.Interaction):

    def __init__(self, name, gold, experience, items = [], dropAll = False):
        interaction.Interaction.__init__(self) # the name of who gives the loot (monsters: "the wolf", "the ogre"; quest-givers: "Old Scar", "Timmy Fletcher")
        self.name = name
        self.gold = gold
        self.experience = experience
        self.items = fList.FrequencyList(items)
        self.dropAll = dropAll

    def dropItem(self, i):
        drop = copy.deepcopy(i)
        if not isinstance(drop, item.Nothing):
            self.player.inventory.addItem(drop)
            output.exclaim("You receive " + drop.name + " from " + self.name + ".")

    def start(self):
        if self.gold == 0 and self.experience == 0 and len(self.items) == 0:
            return
        # Output the gold and experience first because the player might level up after adding the experience.
        if self.gold != 0:
            output.declare("You collect " + str(self.gold) + " gold.")
        output.declare("You collect " + str(self.experience) + " experience.")
        self.player.inventory.addGold(self.gold)
        self.player.addExperience(self.experience)
        if len(self.items) > 0:
            if not self.dropAll:
                self.dropItem(self.items.getOption())
            else:
                allDrops = self.items.getAll()
                for i in allDrops:
                    self.dropItem(i)
