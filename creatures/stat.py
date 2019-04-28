import output

class Stat:

    def __init__(self, name, value, base = 0):
        self.name = name
        self.value = value
        self.base = base
        self.addition = 0
        self.multiplication = 1

    def __str__(self):
        return output.formatNumber( (self.value + self.base + self.addition) * self.multiplication - self.base )

    def percent(self):
        return output.formatNumber( ( (self.value + self.base + self.addition) * self.multiplication - self.base ) * 100 )

    def getValue(self):
        return (self.value + self.base + self.addition) * self.multiplication

    def add(self, amount):
        self.addition += amount

    def mult(self, amount):
        self.multiplication += amount
