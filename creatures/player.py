import input
import output
import frequencyList as fList
import creatures.creature as creature
import ability
import actions
import effect

class Player(creature.Creature):

    def __init__(self, health, location):
        creature.Creature.__init__(self, "player", health)
        self.location = location # the player's actions derive from its location

        # baseActions are actions the player can always take.
        self.baseActions = [
            actions.Menu(self),
            actions.Use(self)
        ]
        self.actions = self.baseActions + self.location.actions
        self.levelBonus = actions.LevelBonus(self, [
            # name, cooldown, caster (always self), cast logic (takes ablty, which means ability but can't be confused with the module, and target)
            [ability.Ability("fireball", 2, self, lambda ablty, target: ability.damage(ablty, target, 10, 20)), "Fireball burns the enemy between 10 and 20 base damage.", 3],
            [ability.Ability("iron heart", 20, self, lambda ablty, target: ablty.caster.addEffect( effect.ArmorBuff("iron heart", 4, 1) )), "Iron heart strengthens your resolve, halving the damage you take for four turns.", 8],
            [ability.Ability("frenzy", 20, self, lambda ablty, target: ablty.caster.addEffect( effect.StrengthBuff("frenzy", 6, 0.4) )), "Frenzy makes you wild and powerful, increasing the damage you deal by 40% for six turns.", 15]
        ])
        self.abilities = [
            actions.Use(self),
            # name, cooldown, caster (always self), cast logic (takes ablty, which means ability but can't be confused with the module, and target)
            ability.Ability("punch", 0, self, lambda ablty, target: ability.damage(ablty, target, 5, 15))
        ] # the player's abilities list is not a frequency list because it chooses abilities

        # The player starts at level 1.
        self.levelUpExperience = [
            # 2  3    4    5    6    7     8     9     10
            100, 200, 400, 600, 800, 1000, 1200, 1400, 1700,
            # 11  12    13    14    15    16    17    18    19    20
            2000, 2300, 2600, 3000, 3400, 3800, 4200, 4600, 5000, 5400,
            # 21  22    23    24    25    26    27    28    29    30
            5800, 6200, 6600, 7000, 7500, 8000, 8500, 9000, 9500, 10000
        ]
        self.maxLevel = len(self.levelUpExperience) + 1
        self.experience = 0
        self.level = 1

        self.isPlayer = True
        self.unique = False
        self.alive = True

    def updateActions(self):
        self.actions = self.baseActions + self.location.actions
        for i in self.actions:
            if i.name == "menu":
                i.changeTaxi(self.location.taxi)
                return True
        return False
    
    def getInteraction(self):
        if not self.alive:
            return actions.Nothing()
        return self.location.getInteraction()

    def changeLocation(self, newLocation):
        self.location.leave()
        self.location = newLocation
        self.location.enter()
        self.updateActions()

    def inspect(self):
        return "You have " + output.formatNumber(self.health) + "/" + str(self.stats.health) + " health."

    def addExperience(self, amount):
        if self.level < self.maxLevel:
            self.experience += amount
            while self.level < self.maxLevel and self.experience >= self.levelUpExperience[self.level - 1]:
                self.levelUp()

    def levelUp(self):
        self.experience -= self.levelUpExperience[self.level - 1]
        self.level += 1
        self.health = self.stats.health.getValue()
        output.proclaim("A gentle wind restores your health.")
        output.say("You leveled up to level " + str(self.level) + "!" + (" You need " + str(self.levelUpExperience[self.level - 1]) + " experience to level up again." if self.level < self.maxLevel else ""))
        self.levelBonus.activate()

    def die(self):
        self.alive = False
        output.bellow("You died. Game over.")

    def attack(self, target):
        ability = input.inputFromOptions("attack", self.abilities, lambda ability: str(ability), lambda ability: not ability.onCooldown(), "Please select an ability that isn't on cooldown.")
        output.separate()
        self.gear.proc(target)
        ability.activate(target)
