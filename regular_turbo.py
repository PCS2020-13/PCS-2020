###
# regular_turbo.py
# This file contains the defintions for processing the cars
# on the regular and the turbo roundabout.
###

import numpy as np
from utils import (DEBUG, random_row, NORTH, EAST, SOUTH, WEST)
from numpy.random import RandomState

def exception_handling(self, car):
    """Handles special cases for turning cars, depending on the type of roundabout.

    Arguments:
        car {Car} -- The car that should drive.

    Returns:
        int -- The state of the position of the car, depending on the exception.
    """
    if self.model.name == "Regular":
        for i in range(0, 2):
            if np.array_equal(car.cur_pos, self.exceptions[i]):
                if car.orientation == SOUTH:
                    return 7
                else:
                    return 5
        for i in range(2, 4):
            if np.array_equal(car.cur_pos, self.exceptions[i]):
                if car.orientation == EAST:
                    return 7
                else:
                    return 5
        for i in range(4, 6):
            if np.array_equal(car.cur_pos, self.exceptions[i]):
                if car.orientation == NORTH:
                    return 7
                else:
                    return 5
        for i in range(6, 8):
            if np.array_equal(car.cur_pos, self.exceptions[i]):
                if car.orientation == WEST:
                    return 7
                else:
                    return 5

    elif self.model.name == "Turbo":
        for i in range(2):
            if np.array_equal(car.cur_pos, self.exceptions[i]):
                if car.orientation == EAST:
                    return 7
                else:
                    return 5

        if np.array_equal(car.cur_pos, self.exceptions[2]):
            if car.orientation == SOUTH:
                return 7
            else:
                return 5

        for i in range(3, 5):
            if np.array_equal(car.cur_pos, self.exceptions[i]):
                if car.orientation == WEST:
                    return 7
                else:
                    return 5

        if np.array_equal(car.cur_pos, self.exceptions[5]):
            if car.orientation == NORTH:
                return 7
            else:
                return 5


def process_cars_reg(self):
    """Process the cars.
    The next step of a car depends on the state of the current cell it is on.
    """
    
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
        drive_roundabout(self, car)

    for car in self.cars_not_round:
        drive_outside(self, car)

def drive_roundabout(self, car, wait_ctr=2):
        """Let a car drive on the roundabout.

        Arguments:
            car {Car} -- The car that should drive.
        """
        row, col = car.cur_pos
        state = self.model.grid[row][col]

        # State 8 defines the exceptions
        if state == 8:
            state = exception_handling(self, car)

        if state == 3:
            if self.priority(car, car.look_left()):
                car.turn_left()
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
            if car.prev_pos[1] >= wait_ctr:
                prob = 1-prob

            turn = RandomState().binomial(1, p=prob)
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
            if car.switch_ctr == 0 and self.priority(car, car.look_right()):
                if RandomState().binomial(1, p=1/2) == 1:
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

        elif state == 10:
            if car.switch_ctr == 0 and self.priority(car, car.look_left()):
                if RandomState().binomial(1, p=1/2) == 1:
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

        if np.array_equal(car.cur_pos, car.prev_pos[0]):
            car.prev_pos[1] += 1
        else:
            car.prev_pos[1] = 0
        car.prev_pos[0] = car.cur_pos

def drive_outside(self, car):
        """Let a car drive outside of the roundabout.

        Arguments:
            car {Car} -- The car that should drive.
        """
        row, col = car.cur_pos
        state = self.model.grid[row][col]

        # Check if nothing is in front of the car
        if self.priority(car, car.orientation):
            if state == 1:
                self.free_starts = np.append(
                    self.free_starts, [car.cur_pos], axis=0)
            elif state == 2:
                car.toggle_active()
                self.n_finished += 1
                self.turns_per_car.append(car.turns)
                return
            car.drive()