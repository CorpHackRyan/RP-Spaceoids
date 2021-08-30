import pygame


class SpaceRocks:
    def __init__(self):
        # initialize Pygame
        # this has to fire up when initializing the instance of a SpaceRocks class
        pygame.init()
        pygame.display.set_caption("Space Rocks")
        self.screen = pygame.display.set_mode((800, 600))

    def main_loop(self):

        while True:
            self._handle_input()
            self._process_game_logic()
            self._draw()

    def _handle_input(self):
        pass

    def _process_game_logic(self):
        pass

    def _draw(self):
        background_color = (0, 0, 255)
        self.screen.fill(background_color)
        pygame.display.flip()
