from Vector import Vector
import pygame as pg
import math as ma


class Boid(object):
    """An object to interface with pygame, although has been designed so it can be worked along with pygame
    Boids follow 3 simple rules, each rule will give it a direction vector to follow.
    Separation - steer to avoid crowding local flockmates
    Alignment  - steer towards the average heading of local flockmates
    Cohesion   - steer to move towards the average position (center of mass) of local flockmates
    Read more at: https://en.wikipedia.org/wiki/Boids, https://www.red3d.com/cwr/boids/
    Author: Woonters
    Github repo at: https://github.com/Fritzbox2000/boids
    """
    # Static list holding all the boids in if no other is provided
    _boid_list_instances = []

    @staticmethod
    def set_boid_list(boid_list):
        """ Sets the mutable, iterable object that will hold the boids.
        It is default a list, access through:

        :param boid_list: Mutable, iterable object that will hold the boids"""
        Boid._boid_list_instances = boid_list

    def __init__(self, pygame_screen=None, x=0, y=0, direction=0, range=30, list_of_boids=None):
        """
        :param pygame_screen: The screen that Pygame uses
        :param x: The x position
        :param y: The y position
        :param direction:  The direction (in radians)
        :param range: The visibility range of the boid
        :param list_of_boids: All boids must be kept within a list, the class allows for you to use one, but you can
                provide your own, must be a mutable iterable object
        """
        # Position and direction are held in pygame.math Vector 2's (Might switch these to my own defined vectors,
        # dependent on if I need more control) TODO: Make own vector class
        self._pos = Vector([x, y])
        self._direction = Vector([ma.cos(direction), ma.sin(direction)])
        self.range = range
        # The _boid_list holds the iterable type that the boid is held in, I wrote this in automatically thinking I
        # would need it but at the moment I don't seem to... TODO: Delete _boid_list if no use comes up
        if list_of_boids is not None:
            self._boid_list = list_of_boids
        else:
            self._boid_list = self.__class__._boid_list_instances
        self._boid_list.append(self)
        # Sets the pygame screen, pygame isn't needed for this module to work, but I plan on making it intuitive to use
        # with it
        if pygame_screen is not None:
            self._screen = pygame_screen

    # Getters and Setters
    @property
    def screen(self):
        """ Returns the pygame screen being used """
        return self._screen

    @screen.setter
    def screen(self, pygame_screen):
        """Set the pygame screen to the given screen object
        :param pygame_screen: The pygame screen that is going to be used"""
        self._screen = pygame_screen

    @property
    def x(self):
        """ Returns the x position of the boid """
        return self._pos[0]

    @x.setter
    def x(self, value):
        """ Sets the x position of the boid
         :param value: The value x will become"""
        self._pos[0] = value

    @property
    def y(self):
        """ Returns the y position of the boid """
        return self._pos[1]

    @y.setter
    def y(self, value):
        """ Sets the y position of the boid
        :param value: The value y will become"""
        self._pos[1] = value

    @property
    def direction(self):
        """ Returns the direction of the boid (in radians)"""
        return ma.acos(self._direction[0])

    @direction.setter
    def direction(self, value):
        """ Sets the direction of the boid (in radians)
        :param value: The value of the direction"""
        self._direction = Vector([ma.cos(value), ma.sin(value)])

    def step_boid(self, sep_weighting=1, ali_weighting=1, coh_weighting=1, draw=None):
        """Steps through all the rules of a boid, updating x, y and direction.
        :param sep_weighting: int/float - The weighting of the separation rule
        :param ali_weighting: int/float - The weighting of the alignment rule
        :param coh_weighting: int/float - The weighting of the cohesion rule
        :param draw: Boolean - If the method should draw to a pre-defined pygame screen

        As said in the description of boids, they follow three main rules. Each of the rules is run on each boid,
         They can be run together using this step method, or separately using the methods:
         - separation()
         - alignment()
         - cohesion()
         check the documentation for each of those methods as well
        """
        if draw and not self._screen:
            raise RuntimeError(f"Tried to draw to pygame screen when no pygame_screen was given")

        if draw:
            pass

    @staticmethod
    def boid_class_step():
        """ More efficient than looping through the list of boids"""
        for boid in Boid._boid_list_instances:
            sep_vect = Vector([0, 0])
            ali_vect = Vector([0, 0])
            ali_list = []
            coh_vect = Vector([0, 0])
            coh_list = []
            for other_boid in Boid._boid_list_instances:
                if boid._boid_visible(other_boid) and boid != other_boid:
                    # boid is in visible range

                    # separation is worked out on the fly
                    sep_vect += boid.single_boid_sep(other_boid)

                    # alignment must be work out using means
                    ali_list.append(other_boid.direction)

                    # cohesion much like alignment must be worked out using means
                    coh_list.append(other_boid._pos)

            # work out alignment
            ali_size = len(ali_list)
            ali_dir = sum(ali_list)/ali_size
            ali_vect = Vector([ma.cos(ali_dir), ma.sin(ali_dir)])

            # work out cohesion
            coh_size = len(coh_list)
            coh_vect = sum(coh_list) * (1/coh_size)

    def separation(self):
        """Loops through all boids and works out the separation for this specific boid."""
        sep_vect = Vector([0, 0])
        for boid in Boid._boid_list_instances:
            if self._boid_visible(boid):
                sep_vect += self.single_boid_sep(boid)
        return sep_vect

    def alignment(self):
        pass

    def cohesion(self):
        pass

    def _boid_visible(self, boid):
        vec_to_boid = Vector([self.x - boid.x, self.y - boid.y])
        return True if vec_to_boid.magnitude() > self.range and self._direction.find_angle(vec_to_boid) < 135 else False

    def single_boid_sep(self, boid):
        vec_to_boid = Vector([self.x - boid.x, self.y - boid.y])
        calc = vec_to_boid.neg().standardise()
        dist = 1 if vec_to_boid.magnitude() == 0 else vec_to_boid.magnitude()
        return calc*(1/dist)


if __name__ == '__main__':
    pg.init()
    pg.display.init()
    screen = pg.display.set_mode((240, 180))

    pg.quit()
