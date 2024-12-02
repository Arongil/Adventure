import game.output as output
import game.frequencyList as fList
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
        self.loot = loot
        self.abilities = fList.FrequencyList(abilities)
        self.unique = kwargs.get("unique") if "unique" in kwargs else False
        self.respawns = 1 if self.unique else -1
        self.isPlayer = False

    def specialReset(self):
        pass

    def reset(self):
        self.clearEffects()
        self.health = self.stats.health.getValue()
        for i in self.abilities:
            i.resetCooldown()
        self.specialReset()

    def canRespawn(self):
        return self.respawns == -1 or self.respawns > 0

    def inspect(self):
        return ("" if self.unique else "The " ) + self.name + " has " + output.formatNumber(self.health) + "/" + str(self.stats.health) + " health."

    def die(self):
        self.loot.activate()
        self.reset()
        if self.respawns > 0:
            self.respawns -= 1

    def attack(self, target):
        self.gear.proc(target)
        self.abilities.getOption(lambda ability: not ability.onCooldown()).activate(self, target)
