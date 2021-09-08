# Ryan and Pat's Spaceoids
# a comically terrible asteroids clone

from ObjectsInSpace import *
from menu import GameMenu
""""
Game is a class that has a "game" instance
Objects in Space is the wrapper for spaceships rocks and bullets


"""


# let's set up Pygame for the game
# initialize Pygame
pygame.init()

# let's set up the screen
pygame.display.set_caption("Space Rocks")

# let's set up the main screen
max_screen_x = 800
max_screen_y = 600
screen_size = (max_screen_x, max_screen_y)
screen = pygame.display.set_mode(screen_size)


# first we should instantiate a GameMenu object to control the game setup
main_menu = GameMenu(screen)
main_menu.mainloop(screen)

# close out pygame when all is done
pygame.quit()
