import globals
import input
import output
import zones.morningFields as morningFields

class Game:

    def __init__(self):
        self.player = globals.get_player()

    def initGame(self):
        # output.say("Start a new game or load an old one?")
        # choice = input.inputFromOptions("adventure", ["start", "load"])
        # if choice == "start":
            # self.player.init()
            # self.player.changeLocation(morningFields.traineeValley)
        # else:
            # output.say("Choose a game to load.")
            # save.load()

        self.player.init()
        self.player.changeLocation(morningFields.traineeValley)

    def start(self):
        self.initGame()
        while self.player.alive:
            self.player.act()
            self.player.interact()
