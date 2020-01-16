import numpy as np
from numpy.random import binomial

import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.animation as animation
import sys

from utils import (DEBUG, random_row, NORTH, EAST, SOUTH, WEST)
from car import Car

CAR_VALUE = -1

# Define car color
cmap = cm.Dark2
cmap.set_bad(color='red')

####
# TODO:
#       - Reckless driving
#         * asshole_factor
#         * dick_move()
#
# OPTIONAL:
#       - Different car velocities
#       -
####


class RoundaboutSim():
    def __init__(self, model, density=0.05, steps=1000, show_animation=True):
        # self.model = np.loadtxt(model_path, delimiter = ' ', dtype=int)
        self.model = model
        self.aimed_density = density
        self.true_density = 0
        self.steps = steps
        self.exceptions = model.exceptions

        self.road_size = (self.model.grid != 0).sum()
        self.n_finished = 0

        self.start_states = np.argwhere(self.model.grid == 1)
        assert self.start_states.size != 0, 'This roundabout contains no start states.'
        self.end_states = np.argwhere(self.model.grid == 2)
        assert self.end_states.size != 0, 'This roundabout contains no end states.'

        self.free_starts = np.copy(self.start_states)
        self.cars = []
        self.turns_per_car = []

        self.show_animation = show_animation

    def __str__(self):
        return str(self.model)
        # return '\n'.join([np.array2string(row)[1:-1] for row in self.model.grid])

    def set_steps(self, steps):
        self.steps = steps

    def get_cars(self):
        """Get a list of the cars currently on the grid.

        Returns:
            np.array -- An array containing the cars.
        """
        return self.cars

    def get_start_orientation(self, start_pos):
        """Helper function for determining the initial orientation of a car.

        Arguments:
            start_pos {(int, int)} -- A tuple with the x and y coordinates of the starting position.

        Returns:
            int -- The integer corresponding to the ordinal orientation.
        """
        if start_pos[0] == 0:
            return SOUTH
        elif start_pos[1] == 0:
            return EAST
        elif start_pos[0] == self.model.grid.shape[0] - 1:
            return NORTH
        elif start_pos[1] == self.model.grid.shape[1] - 1:
            return WEST

    def get_grid(self):
        """Creates a grid with all cars currently on the road. The cells that have a car on them will take on CAR_VALUE.

        Returns:
            np.array -- The model with all cars currently on the grid.
        """
        grid = np.copy(self.model.grid)

        for car in self.cars:
            r, c = car.cur_pos
            grid[r][c] = CAR_VALUE

        masked_grid = np.ma.masked_where(grid == CAR_VALUE, grid)
        return masked_grid

    def draw_model(self, with_cars=True, blocking=True):
        """Draws the model of the roundabout.

        Keyword Arguments:
            blocking {bool} -- If set to 'True', the figure is displayed immediately and the program waits 
            until the figure is closed. Otherwise it waits until a blocking show() somewhere else in the program is called.
            (default: {True})
        """
        if with_cars:
            grid = self.get_grid()
            masked_grid = np.ma.masked_where(grid == CAR_VALUE, grid)
            plt.imshow(masked_grid, cmap=cmap)
        else:
            plt.imshow(self.model.grid, cmap=cmap)

        plt.axis('off')
        plt.show(block=blocking)

    def spawn_cars(self):
        while self.free_starts.size != 0 and self.true_density < self.aimed_density:
            start_pos = random_row(self.free_starts)[0]
            end_pos = random_row(self.end_states)[0]
            orientation = self.get_start_orientation(start_pos)
            car = Car(orientation, start_pos, end_pos)
            self.cars.append(car)
            self.true_density = len(self.cars) / self.road_size

            # Delete the start position from the list of possible starts
            self.free_starts = np.delete(self.free_starts, (np.where(
                (self.free_starts == start_pos).all(axis=1))[0][0]), axis=0)

    def reset(self):
        self.cars = []
        self.n_finished = 0
        self.true_density = 0
        self.free_starts = np.copy(self.start_states)

    def run(self):
        """Initializes the simulation."""
        self.spawn_cars()
        grid = self.get_grid()

        if DEBUG:
            print(self.cars)

        if self.show_animation:
            fig = plt.figure()
            frame = plt.gca()
            frame.axes.get_xaxis().set_visible(False)
            frame.axes.get_yaxis().set_visible(False)

            cmap = cm.Dark2
            cmap.set_bad(color='red')
            sim_grid = plt.imshow(grid, cmap=cmap)

            anim = animation.FuncAnimation(fig, self.step,
                                           fargs=(sim_grid,),
                                           interval=500,  # MAKE VARIABLE
                                           frames=self.steps,
                                           repeat=False
                                           )

            plt.show()

        else:
            for i in range(self.steps):
                self.step(i, grid)
        
        print("== FINAL STATISTICS ==")
        print("CARS FINISHED PER STEP: {}".format(self.n_finished/self.steps))
        print("TOTAL STEPS  : {}".format(self.steps))
        print("CARS IN TOTAL: {}".format(len(self.cars)+self.n_finished))
        print("CARS FINISHED: {}".format(self.n_finished))
        print("THROUGHPUT   : {} %".format(round((self.n_finished/(len(self.cars)+self.n_finished)*100), 3)))
        print("======================")

    def step(self, i, grid):
        if DEBUG:
            print("== Iteration {} ==".format(i))
        if self.model.name == 'Magic':
            self.process_cars_magic()
        else:
            self.process_cars()
        self.spawn_cars()

        if self.show_animation:
            grid.set_data(self.get_grid())

        return grid,

    def process_cars(self):
        '''
        0 = Grass
        1 = Start
        2 = Stop
        3 = Left
        4 = Left and straight
        5 = Straight
        6 = Right and straight
        7 = Right
        8 = Special
        9 = Switch to right lane
        10 = Switch to left lane
        '''

        # if self.model.name == 'Magic':
        #     self.process_cars_magic()
        # else:

        self.cars_on_round = []
        self.cars_not_round = []

        # Define which cars are on the roundabout.
        if not self.collision():
            for car in self.cars:
                if list(car.cur_pos) in self.model.area:
                    self.cars_on_round.append(car)
                else:
                    self.cars_not_round.append(car)
        else:
            cur_pos = [car.cur_pos for car in self.cars]
            print(cur_pos)
            sys.exit('Cars overlap')

        # Let the cars on the roundabout drive first.
        for car in self.cars_on_round:
            self.drive_roundabout(car)

        for car in self.cars_not_round:
            self.drive_outside(car)

        self.cars = list(filter(lambda c: c.active, self.cars))
        self.true_density = len(self.cars) / self.road_size

        if DEBUG:
            print("CARS ON THE ROAD: {}".format(len(self.cars)))
            print("DENSITY: {}".format(self.true_density))
            print("CARS FINISHED: {}".format(self.n_finished))

    def drive_roundabout(self, car):
        r, c = car.cur_pos
        state = self.model.grid[r][c]

        # state 8 defines the exceptions
        if state == 8:
            state = self.exception_handling(car)

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
            turn = np.random.binomial(1, p=prob)
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
            car.turn_right()
            if self.priority(car, car.orientation):
                car.drive()
                car.turn_left()
            else:
                car.turn_left()
        elif state == 10:
            car.turn_left()
            if self.priority(car, car.orientation):
                car.drive()
                car.turn_right()
            else:
                car.turn_right()

    def drive_outside(self, car):
        r, c = car.cur_pos
        state = self.model.grid[r][c]

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

    def priority(self, car, orientation):
        check_pos = car.cur_pos
        if orientation == NORTH:
            check_pos = check_pos + [-1, 0]
        elif orientation == EAST:
            check_pos = check_pos + [0, 1]
        elif orientation == SOUTH:
            check_pos = check_pos + [1, 0]
        else:
            check_pos = check_pos + [0, -1]

        for vehicle in self.cars:
            if np.array_equal(vehicle.cur_pos, check_pos):
                return False
        return True

    def collision(self):
        cur_pos = [car.cur_pos for car in self.cars]
        if len(np.unique(cur_pos, axis=0)) == len(cur_pos):
            return False
        return True

    def exception_handling(self, car):
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

        elif self.model.name == 'Magic':
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
        self.cars_on_round = []
        self.cars_not_round = []

        # Define which cars are on the roundabout.
        if not self.collision():
            for car in self.cars:
                if list(car.cur_pos) in self.model.area:
                    self.cars_on_round.append(car)
                else:
                    self.cars_not_round.append(car)
        else:
            cur_pos = [car.cur_pos for car in self.cars]
            print(cur_pos)
            sys.exit('Cars overlap')

        # Let the cars on the roundabout drive first.
        for car in self.cars_on_round:
            self.drive_magic(car)

        for car in self.cars_not_round:
            self.drive_magic(car)

        self.cars = list(filter(lambda c: c.active, self.cars))
        self.true_density = len(self.cars) / self.road_size

        if DEBUG:
            print("CARS ON THE ROAD: {}".format(len(self.cars)))
            print("DENSITY: {}".format(self.true_density))
            print("CARS FINISHED: {}".format(self.n_finished))

    def drive_magic(self, car):
        r, c = car.cur_pos
        state = self.model.grid[r][c]

        # state 8 defines the exceptions
        if state == 8:
            state = self.exception_handling(car)

        if state == 1:
            self.free_starts = np.append(
                self.free_starts, [car.cur_pos], axis=0)
            if self.priority(car, car.orientation):
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
            turn = np.random.binomial(1, p=prob)
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
            turn = np.random.binomial(1, p=prob)
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
            car.turn_right()
            if self.priority(car, car.orientation):
                car.drive()
                car.turn_left()
            else:
                car.turn_left()
        elif state == 10:
            car.turn_left()
            if self.priority(car, car.orientation):
                car.drive()
                car.turn_right()
            else:
                car.turn_right()