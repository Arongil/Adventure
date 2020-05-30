import output
import frequencyList as fList
import creatures.creature as creature

class Monster(creature.Creature):

    def __init__(self, name, health, loot, abilities, **kwargs):
        creature.Creature.__init__(self, name, health,
            armor = kwargs.get("armor") if "armor" in kwargs else 0,
            strength = kwargs.get("strength") if "strength" in kwargs else 0,
            spirit = kwargs.get("spirit") if "spirit" in kwargs else 0,
            criticalChance = kwargs.get("criticalChance") if "criticalChance" in kwargs else 0.1,
            criticalStrike = kwargs.get("criticalStrike") if "criticalStrike" in kwargs else 2
        )
        self.unique = kwargs.get("unique") if "unique" in kwargs else False
        self.loot = loot
        self.abilities = fList.FrequencyList(abilities)
        self.isPlayer = False

    def reset(self):
        self.effects = []
        self.health = self.stats.health.getValue()
        for i in self.abilities:
            i.resetCooldown()

    def inspect(self):
        return ("" if self.unique else "The " ) + self.name + " has " + output.formatNumber(self.health) + "/" + str(self.stats.health) + " health."

    def die(self):
        self.loot.activate()

    def attack(self, target):
        self.gear.proc(target)
        self.abilities.getOption(lambda ability: not ability.onCooldown()).activate(self, target)
