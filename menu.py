"""Pygame Menu Interface
docs available at:
https://pygame-menu.readthedocs.io/en/4.1.3/

for RP-Spaceoids

I started to "roll my own" menu functionality, then I realized, hey, this is Python
there's got to be a library for that!  Seriously, why on God's Green Earth are we
attempting to reinvent the wheel here.  So, I looked up the "pygame-menu" module
and found the docs.

This menu is designed to create A "Game" object - or, a "game" object.
The idea is that you can customize the game before playing.

It is likely that we'll need to refactor the Game code to quantify precisely "how"
all the pieces are going to fit together in the final iteration, but using this library
will dramatically simplify the process by which the game is customized
"""

import pygame
import pygame_menu
from game import *
from random import randint, choice
import pickle


def create_singleplayer_game(number_of_space_rocks: int,
                             screen: pygame.surface,
                             difficulty: int = 2) -> Game:
    game = Game(screen)

    # we instantiate a "Player" here, stick them in the middle of the screen
    player_ship = Player()
    player_ship.health = 100
    # let's place the player in the middle of the game screen
    player_ship.rect.centerx = game.max_screen_x / 2
    player_ship.rect.centery = game.max_screen_y / 2
    player_ship.dtheta = 0
    player_ship.create_rotation_map()
    # it's a player ship, so we need to flag the ship as controllable
    player_ship.is_controllable = True
    game.space_objects.add(player_ship)  # finally add it to the space_objects

    """
    now let's draw the asteroids making sure that none of them overlap with the player ship
    at start up but they're still randomly distributed in the frame
    
    we'll do this by plotting them randomly on the screen, then if they overlap
    plotting them again
    """
    rocks_to_add = number_of_space_rocks
    while rocks_to_add >= 0:
        new_rock = SpaceBoulder()
        new_rock.rect.centerx = randint(0, screen.get_width())
        new_rock.rect.centery = randint(0, screen.get_height())
        new_rock.dx = randint(-difficulty, difficulty)
        new_rock.dy = randint(-difficulty, difficulty)

        new_rock.theta = randint(0, 360)
        new_rock.dtheta = choice([1, -1])
        new_rock.create_rotation_map()

        # check to see if the rock collides with the player, if so loop again
        collides = pygame.sprite.collide_rect(player_ship, new_rock)
        if collides:
            continue
        else:
            # otherwise add this rock to the sprite group
            game.space_objects.add(new_rock)
            rocks_to_add = rocks_to_add - 1

    return game


class GameMenu(pygame_menu.Menu):
    """
    This menu class controls the instantiation of new "Game" Objects.
    An individual game can be created through the interface here.  Ultimately,
    run the functions "create_singleplayer_game" or "create_multiplayer_game" to
    generate a game of that sort.
    """

    def __init__(self, screen: pygame.surface, title="Main menu!"):
        """
        initialize the menu witht he following params

        width
        height

        these params are tweakable, but the default is "600x500"
        """

        # let's set up the screen
        width = screen.get_width()
        height = screen.get_height()
        self.screen = screen

        super().__init__(title=title,
                         width=width,
                         height=height,
                         theme=pygame_menu.themes.THEME_BLUE)

        self.label = self.add.label("Welcome to Space Rocks!", label_id="message_box")

        self.name = self.add.text_input("Name : ",
                                        default="Bilbo Baggins")

        self.add.selector("Number of Rocks :",
                          [str(i) for i in range(1, 10)],
                          onchange=self._change_rock_count,
                          default=3)

        self.add.button("Create Singleplayer Game",
                        action=self._play_singleplayer_game)

        self.add.button("Create Multiplayer Game")
        self.add.button("High Scores!", action=self.display_high_scores)
        self.add.button("Quit", pygame_menu.events.EXIT)  # close the menu
        self.rock_count = 3

        # try to load the save states
        try:
            save_file = open("scores.p", "rb")
            self.high_scores = pickle.load(save_file)
        except FileNotFoundError as err:
            # if that didn't work, just make the highscores variable equal to []
            self.high_scores = []

    def _change_rock_count(self, *args) -> None:
        self.rock_count = int(args[0][0])

    def _play_singleplayer_game(self, *args):
        """
        this function will return a single player instance of a game
        using the data entered in the menu
        """
        self.game = create_singleplayer_game(self.rock_count, self.screen)
        new_score = self.game.main_loop()
        self._post_score(new_score[1], self.name.get_value())  # post the score to the

        self.label.set_title(new_score[0])
        # do something with the score when you win!

    def _post_score(self, score, name) -> None:
        # add the high score to the score list
        self.high_scores.append((name, score))  # append a tuple with the name and score of the player

        # when you close down the game, save the scores
        # try to load the save states
        try:
            save_file = open("scores.p", "wb")
            pickle.dump(self.high_scores, save_file)
        except Exception as err:
            print("Error saving file.")

    def display_high_scores(self) -> None:
        # display a menu with the scores

        # debug
        print(self.high_scores)


    def _create_multiplayer_game(self):
        """
        this function will return a multi player instance of a game
        using the data entered in the menu
        """
        pass