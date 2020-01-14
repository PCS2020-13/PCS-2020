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
# TODO: - Reckless driving
#         * asshole_factor
#         * dick_move()
#       - Different car velocities
#       -
####


class RoundaboutSim():
    def __init__(self, model, density=0.01, steps=100, show_animation=True):
        # self.model = np.loadtxt(model_path, delimiter = ' ', dtype=int)
        self.model = model
        self.aimed_density = density
        self.true_density = 0
        self.steps = steps
        self.exceptions = model.exceptions

        self.road_size = (self.model != 0).sum()
        self.n_finished = 0

        self.start_states = np.argwhere(self.model == 1)
        assert self.start_states.size != 0, 'This roundabout contains no start states.'
        self.end_states = np.argwhere(self.model == 2)
        assert self.end_states.size != 0, 'This roundabout contains no end states.'

        self.free_starts = np.copy(self.start_states)
        self.cars = []
        self.turns_per_car = []

        self.show_animation = show_animation

    def __str__(self):
        return str(self.model)
        #return '\n'.join([np.array2string(row)[1:-1] for row in self.model.grid])

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
        elif start_pos[0] == self.model.shape[0] - 1:
            return NORTH
        elif start_pos[1] == self.model.shape[1] - 1:
            return WEST

    def get_grid(self):
        """Creates a grid with all cars currently on the road. The cells that have a car on them will take on CAR_VALUE.

        Returns:
            np.array -- The model with all cars currently on the grid.
        """
        grid = np.copy(self.model)

        for car in self.cars:
            r, c = car.cur_pos
            grid[r][c] = CAR_VALUE

        masked_grid = np.ma.masked_where(grid == CAR_VALUE, grid)
        return masked_grid

    def draw_model(self, with_cars=True, blocking=True):
        """Draws the model of the roundabout.

        Keyword Arguments:
            blocking {bool} -- If set to 'True', the figure is displayed immediately and the program waits until the figure is closed. Otherwise it waits until a blocking show() somewhere else in the program is called. (default: {True})
        """
        if with_cars:
            grid = self.get_grid()
            masked_grid = np.ma.masked_where(grid == CAR_VALUE, grid)
            plt.imshow(masked_grid, cmap=cmap)
        else:
            plt.imshow(self.model, cmap=cmap)

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

    def step(self, i, grid):
        if DEBUG:
            print("== Iteration {} ==".format(i))
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
        '''

        self.cars_on_round = []
        self.cars_not_round = []

        # Define which cars are on the roundabout.
        if not self.collision():
            for car in self.cars:
                if (car.cur_pos[0] >= self.model.points[0][0][0] and car.cur_pos[0] <= self.model.points[0][1][0]) and \
                (car.cur_pos[1] >= self.model.points[0][0][1] and car.cur_pos[1] <= self.model.points[0][1][1]):
                    self.cars_on_round.append(car)
                else:
                    self.cars_not_round.append(car)
        else:
            sys.exit(1)

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
            for i in range(2):
                if np.array_equal(car.cur_pos, self.exceptions[i]):
                    if car.orientation == SOUTH:
                        state = 7
                    else:
                        state = 5
            for i in range(2, 4):
                if np.array_equal(car.cur_pos, self.exceptions[i]):
                    if car.orientation == EAST:
                        state = 7
                    else:
                        state = 5
            for i in range(4, 6):
                if np.array_equal(car.cur_pos, self.exceptions[i]):
                    if car.orientation == NORTH:
                        state = 7
                    else:
                        state = 5
            for i in range(6, 8):
                if np.array_equal(car.cur_pos, self.exceptions[i]):
                    if car.orientation == WEST:
                        state = 7
                    else:
                        state = 5

        if state == 3:
            car.turn_left()
        elif state == 6:
            car.turn_ctr += 1
            turn = np.random.binomial(1, p=(car.turn_ctr * (1/4)))
            if turn == 1:
                car.turn_right()
        elif state == 7:
            car.turn_right()
        elif state == 9:
            car.turn_right()
            if self.offside_priority(car):
                car.drive()
                car.turn_left()
            else:
                car.turn_left()
        elif state == 10:
            car.turn_left()
            if self.offside_priority(car):
                car.drive()
                car.turn_right()
            else:
                car.turn_right()

        car.drive()

    def drive_outside(self, car):
        r, c = car.cur_pos
        state = self.model.grid[r][c]

        # Check if nothing is in front of the car
        if self.offside_priority(car):
            if state == 1:
                self.free_starts = np.append(
                    self.free_starts, [car.cur_pos], axis=0)
            elif state == 2:
                car.toggle_active()
                self.n_finished += 1
                return
            car.drive()

    def offside_priority(self, car):
        check_pos = car.cur_pos
        if car.orientation == NORTH:
            check_pos = check_pos + [-1, 0]
        elif car.orientation == EAST:
            check_pos = check_pos + [0, 1]
        elif car.orientation == SOUTH:
            check_pos = check_pos + [1, 0]
        else:
            check_pos = check_pos + [0, -1]

        for vehicle in self.cars:
            if np.array_equal(vehicle.cur_pos, check_pos):
                return False
        return True

    def collision(self):
        if len(np.unique(self.cars, axis=0)) == len(self.cars):
            return False
        return True
