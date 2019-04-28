import globals
import input
import output
import zones.morningFields as morningFields

class Game:

    def __init__(self):
        self.player = globals.player
        self.player.changeLocation(morningFields.traineeValley)
    
    def start(self):
        while self.player.alive:
            self.player.act()
            self.player.interact()
