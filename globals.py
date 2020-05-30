import creatures.player
import location

player = creatures.player.Player(health=100, location=location.Nowhere())
def get_player():
    return player

##############
global debug
debug = False
##############
