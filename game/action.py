# The Action class describes any action the player can take. Every Action has a name and FrequencyList of interactions it can cause. Examples of actions are scavenging (the interactions might be to get gold, to find an item, or to discover a shrine) and exploring (the interactions would be paths from the player's location to neighboring locations). In a town, an action might be to take a horse to a neighboring zone.

class Action:

    def __init__(self, name, player):
        self.name = name
        self.player = player

    def __str__(self):
        return self.name

    def activate(self):
        pass
