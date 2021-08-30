from pygame.sprite import Sprite


class SpaceObject(Sprite):
    # each Space Object has some basic data that's attached to it
    # and they all inherit from the Sprite class
    def __init__(self):
        # we define the basic physical location and properties of a space object during
        # instantiation, a space object can have a postion, a angle theta, a velocity
        # causes a certain amount of collision damage, has a health, etc.

        # physical stats of the object
        self.mass = None  # mass of the object, useful for momentum calculation

        # the position variables will eventually be handled some other way
        self.x = None  # x position
        self.y = None  # y postion
        self.theta = None  # angle theta of the sprite

        # these are the values for velocity
        # we'll figure out how to properly scale these later, but at first glance
        # I suspect the velocities should be in "pixels / second" and the angular velocity in
        # in "radians / second"
        self.dx = None
        self.dy = None
        self.dtheta = None

        # default health
        self.health = 100

        # default damage that is experienced when colliding with it
        self.collision_damage = 1


class SpaceBoulder(SpaceObject):
    # the actual physical asteroid sprites go here
    def __init__(self):
        pass


class Player(SpaceObject):
    # the player sprites go in here
    def __init__(self):
        pass


class Bullet(SpaceObject):
    # bullet sprites go here
    def __init__(self):
        pass