import pygame.image
from pygame.sprite import Sprite
from math import pi


class SpaceObject(Sprite):
    # each Space Object has some basic data that's attached to it
    # and they all inherit from the Sprite class
    def __init__(self):
        # we define the basic physical location and properties of a space object during
        # instantiation, a space object can have a postion, a angle theta, a velocity
        # causes a certain amount of collision damage, has a health, etc.

        # first, let's get all the stuff from the parent class
        super().__init__()

        # the default image
        self.image = pygame.image.load("images/player.png").convert_alpha()
        self.rect = self.image.get_rect()


        # physical stats of the object
        self.mass = 1  # mass of the object, useful for momentum calculation

        # the position variables will eventually be handled some other way
        self.theta = 0  # angle theta of the sprite

        # these are the values for velocity
        # we'll figure out how to properly scale these later, but at first glance
        # I suspect the velocities should be in "pixels / second" and the angular velocity in
        # in "radians / second"
        self.dx = 0
        self.dy = 0
        self.dtheta = 0

        # default health
        self.health = 100

        # default damage that is experienced when colliding with it
        self.collision_damage = 1

        self.rotation_mapping = {}

    def create_rotation_map(self):
        # make a hash table of all the rotations
        # I did this because rotating every time was ponderously slow
        # this let me load all the angles into a dictionary
        for angle in range(-15,380):
            # it's a little more than 360 degrees because rounding errors can cause a key error
            orig_image = self.image.copy()
            rotated_image = pygame.transform.rotozoom(orig_image, angle, 1)
            self.rotation_mapping[angle] = rotated_image

    def update(self):
        # this gets updated when you update a sprite or group of sprites
        # it's just part of the Pygame API

        # let's process rotation here
        # we want to keep the values of theta from becoming giant
        if self.dtheta != 0:
            if self.theta > 360:
                self.theta = 0
            elif self.theta < 0:
                self.theta = 360

            self.theta += self.dtheta

        self.image = self.rotation_mapping[round(self.theta)]
        self.rect = self.image.get_rect(center=self.rect.center)

        # we can process motion here
        if (not self.dx == 0) or (not self.dy == 0):
            # if there's motion, update the sprite position
            # you could change this with DeMorgan's law... but this seems cleanest
            self.rect.centerx += self.dx
            self.rect.centery += self.dy


class SpaceBoulder(SpaceObject):
    # the actual physical asteroid sprites go here

    def __init__(self):
        # let's get all the data from the class above
        super().__init__()

        # load the image from the images folder
        self.image = pygame.image.load("images/meteorBig.png").convert_alpha()

        # create a rectangle from the image
        self.rect = self.image.get_rect()

        # you have to do this to initialize the sprite
        pygame.sprite.Sprite.__init__(self)

class Player(SpaceObject):
    # the player sprites go in here
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # you have to do this to initialize the sprite

class Bullet(SpaceObject):
    # bullet sprites go here
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # you have to do this to initialize the sprite
