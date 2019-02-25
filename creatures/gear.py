import item

class Gear:

    def __init__(self, creature, **kwargs):
        self.creature = creature # the creature with the gear
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
    
    def equipSlot(self, slot, equipment):
        if not isinstance(self.slots[slot], EmptySlot):
            self.creature.inventory.addItem(self.slots[slot])
        self.slots[slot].unequip(self.creature)
        self.slots[slot] = equipment
        self.slots[slot].number = 1
        self.slots[slot].equip(self.creature)

    def equip(self, equipment):
        category = equipment.category
        if category == "weapon":
            self.equipSlot("weapon", equipment)
        elif category == "helmet":
            self.equipSlot("helmet", equipment)
        elif category == "chest":
            self.equipSlot("chest", equipment)
        elif category == "gloves":
            self.equipSlot("gloves", equipment)
        elif category == "legs":
            self.equipSlot("legs", equipment)
        elif category == "boots":
            self.equipSlot("boots", equipment)
        elif category == "ring":
            self.equipSlot("ring", equipment)
        elif category == "trinket":
            self.equipSlot("trinket", equipment)
        else:
            return False
        return True

# END OF GEAR

# START OF SPECIFIC TYPES OF GEAR

class Slot(item.UsableItem):

    def __init__(self, name, description, sellCost, buyCost, equip, unequip, category):
        item.UsableItem.__init__(self, name, description, sellCost, buyCost, lambda creature: creature.gear.equip(self))
        self.equip = equip # function that takes creature as a parameter
        self.unequip = unequip # function that takes creature as a parameter
        self.category = category

class EmptySlot(Slot):

    def __init__(self):
        Slot.__init__(self, "empty", "an empty slot", 0, 0, lambda creature: None, lambda creature: None, "empty slot")

class Weapon(Slot):

    def __init__(self, name, description, sellCost, buyCost, equip, unequip):
        Slot.__init__(self, name, description, sellCost, buyCost, equip, unequip, "weapon")

class Helmet(Slot):

    def __init__(self, name, description, sellCost, buyCost, equip, unequip):
        Slot.__init__(self, name, description, sellCost, buyCost, equip, unequip, "helmet")

class Chest(Slot):

    def __init__(self, name, description, sellCost, buyCost, equip, unequip):
        Slot.__init__(self, name, description, sellCost, buyCost, equip, unequip, "chest")

class Gloves(Slot):

    def __init__(self, name, description, sellCost, buyCost, equip, unequip):
        Slot.__init__(self, name, description, sellCost, buyCost, equip, unequip, "gloves")

class Legs(Slot):

    def __init__(self, name, description, sellCost, buyCost, equip, unequip):
        Slot.__init__(self, name, description, sellCost, buyCost, equip, unequip, "legs")

class Boots(Slot):

    def __init__(self, name, description, sellCost, buyCost, equip, unequip):
        Slot.__init__(self, name, description, sellCost, buyCost, equip, unequip, "boots")

class Ring(Slot):

    def __init__(self, name, description, sellCost, buyCost, equip, unequip):
        Slot.__init__(self, name, description, sellCost, buyCost, equip, unequip, "ring")

class Trinket(Slot):

    def __init__(self, name, description, sellCost, buyCost, equip, unequip):
        Slot.__init__(self, name, description, sellCost, buyCost, equip, unequip, "trinket")
