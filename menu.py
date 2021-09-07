"""Pygame Menu Interface
docs available at:
https://pygame-menu.readthedocs.io/en/4.1.3/

for RP-Spaceoids

I started to "roll my own" menu functionality, then I realized, hey, this is Python
there's got to be a library for that!  Seriously, why on God's Green Earth are we
attempting to reinvent the wheel here.  So, I looked up the "pygame-menu" module
and found the docs.

This menu is designed to create A "SpaceRocks" object - or, a "game" object.
The idea is that you can customize the game before playing.

It is likely that we'll need to refactor the SpaceRocks code to quantify precisely "how"
all the pieces are going to fit together in the final iteration, but using this library
will dramatically simplify the process by which the game is customized
"""

import pygame
import pygame_menu
from game import SpaceRocks


class GameMenu(pygame_menu.Menu):
    """
    This menu class controls the instantiation of new "SpaceRocks" Objects.
    An individual game can be created through the interface here.  Ultimately,
    run the functions "create_singleplayer_game" or "create_multiplayer_game" to
    generate a game of that sort.
    """

    def __init__(self,title="Main menu!", width=600, height=500):
        """
        initialize the menu witht he following params

        width
        height

        these params are tweakable, but the default is "600x500"
        """

        pygame.init()

        # let's set up the screen
        # ::REFACTOR:: we need to refactor this to separate game screens from games or menus

        pygame.display.set_caption("Space Rocks")
        super().__init__(title=title,
                         width=width,
                         height=height,
                         theme=pygame_menu.themes.THEME_BLUE)
        # screen size for convenience during initialization
        self.max_screen_x = 800
        self.max_screen_y = 600

        screen_size = (self.max_screen_x, self.max_screen_y)
        self.screen = pygame.display.set_mode(screen_size)

        self. name = self.add.text_input("Name : ",
                                        default="Ryan The Magnificent!")

        self.add.selector("Number of Rocks :",
                          [(str(i), i) for i in range(1,20)]
                          )

        self.add.button("Create Singleplayer Game")
        self.add.button("Create Multiplayer Game")
        self.add.button("High Scores!")
        self.add.button("Quit", pygame_menu.events.EXIT)  # close the menu



    def create_singleplayer_game(self):
        """
        this function will return a single player instance of a SpaceRocks game
        using the data entered in the menu
        """
        pass

    def create_multiplayer_game(self):
        """
        this function will return a multi player instance of a SpaceRocks game
        using the data entered in the menu
        """
        pass

    def __del__(self):
        """
        ::REFACTOR::
        we need to refactor this along with the screen instantiation
        :return:
        """
        # when the object is deleted, kill Pygame
        pygame.quit()
