import sys
import pygame
from ObjectsInSpace import *

class SpaceRocks:
    def __init__(self):
        # initialize Pygame
        # this has to fire up when initializing the instance of a SpaceRocks class
        pygame.init()
        pygame.display.set_caption("Space Rocks")
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.running = True
        self.space_objects = []  # eventually this will be a list of all the sprites
        # there may be a better way to do in Pygame (sprite groups), -pp

        # menu instantiation here?
        # my intuition is that for something simple like this, maybe we should have
        # any menu stuff handled in the instantiation of the class?  I don't know - TBD.

    def __del__(self):
        # when the object is deleted, kill Pygame
        pygame.quit()

    def main_loop(self):

        while True:

            # get all the events, and process every one
            for event in pygame.event.get():
                self._process_events(event)

            # sprite colision, physics stuff, etc can go in this function
            self._process_game_logic()

            # draw the scene on the screen
            self._draw()

            # now tick the clock forward
            self.clock.tick(60)

    def _process_events(self, event):
        # pygame events processed here
        # I reckon we could eventually refactor this into
        # a class?  I'm not sure of the best way to handle this yet -pp

        # first, let's process the process of properly quitting pygame
        if event.type == pygame.QUIT:
            # first let's kill the loop running the variable
            # why?  Well - I'd imagine there's some multi threading under the hood
            # and God knows what processes will still be running, let's make sure
            # there's not a chance to loop through again, as Ripley would say
            # nuke it from orbit, it's the only way to be sure
            # i'll add that after adding this event handler
            pygame.quit()
            sys.exit()  # finally, let's kill everything that's left

    def _process_game_logic(self):
        pass

    def _draw(self):
        background_color = (0, 0, 255)
        self.screen.fill(background_color)
        pygame.display.flip()
