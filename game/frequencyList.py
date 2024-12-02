from random import random

class FrequencyList:

    def __init__(self, options = []):
        # options is a 2 by n array with the option and the chance: [["walk", 0.4], ["run", 0.6]]
        self.options = options
        # options are automatically normalized so the total probability is 1
        self.normalize()

    def __len__(self):
        return len(self.options)

    def __getitem__(self, index):
        return self.options[index][0]

    def normalize(self):
        total = sum(option[1] for option in self.options)
        for i in range(len(self.options)):
            self.options[i][1] /= total

    def add(self, option, chance, unique = False):
        self.options.append([option, chance, unique])
        self.normalize()

    def getAll(self):
        return [option[0] for option in self.options]

    # A condition may be provided that the output must satisfy.
    def getOption(self, condition = lambda option: True):
        impossible = [item[0] for item in self.options if not condition(item[0])]
        if len(impossible) == len(self.options):
            return None
        option = None
        r = random()
        for i in self.options: # sort out removing invalid options
            if i[0] in impossible:
                r -= i[1]
        for i in self.options:
            if i[0] in impossible:
                continue
            if r < i[1]:
                option = i
                break
            r -= i[1]
        # If a rounding error caused none to be picked, choose the first
        if option == None:
            option = self.options[0]
        # If there is a third element in option that is set to True, then this is a unique option.
        # After getting picked, it should be removed from the list.
        if len(option) == 3 and option[2]:
            self.options.remove(option)
            self.normalize()
        return option[0]
