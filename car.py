###
# car.py
#
# This file contains the Car class, which represents an individual car on the
# roundabout.
###

from utils import (NORTH, EAST, SOUTH, WEST)
from numpy.random import RandomState


class Car:
    def __init__(self, orientation, start_pos, end_pos, active=True, p_turn=0.5,
                 turn_ctr=0, switch_ctr=0, asshole_factor=0, asshole_ctr=0):
        self.orientation = orientation
        self.cur_pos = start_pos
        self.prev_pos = [start_pos, 0]
        self.active = active
        self.p_turn = p_turn
        self.turn_ctr = turn_ctr
        self.switch_ctr = switch_ctr
        self.turns = 0
        self.asshole_factor = asshole_factor
        self.asshole_ctr = asshole_ctr

    def __repr__(self):
        return '(cur_pos: {}, orientation: {})'.format(self.cur_pos,
                                                       self.orientation)

    def toggle_active(self):
        """Toggle whether a car is active or not (e.g. still participating in
           the traffic of the roundabout)."""
        self.active = not self.active

    def drive(self):
        """Move the car to a new position.

        Arguments:
            new_pos {[int, int]} -- A numpy-array containing the x and y
                                    coordinates of the new position.

        Returns:
            {[int, int]} -- A numpy-array containing the x and y coordinates
                            of the updated current position.
        """
        if self.orientation == NORTH:
            self.cur_pos[0] -= 1
        elif self.orientation == EAST:
            self.cur_pos[1] += 1
        elif self.orientation == SOUTH:
            self.cur_pos[0] += 1
        elif self.orientation == WEST:
            self.cur_pos[1] -= 1

        return self.cur_pos

    def turn_left(self):
        """Make a left turn."""
        self.orientation = (self.orientation - 1) % 4
        self.turns += 1

    def turn_right(self):
        """Make a right turn."""
        self.orientation = (self.orientation + 1) % 4
        self.turns += 1

    def look_left(self):
        """Look to the position left of the car.

        Returns:
            int -- The orientation left of the car.
        """
        return (self.orientation - 1) % 4

    def look_right(self):
        """Look to the position right of the car.

        Returns:
            int -- The orientation right of the car.
        """
        return (self.orientation + 1) % 4
