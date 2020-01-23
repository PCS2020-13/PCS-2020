###
# magic.py
# This file contains the defintions for processing the cars
# on the magic roundabout.
###

import numpy as np
from utils import (DEBUG, random_row, NORTH, EAST, SOUTH, WEST)
from numpy.random import RandomState
import sys


def exceptions_magic(self, car):
    """Handles special cases for turning cars.

    Arguments:
        car {Car} -- The car that should drive.

    Returns:
        int -- The state of the position of the car, depending on the exception.
    """
    for i in range(0, 4):
        if np.array_equal(car.cur_pos, self.exceptions[i]):
            if car.orientation == EAST:
                return 6
            else:
                return 4

    for i in range(4, 8):
        if np.array_equal(car.cur_pos, self.exceptions[i]):
            if car.orientation == SOUTH:
                return 6
            else:
                return 4

    for i in range(8, 12):
        if np.array_equal(car.cur_pos, self.exceptions[i]):
            if car.orientation == WEST:
                return 6
            else:
                return 4

    for i in range(12, 16):
        if np.array_equal(car.cur_pos, self.exceptions[i]):
            if car.orientation == NORTH:
                return 6
            else:
                return 4

    for i in range(16, 18):
        if np.array_equal(car.cur_pos, self.exceptions[i]):
            if car.orientation == EAST:
                return 5
            else:
                return 4

    for i in range(18, 20):
        if np.array_equal(car.cur_pos, self.exceptions[i]):
            if car.orientation == SOUTH:
                return 5
            else:
                return 4

    for i in range(20, 22):
        if np.array_equal(car.cur_pos, self.exceptions[i]):
            if car.orientation == WEST:
                return 5
            else:
                return 4

    for i in range(22, 24):
        if np.array_equal(car.cur_pos, self.exceptions[i]):
            if car.orientation == NORTH:
                return 5
            else:
                return 4

    for i in range(24, 26):
        if np.array_equal(car.cur_pos, self.exceptions[i]):
            if car.orientation == NORTH:
                return 5
            else:
                return 3

    for i in range(26, 28):
        if np.array_equal(car.cur_pos, self.exceptions[i]):
            if car.orientation == EAST:
                return 5
            else:
                return 3

    for i in range(28, 30):
        if np.array_equal(car.cur_pos, self.exceptions[i]):
            if car.orientation == SOUTH:
                return 5
            else:
                return 3

    for i in range(30, 32):
        if np.array_equal(car.cur_pos, self.exceptions[i]):
            if car.orientation == WEST:
                return 5
            else:
                return 3


def process_cars_magic(self):
    """Special function for processing cars on the magic roundabout."""
    self.cars_on_round = []
    self.cars_not_round = []

    # Define which cars are on the roundabout.
    if not self.collision():
        for car in self.cars:
            if list(car.cur_pos) in self.model.area:
                self.cars_on_round.append(car)
            else:
                self.cars_not_round.append(car)
    # If there is a collision, print out the position of it and exit.
    else:
        cur_pos = [car.cur_pos for car in self.cars]
        pos, count = np.unique(cur_pos, axis=0, return_counts=True)
        print(pos[count > 1])
        sys.exit('Cars overlap')

    # Let the cars on the roundabout drive first.
    for car in self.cars_on_round:
        drive_magic(self, car)
    else:
        car.prev_pos[1] = 0
    for car in self.cars_not_round:
        drive_magic(self, car)


def drive_magic(self, car, wait_ctr=3):
    r, c = car.cur_pos
    state = self.model.grid[r][c]

    # Depending on the asshole factor, stand still for 3 time steps.
    stand = RandomState().binomial(1, p=car.asshole_factor)
    if stand or (car.asshole_ctr > 0 and car.asshole_ctr < 4):
        car.asshole_ctr += 1
    else:
        # state 8 defines the exceptions
        if state == 8:
            state = exceptions_magic(self, car)

        if state == 1:
            if self.priority(car, car.orientation):
                self.free_starts = np.append(
                    self.free_starts, [car.cur_pos], axis=0)
                car.drive()
        elif state == 2:
            car.toggle_active()
            self.n_finished += 1
            self.turns_per_car.append(car.turns)
            return
        elif state == 3:
            if self.priority(car, car.look_left()):
                car.turn_left()
                car.drive()
        elif state == 4:
            car.turn_ctr += 1
            prob = car.turn_ctr * (1/4)
            if prob > 1:
                prob = 1

            # Checks if car stands still for more than 3 turns
            if car.prev_pos[1] >= wait_ctr:
                prob = 1-prob

            turn = np.random.binomial(1, p=1/2)
            if turn == 1:
                if self.priority(car, car.look_left()):
                    car.turn_left()
                    car.drive()
                else:
                    car.turn_ctr = 3
            else:
                if self.priority(car, car.orientation):
                    car.drive()
        elif state == 5:
            if self.priority(car, car.orientation):
                car.drive()

        elif state == 6:
            car.turn_ctr += 1
            prob = car.turn_ctr * (1/4)
            if prob > 1:
                prob = 1

            # Checks if car stands still for more than 3 turns
            if car.prev_pos[1] == wait_ctr:
                prob = 1-prob
                car.prev_pos[1] = 0
                self.waiting_cars += 1

            turn = np.random.binomial(1, p=1/2)
            if turn == 1:
                if self.priority(car, car.look_right()):
                    car.turn_right()
                    car.drive()
                else:
                    car.turn_ctr = 3
            else:
                if self.priority(car, car.orientation):
                    car.drive()
        elif state == 7:
            if self.priority(car, car.look_right()):
                car.turn_right()
                car.drive()
        elif state == 9:
            if self.priority(car, car.look_right()):
                if car.switch_ctr == 0 or car.prev_pos[1] >= wait_ctr:
                    if car.prev_pos[1] >= wait_ctr:
                        p = 1
                    else:
                        p = 1/5
                    if RandomState().binomial(1, p=p) == 1:
                        car.turn_right()
                        car.drive()
                        car.turn_left()
                        if self.priority(car, car.orientation):
                            car.drive()
                            car.switch_ctr = 1
                        else:
                            car.turn_left()
                            car.drive()
                            car.turn_right()
                            if self.priority(car, car.orientation):
                                car.drive()
                    elif self.priority(car, car.orientation):
                        car.drive()
                elif self.priority(car, car.orientation):
                    car.drive()
            elif self.priority(car, car.orientation):
                car.drive()

        elif state == 10:
            if self.priority(car, car.look_left()):
                if car.switch_ctr == 0 or car.prev_pos[1] >= wait_ctr:
                    if car.prev_pos[1] >= wait_ctr:
                        p = 1
                    else:
                        p = 1/5
                    if RandomState().binomial(1, p=p) == 1:
                        car.turn_left()
                        car.drive()
                        car.turn_right()
                        if self.priority(car, car.orientation):
                            car.drive()
                            car.switch_ctr = 1
                        else:
                            car.turn_right()
                            car.drive()
                            car.turn_left()
                            if self.priority(car, car.orientation):
                                car.drive()
                    elif self.priority(car, car.orientation):
                        car.drive()
                elif self.priority(car, car.orientation):
                    car.drive()
            elif self.priority(car, car.orientation):
                car.drive()

        if np.array_equal(car.cur_pos, car.prev_pos[0]):
            car.prev_pos[1] += 1

        car.prev_pos[0] = car.cur_pos
