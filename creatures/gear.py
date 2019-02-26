import item

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

    def __init__(self, name, description, sellCost, buyCost, equip, unequip, category, proc):
        item.UsableItem.__init__(self, name, description, sellCost, buyCost, lambda creature: creature.gear.equip(self))
        self.equip = equip # function that takes creature as a parameter
        self.unequip = unequip # function that takes creature as a parameter
        self.category = category # type of equipment
        self.proc = proc # optional function that triggers special functionality (takes the wearer and the target)

class EmptySlot(Slot):

    def __init__(self):
        Slot.__init__(self, "empty", "an empty slot", 0, 0, lambda creature: None, lambda creature: None, "empty slot", lambda wearer, target: None)

class Weapon(Slot):

    def __init__(self, name, description, sellCost, buyCost, equip, unequip, proc = lambda wearer, target: None):
        Slot.__init__(self, name, description, sellCost, buyCost, equip, unequip, "weapon", proc)

class Helmet(Slot):

    def __init__(self, name, description, sellCost, buyCost, equip, unequip, proc = lambda wearer, target: None):
        Slot.__init__(self, name, description, sellCost, buyCost, equip, unequip, "helmet", proc)

class Chest(Slot):

    def __init__(self, name, description, sellCost, buyCost, equip, unequip, proc = lambda wearer, target: None):
        Slot.__init__(self, name, description, sellCost, buyCost, equip, unequip, "chest", proc)

class Gloves(Slot):

    def __init__(self, name, description, sellCost, buyCost, equip, unequip, proc = lambda wearer, target: None):
        Slot.__init__(self, name, description, sellCost, buyCost, equip, unequip, "gloves", proc)

class Legs(Slot):

    def __init__(self, name, description, sellCost, buyCost, equip, unequip, proc = lambda wearer, target: None):
        Slot.__init__(self, name, description, sellCost, buyCost, equip, unequip, "legs", proc)

class Boots(Slot):

    def __init__(self, name, description, sellCost, buyCost, equip, unequip, proc = lambda wearer, target: None):
        Slot.__init__(self, name, description, sellCost, buyCost, equip, unequip, "boots", proc)

class Ring(Slot):

    def __init__(self, name, description, sellCost, buyCost, equip, unequip, proc = lambda wearer, target: None):
        Slot.__init__(self, name, description, sellCost, buyCost, equip, unequip, "ring", proc)

class Trinket(Slot):

    def __init__(self, name, description, sellCost, buyCost, equip, unequip, proc = lambda wearer, target: None):
        Slot.__init__(self, name, description, sellCost, buyCost, equip, unequip, "trinket", proc)
