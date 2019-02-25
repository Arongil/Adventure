from random import random
import output
import interaction

class Fight(interaction.Interaction):

    def __init__(self, getMonster): # other is a function that will return a monster
        interaction.Interaction.__init__(self)
        self.getMonster = getMonster

    def start(self):
        self.monster = self.getMonster()
        self.monster.reset() # reset the monster's stats (it may have been fought before, as only one instance of each monster is used)
        output.bar()
        output.declare("You have been attacked by " + ("" if self.monster.unique else "a ") + str(self.monster) + "!")
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
            output.declare("You have defeated " + ("" if self.monster.unique else "the ") + str(self.monster) + "!")
            self.monster.die()
        else:
            self.player.die()
    
    def exit(self):
        return self.player.health <= 0 or self.monster.health <= 0
