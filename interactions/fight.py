from random import random
import copy
import output
import interaction

class Fight(interaction.Interaction):

    def __init__(self, getMonster):
        interaction.Interaction.__init__(self)
        self.getMonster = getMonster

    def start(self):
        self.monster.reset() # the same instance of the monster may have already been fought
        output.bar()
        output.declare("You have been attacked by " + self.monster.a + "!")
        output.bar()

    def tick(self):
        output.say(self.player.inspect())
        output.say(self.monster.inspect())
        self.player.attack(self.monster)
        self.monster.attack(self.player)
        self.player.update()
        self.monster.update()
        output.separate()

    def end(self):
        if self.player.health > 0:
            output.declare("You have defeated " + self.monster.the + "!")
            self.monster.die()
            return False
        else:
            return True

    def exit(self):
        return self.player.health <= 0 or self.monster.health <= 0

    def activate(self):
        self.monster = self.getMonster()
        if self.monster == None:
            return "nothing" # abort if no monsters available
        self.start()
        while not self.exit():
            self.tick()
        return self.end()
