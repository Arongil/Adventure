# The Interaction class describes any interaction the player has, be it with a monster, shrine, or shopkeeper. Every interaction has four components: the exit condition of the interaction, the logic for the start and end of the interaction, and the logic for every turn the interaction continues.
# A Fight interaction with a monster might take a monster as the object, set the exit condition to whether the player of the monster had health less or equal to zero, alert the player a fight has begun when starting, alert the fight has stopped when ending, and ask for the ability to use at each round of the fight.

import game.globals as globals

class Interaction:

    def __init__(self):
        self.player = globals.player

    def start(self):
        pass

    def tick(self):
        pass

    def end(self):
        pass

    def exit(self):
        return True

    def activate(self):
        self.start()
        while not self.exit():
            self.tick()
        self.end()
