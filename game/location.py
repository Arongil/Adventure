import game.frequencyList as fList

class Location:

    def __init__(self, name, enter, leave, actions, interactions):
        self.name = name
        self.enter = enter # function
        self.leave = leave # function
        self.actions = actions
        self.interactions = fList.FrequencyList(interactions)
        self.taxi = None # the taxi often contains circular reference to other locations, so it's set outside of the constructor

    def __str__(self):
        return self.name

    def setTaxi(self, taxi):
        self.taxi = taxi

    def getInteraction(self):
        return self.interactions.getOption()

class Nowhere(Location):

    def __init__(self):
        Location.__init__(self, "nowhere", lambda: None, lambda: None, [], [])
