from game import SpaceRocks
from ObjectsInSpace import *
from random import randint, choice

# instantiate a "game" object for the game
game = SpaceRocks()

print("Loading Objects!")
# let's initialize the objects to be used in the game object
for i in range(10):
    new_rock = SpaceBoulder()
    new_rock.rect.centerx = randint(0, game.max_screen_x)
    new_rock.rect.centery = randint(0, game.max_screen_y)
    new_rock.dx = randint(-3, 3)
    new_rock.dy = randint(-3, 3)
    new_rock.theta = randint(0, 360)
    new_rock.dtheta = choice([1, -1])  # degrees per tick
    new_rock.create_rotation_map()
    game.space_objects.add(new_rock)

# we've got the asteroids built, let's instantiate a "Player"
# we instantiate a "Player" here, stick them in the middle of the screen
player_ship = Player()
player_ship.health = 100
player_ship.rect.centerx = game.max_screen_x / 2
player_ship.rect.centery = game.max_screen_y / 2
player_ship.dtheta = 0
player_ship.create_rotation_map()
# it's a player ship, so we need to flag the ship as controllable
player_ship.is_controllable = True
game.space_objects.add(player_ship)  # finally add it to the space_objects


game.main_loop()
