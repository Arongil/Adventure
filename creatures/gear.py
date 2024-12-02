import game.item as item
import game.output as output

class Gear:

    def __init__(self, wearer, **kwargs):
        self.wearer = wearer # the creature with the gear
        self.slots = {
            "weapon": kwargs.get("weapon") if "weapon" in kwargs else EmptySlot(),
            "helmet": kwargs.get("helmet") if "helmet" in kwargs else EmptySlot(),
            "chest": kwargs.get("chest") if "chest" in kwargs else EmptySlot(),
            "gloves": kwargs.get("gloves") if "gloves" in kwargs else EmptySlot(),
            "legs": kwargs.get("legs") if "legs" in kwargs else EmptySlot(),
            "boots": kwargs.get("boots") if "boots" in kwargs else EmptySlot(),
            "ring": kwargs.get("ring") if "ring" in kwargs else EmptySlot(),
            "trinket": kwargs.get("trinket") if "trinket" in kwargs else EmptySlot()
        }

    def proc(self, target):
        # check for any slots having a proc
        for key in self.slots:
            self.slots[key].proc(self.wearer, target)

    def equipSlot(self, slot, equipment):
        if not isinstance(self.slots[slot], EmptySlot):
            self.wearer.inventory.addItem(self.slots[slot])
        self.slots[slot].unequip(self.wearer)
        self.slots[slot] = equipment
        self.slots[slot].number = 1
        self.slots[slot].equip(self.wearer)

    def equip(self, equipment):
        for key in self.slots:
            if equipment.category == key:
                self.equipSlot(key, equipment)
                return True
        return False

# END OF GEAR

# START OF SPECIFIC TYPES OF GEAR

class Slot(item.UsableItem):

    def __init__(self, name, description, sellCost, buyCost, stats, category, proc):
        item.UsableItem.__init__(self, name, description, sellCost, buyCost, lambda creature: creature.gear.equip(self))
        self.stats = stats
        self.category = category # type of equipment
        self.proc = proc # optional function that triggers special functionality (takes the wearer and the target)

        # add stats to the description (sorted alphabetically by stat name)
        for stat, value in sorted(self.stats.items(), key=lambda x: x[0]):
            self.description += "\n\t" + stat + (" +" if value > 0 else " -") + output.formatNumber(value, 2)

    def equip(self, wearer):
        for stat, value in self.stats.items():
            wearer.stats.add(**{stat: value})

    def unequip(self, wearer):
        for stat, value in self.stats.items():
            wearer.stats.add(**{stat: -value})

class EmptySlot(Slot):

    def __init__(self):
        Slot.__init__(self, "empty", "an empty slot", 0, 0, {}, "empty slot", lambda wearer, target: None)

class Weapon(Slot):

    def __init__(self, name, description, sellCost, buyCost, stats, proc = lambda wearer, target: None):
        Slot.__init__(self, name, description, sellCost, buyCost, stats, "weapon", proc)

class Helmet(Slot):

    def __init__(self, name, description, sellCost, buyCost, stats, proc = lambda wearer, target: None):
        Slot.__init__(self, name, description, sellCost, buyCost, stats, "helmet", proc)

class Chest(Slot):

    def __init__(self, name, description, sellCost, buyCost, stats, proc = lambda wearer, target: None):
        Slot.__init__(self, name, description, sellCost, buyCost, stats, "chest", proc)

class Gloves(Slot):

    def __init__(self, name, description, sellCost, buyCost, stats, proc = lambda wearer, target: None):
        Slot.__init__(self, name, description, sellCost, buyCost, stats, "gloves", proc)

class Legs(Slot):

    def __init__(self, name, description, sellCost, buyCost, stats, proc = lambda wearer, target: None):
        Slot.__init__(self, name, description, sellCost, buyCost, stats, "legs", proc)

class Boots(Slot):

    def __init__(self, name, description, sellCost, buyCost, stats, proc = lambda wearer, target: None):
        Slot.__init__(self, name, description, sellCost, buyCost, stats, "boots", proc)

class Ring(Slot):

    def __init__(self, name, description, sellCost, buyCost, stats, proc = lambda wearer, target: None):
        Slot.__init__(self, name, description, sellCost, buyCost, stats, "ring", proc)

class Trinket(Slot):

    def __init__(self, name, description, sellCost, buyCost, stats, proc = lambda wearer, target: None):
        Slot.__init__(self, name, description, sellCost, buyCost, stats, "trinket", proc)
