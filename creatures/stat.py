import output

class Stat:

    def __init__(self, name, value, base = 0):
        self.name = name
        self.value = value
        self.base = base
        self.addition = 0
        self.multiplication = 1
        self.difficultyModifier = 1

    def __str__(self):
        # use two decimals of precision for stats
        return output.formatNumber( ( (self.value + self.base + self.addition) * self.multiplication - self.base) * self.difficultyModifier, 2 )

    def percent(self):
        return output.formatNumber( ( (self.value + self.base + self.addition) * self.multiplication - self.base ) * 100 * self.difficultyModifier)

    def getValue(self):
        return (self.value + self.base + self.addition) * self.multiplication * self.difficultyModifier

    def add(self, amount):
        self.addition += amount

    def mult(self, amount):
        self.multiplication += amount
