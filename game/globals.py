import creatures.player
import game.location as location

player = creatures.player.Player(health=100, location=location.Nowhere())
def get_player():
    return player
