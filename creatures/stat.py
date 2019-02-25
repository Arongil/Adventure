import output

class Stat:

    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.addition = 0
        self.multiplication = 1

    def __str__(self):
        return output.formatNumber(self.getValue())

    def getValue(self):
        return (self.value + self.addition) * self.multiplication

    def add(self, amount):
        self.addition += amount

    def mult(self, amount):
        self.multiplication += amount
