import sys
import pygame
from random import randint, random, choice
from ObjectsInSpace import *
from math import sin, cos, radians, sqrt


class SpaceRocks:
    def __init__(self):
        # initialize Pygame
        # this has to fire up when initializing the instance of a SpaceRocks class
        pygame.init()

        # let's set up the screen
        pygame.display.set_caption("Space Rocks")
        # screen size for convenience during initialization
        self.max_screen_x = 800
        self.max_screen_y = 600
        screen_size = (self.max_screen_x, self.max_screen_y)
        self.screen = pygame.display.set_mode(screen_size)

        # game clock
        self.clock = pygame.time.Clock()

        # sprite Group
        self.space_objects = pygame.sprite.Group()

        print("Initializing Objects!")
        # let's initialize the objects, let's make them random
        for i in range(10):
            new_rock = SpaceBoulder()
            new_rock.centerx = randint(0, self.max_screen_x)
            new_rock.centery = randint(0, self.max_screen_y)
            new_rock.dx = randint(-3, 3)
            new_rock.dy = randint(-3, 3)
            new_rock.theta = randint(0, 360)
            new_rock.dtheta = random()*choice([1, -1])  # degrees per second
            new_rock.create_rotation_map()

            # do more later
            self.space_objects.add(new_rock)

        # debug test object for control test
        self.player_ship = Player()
        self.player_ship.centerx, self.player_ship.centery = self.max_screen_x/2, self.max_screen_y/2
        self.player_ship.dtheta = 0
        self.player_ship.create_rotation_map()
        self.player_ship.is_controllable = True
        self.space_objects.add(self.player_ship)

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

        # control of the sprites works by turning off or on sprites' thrusters
        sprites = [sprite for sprite in self.space_objects if sprite.is_controllable]
        # a list of all the sprites that are player controllable
        for sprite in sprites:
            if event.type == pygame.KEYUP:
                # when you let up on the keys, the rotation stops
                sprite.stop_rotation()
            elif event.type == pygame.KEYDOWN:
                # when you push a key, let's turn thrusters on or off
                if event.key == pygame.K_LEFT:
                    sprite.rotate_left()
                elif event.key == pygame.K_RIGHT:
                    sprite.rotate_right()
                elif event.key == pygame.K_UP:
                    sprite.accelerate()
                elif event.key == pygame.K_DOWN:
                    sprite.decelerate()
                elif event.key == pygame.K_SPACE:
                    bullet = sprite.fire()
                    bullet.create_rotation_map()
                    self.space_objects.add(bullet)

    def _process_game_logic(self):
        # start with processing the simple physics
        # delete object list
        delete_list = []
        for obj in self.space_objects:

            # let's warm the object back around if it goes outside the screen
            if obj.rect.centerx > (self.max_screen_x + obj.rect.width):
                obj.rect.centerx = -obj.rect.width

            if obj.rect.centerx < -obj.rect.width:
                obj.rect.centerx = self.max_screen_x + obj.rect.width

            if obj.rect.centery > (self.max_screen_y + obj.rect.height):
                obj.rect.centery = -obj.rect.height

            if obj.rect.centery < -obj.rect.height:
                obj.rect.centery = self.max_screen_y + obj.rect.height

            if isinstance(obj,Bullet):
                if obj.range <= 0:
                    delete_list.append(obj)

        # now delete all the stuff that should be deleted
        for obj in delete_list:
            self.space_objects.remove(obj)


    def _draw(self):
        background_color = (0, 0, 255)
        self.screen.fill(background_color)

        # now let's update and draw all the sprites
        self.space_objects.update()
        self.space_objects.draw(self.screen)

        pygame.display.flip()
