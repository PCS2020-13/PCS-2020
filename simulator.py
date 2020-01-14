import numpy as np
from numpy.random import binomial

import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.animation as animation

from utils import (DEBUG, random_row, NORTH, EAST, SOUTH, WEST)
from car import Car

CAR_VALUE = -1

# Define car color
cmap = cm.Dark2
cmap.set_bad(color='red')

####
# TODO: - asshole_factor
#       - dick_move()
####


class RoundaboutSim():
    def __init__(self, model, density=0.5, steps=100, show_animation=True):
        # self.model = np.loadtxt(model_path, delimiter = ' ', dtype=int)
        self.model = model
        self.aimed_density = density
        self.true_density = 0
        self.steps = steps

        self.road_size = (self.model.grid != 0).sum()
        self.n_finished = 0

        self.start_states = np.argwhere(self.model.grid == 1)
        assert self.start_states.size != 0, 'This roundabout contains no start states.'
        self.end_states = np.argwhere(self.model.grid == 2)
        assert self.end_states.size != 0, 'This roundabout contains no end states.'

        self.free_starts = np.copy(self.start_states)
        self.cars = []

        self.show_animation = show_animation

    def __repr__(self):
        return '\n'.join([np.array2string(row)[1:-1] for row in self.model.grid])

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
        for car in self.cars:
            r, c = car.cur_pos
            state = self.model.grid[r][c]

            exceptions = [[3, 3], [3, 7], [7, 7], [
                7, 3], [2, 2], [2, 8], [8, 8], [8, 2]]
            turn = 1/3 * car.turn_ctr

            if self.offside_priority(car):
                for i in range(4):
                    grid = i
                    if np.array_equal(car.cur_pos, exceptions[i]):
                        if car.orientation == (2 - grid) % 4:
                            state = 5
                        elif car.orientation == (2 - (grid + 1)) % 4:
                            state = 4
                for i in range(4, 8):
                    grid = i
                    if np.array_equal(car.cur_pos, exceptions[i]):
                        if car.orientation == (2 + grid) % 4:
                            state = 6
                        elif car.orientation == (2 + (grid + 1)) % 4:
                            state = 5

                if state == 1:
                    self.free_starts = np.append(
                        self.free_starts, [car.cur_pos], axis=0)
                elif state == 2:
                    car.toggle_active()
                    self.n_finished += 1
                    break
                elif state == 3:
                    car.turn_left()
                elif state == 4:
                    if turn:
                        car.turn_left()
                elif state == 6:
                    if turn:
                        car.turn_right()
                elif state == 7:
                    car.turn_right()
                elif state == 8:
                    for i in range(4):
                        grid = i
                        if np.array_equal(car.cur_pos, exceptions[i]):
                            # only count the turns for the middle parts of the roundabout
                            car.turn_ctr += 1
                            if car.orientation == np.abs(2 - grid) %4:
                                state = 5
                            elif car.orientation == np.abs(2 - (grid + 1)) %4:
                                state = 4
                    for i in range(4, 8):
                        grid = i
                        if np.array_equal(car.cur_pos, exceptions[i]):
                            if car.orientation == np.abs(2 + grid) %4:
                                state = 6
                            elif car.orientation == np.abs(2 + (grid + 1)) %4:
                                state = 5

            car.drive()

        self.cars = list(filter(lambda c: c.active, self.cars))
        self.true_density = len(self.cars) / self.road_size

        # remove all cars that have finished
        self.cars = [car for car in self.cars if car.active]

        if DEBUG:
            print("CARS ON THE ROAD: {}".format(len(self.cars)))
            print("DENSITY: {}".format(self.true_density))
            print("CARS FINISHED: {}".format(self.n_finished))


    # NOG NIET ECHT WERKEND
    def offside_priority(self, car):
        check_pos = car.cur_pos
        if car.orientation == NORTH:
            check_pos = check_pos + [-1, -1]
        elif car.orientation == EAST:
            check_pos = check_pos + [-1, 1]
        elif car.orientation == SOUTH:
            check_pos = check_pos + [1, 1]
        else:
            check_pos = check_pos + [1, -1]

        for vehicle in self.cars:
            if np.array_equal(vehicle.cur_pos, check_pos):
                return False
        return True
