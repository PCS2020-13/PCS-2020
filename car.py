## Car class
from utils import (NORTH, EAST, SOUTH, WEST)

class Car:
    def __init__(self, orientation, start_pos, end_pos, active=True, p_turn=0.5, turn_ctr=0):
        self.orientation = orientation
        self.cur_pos = start_pos
        self.active = active
        self.p_turn = p_turn
        self.turn_ctr = turn_ctr

    def __repr__(self):
        return '(cur_pos: {}, orientation: {})'.format(self.cur_pos, self.orientation)

    def toggle_active(self):
        self.active = not self.active

    def drive(self):
        """Move the car to a new position.

        Arguments:
            new_pos {[int, int]} -- A numpy-array containing the x and y coordinates of the new position.

        Returns:
            {[int, int]} -- A numpy-array containing the x and y coordinates of the updated current position.
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
        """Make a left turn.
        """
        self.orientation = (self.orientation - 1) % 4

    def turn_right(self):
        """Make a right turn.
        """
        self.orientation = (self.orientation + 1) % 4

