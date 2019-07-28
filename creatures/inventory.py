class Inventory:

    def __init__(self, gold = 0, items = []):
        self.gold = gold
        self.items = items

    def __str__(self):
        itemStrings = [str(self.gold) + " gold"]
        for i in self.items:
            itemStrings.append(str(i))
        return '\n'.join(itemStrings)

    def checkAndRemove(self, name, number):
        for item in self.items:
            if item.name.lower() == name.lower() and item.number >= number:
                item.number -= number
                if item.number == 0:
                    self.items.remove(item)
                return True
        return False

    def has(self, name, number):
        for item in self.items:
            if item.name.lower() == name.lower() and item.number >= number:
                return True
        return False

    def getUsableItems(self):
        usableItems = []
        for i in self.items:
            if i.usable:
                usableItems.append(i)
        return usableItems

    def addGold(self, amount):
        self.gold += amount

    def removeGold(self, amount):
        if self.gold < amount:
            return False
        self.gold -= amount
        return True

    def addItem(self, item):
        for i in self.items:
            if i.stack(item):
                return
        self.items.append(item)

    def removeItem(self, item, amount = 1):
        for i in self.items:
            if i.remove(item, amount):
                if i.number == 0:
                    self.items.remove(i)
                return True
        return False
