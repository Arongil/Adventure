import output
import frequencyList as fList
import interaction
import item

class Loot(interaction.Interaction):

    def __init__(self, name, gold, experience, items = []):
        interaction.Interaction.__init__(self) # the name of who gives the loot (monsters: "the wolf", "the ogre"; quest-givers: "Old Scar", "Timmy Fletcher")
        self.name = name
        self.gold = gold
        self.experience = experience
        self.items = fList.FrequencyList(items)

    def start(self):
        if self.gold == 0 and self.experience == 0 and len(self.items) == 0:
            return
        # Output the gold and experience first because the player might level up after adding the experience.
        output.declare("You collect " + str(self.gold) + " gold.")
        output.declare("You collect " + str(self.experience) + " experience.")
        self.player.inventory.addGold(self.gold)
        self.player.addExperience(self.experience)
        if len(self.items) > 0:
            drop = self.items.getOption()
            if not isinstance(drop, item.Nothing):
                self.player.inventory.addItem(drop)
                output.exclaim("You receive " + drop.name + " from " + self.name + ".")
