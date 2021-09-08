import pygame.image
from pygame.sprite import Sprite
from math import atan2, radians, sin, cos, sqrt
from random import choice


class SpaceObject(Sprite):
    # each Space Object has some basic data that's attached to it
    # and they all inherit from the Sprite class
    def __init__(self):
        # we define the basic physical location and properties of a space object during
        # instantiation, a space object can have a position, a angle theta, a velocity
        # causes a certain amount of collision damage, has a health, etc.

        # first, let's get all the stuff from the parent class
        super().__init__()

        # the default image
        # you must rotate all the images so they face to the right
        # you can do this by loading the image in rotated - load the image, convert alpha, then rotate it -90 degrees
        self.image = pygame.transform.rotate(pygame.image.load("images/player.png").convert_alpha(), -90)
        self.rect = self.image.get_rect()

        # physical stats of the object
        self.mass = 1  # mass of the object, useful for momentum calculation

        # the position variables may eventually be handled some other way
        self.theta = 0  # angle theta of the sprite, basically the heading

        # these are the values for velocity
        # we'll figure out how to properly scale these later, but at first glance
        # I suspect the velocities should be in "pixels / second" and the angular velocity in
        # in "radians / second"
        self.dx = 0
        self.dy = 0
        self.dtheta = 0
        self.thruster_rate = 0  # this will determine how fast a particular object can rotate by default
        self.max_speed = 10  # in pixels per second

        # default health
        self.max_health = 100
        self.health = 100

        # default damage that is experienced when colliding with it
        self.collision_damage = 1

        self.rotation_mapping = {}

        # debug flag
        self.debug = False

        # controllable flags
        self.is_controllable = False
        self.network_controllable = False
        self.AI_controllable = False

    def create_rotation_map(self):
        # make a hash table of all the rotations
        # I did this because rotating every time was ponderously slow
        # this let me load all the angles into a dictionary
        for angle in range(-15, 380):
            # it's a little more than 360 degrees because rounding errors can cause a key error
            orig_image = self.image.copy()
            rotated_image = pygame.transform.rotozoom(orig_image, angle, 1)
            self.rotation_mapping[angle] = rotated_image

    def stop_rotation(self):
        self.dtheta = 0

    def rotate_right(self):
        self.dtheta = -self.thruster_rate

    def rotate_left(self):
        self.dtheta = self.thruster_rate

    def accelerate(self):
        # this works by getting the current angle theta from the heading of the ship
        theta = radians(self.theta)
        # now figure out what the sum of the current speed and the thrust will give you
        new_dx = self.dx + cos(theta) * self.thruster_rate
        new_dy = self.dy - sin(theta) * self.thruster_rate

        # if that doesn't exceed the max speed then go ahead and add to speed
        if sqrt(new_dx ** 2 + new_dy ** 2) < self.max_speed:
            self.dx += cos(theta) * self.thruster_rate
            self.dy += -sin(theta) * self.thruster_rate

    def decelerate(self):
        # this works by getting the current angle theta from the heading of the ship
        theta = radians(self.theta)
        # now figure out what the sum of the current speed and the thrust will give you
        new_dx = self.dx + cos(theta) * self.thruster_rate
        new_dy = self.dy - sin(theta) * self.thruster_rate

        # if that doesn't exceed the max speed then go ahead and add to speed
        if sqrt(new_dx ** 2 + new_dy ** 2) >= 0:
            self.dx = self.dx * self.thruster_rate/100
            self.dy = self.dy * self.thruster_rate/100

    def fire(self):
        # this produces a bullet object with the position and velocity of the sprite in question
        bullet = Bullet(self.rect, self.dy, self.dx, radians(self.theta))
        return bullet

    def get_track(self):
        dx = self.dx
        dy = self.dy
        return atan2(-dy, dx)

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

        if self.debug:
            print(self.rect, self.theta, self.dx, self.dy)


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
        super().__init__()
        # load the image from the images folder
        self.image = pygame.transform.rotate(pygame.image.load("images/player.png").convert_alpha(), -90)

        # create a rectangle from the image
        self.rect = self.image.get_rect()

        self.thruster_rate = 3
        self.max_speed = 20

        pygame.sprite.Sprite.__init__(self)  # you have to do this to initialize the sprite


class RockDebris(SpaceObject):

    def __init__(self, rect):
        # when a laser hits a rock, make some rock debris sprites that list a little bit
        super().__init__()  # you have to do this to initialize the Space Object class
        self.image = pygame.transform.rotate(pygame.image.load("images/meteorSmall.png").convert_alpha(), -90)
        self.rect = rect

        self.dx = choice([-1, 0, 1])
        self.dy = choice([-1, 0, 1])
        self.dtheta = choice([-10, -5, 0, 5, 10])

        self.range = 20  # counter range

        pygame.sprite.Sprite.__init__(self)

    def update(self):
        super().update()

        self.range = self.range - 1


class Spark(SpaceObject):
    # these are "sparks" objects
    # they're basically the same as RockDebris
    # but I think it's more readable to just make
    # a separate object
    def __init__(self, rect):
        # when a laser hits a rock, make some rock debris sprites that list a little bit
        super().__init__()  # you have to do this to initialize the Space Object class
        self.image = pygame.transform.rotate(pygame.image.load("images/spark.png").convert_alpha(), -90)
        self.rect = rect

        self.dx = choice([-10, 0, 10])
        self.dy = choice([-10, 0, 10])
        self.dtheta = choice([-10, -5, 0, 5, 10])

        self.range = 10  # counter range

        pygame.sprite.Sprite.__init__(self)

    def update(self):
        super().update()

        self.range = self.range - 1


class Bullet(SpaceObject):

    def __init__(self, rect, dx, dy, theta):
        super().__init__()  # you have to do this to initialize the Space Object class
        self.image = pygame.transform.rotate(pygame.image.load("images/laserRed.png").convert_alpha(), -90)

        self.rect = rect
        self.max_speed = 10
        self.dx = (dx + self.max_speed)*cos(theta)
        self.dy = (dy + -self.max_speed)*sin(theta)
        self.range = 50  # counter range

        pygame.sprite.Sprite.__init__(self)

    def update(self):
        super().update()

        self.range = self.range - 1
