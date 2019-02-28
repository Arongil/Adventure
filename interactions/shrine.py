import input
import output
import frequencyList as fList
import interaction
import effect

class Shrine(interaction.Interaction):

    def __init__(self, use):
        interaction.Interaction.__init__(self)
        self.use = use # function
        self.mysteryWords = fList.FrequencyList([["a mysterious", 0.2], ["a strange", 0.2], ["an odd", 0.2], ["a peculiar", 0.2], ["an eerie", 0.2]])
        self.shrineAdjectives = fList.FrequencyList([["brown", 0.1], ["gray", 0.1], ["broken", 0.1], ["cracked", 0.1], ["sunken", 0.1], ["broken", 0.1], ["stone", 0.1], ["chiseled", 0.1], ["short", 0.1], ["tall", 0.1]])
        self.shrineNouns = fList.FrequencyList([["pillar", 0.2], ["obelisk", 0.2], ["monolith", 0.2], ["shrine", 0.2], ["altar", 0.2]])
        self.nearWords = fList.FrequencyList([["a copse of dead trees", 0.2], ["a small hill", 0.2], ["a small cave", 0.2], ["a murky pond", 0.2], ["a faded signpost", 0.2]])

    def start(self):
        output.proclaim("You stumble upon " + self.mysteryWords.getOption() + " " + self.shrineAdjectives.getOption() + " " + self.shrineNouns.getOption() + " near " + self.nearWords.getOption() + ".")
        self.use()

class StatShrine(Shrine):

    def __init__(self, amounts, duration):
        Shrine.__init__(self, self.addBonus)
        self.amounts = amounts # amounts is an array of numbers [health, armor, strength, spirit, criticalChance, criticalStrike]
        self.duration = duration
        self.stats = [
            self.player.stats.health,
            self.player.stats.armor,
            self.player.stats.strength,
            self.player.stats.spirit,
            self.player.stats.criticalChance,
            self.player.stats.criticalStrike
        ]
        self.buffs = [
            effect.HealthBuff,
            effect.ArmorBuffAdd,
            effect.StrengthBuffAdd,
            effect.SpiritBuffAdd,
            effect.CriticalChanceBuffAdd,
            effect.CriticalStrikeBuffAdd
        ]

    def addBonus(self):
        output.say("Which stat do you want to boost for " + str(self.duration) + " turns?")
        while True:
            stat = input.inputFromOptions("shrine", self.stats, lambda stat: stat.name + " by " + str(self.amounts[self.stats.index(stat)]) + ", currently at " + str(stat.getValue()) + ".")
            index = self.stats.index(stat)
            output.say("Are you sure you want to boost " + stat.name + " by " + str(self.amounts[index]) + " for " + str(self.duration) + " turns?")
            if input.yesNo():
                self.player.addEffect( self.buffs[index]("shrine bonus", self.duration, self.amounts[index]) )
                return
