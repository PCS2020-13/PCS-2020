import numpy as np
from numpy.lib.recfunctions import append_fields
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.animation as animation

from utils import (DEBUG, random_row, NORTH, EAST, SOUTH, WEST)
from car import Car

CAR_VALUE = -1

# Define car color
cmap = cm.Dark2
cmap.set_bad(color='red')

class RoundaboutSim():
    def __init__(self, model_path, show_animation=True):
        self.model = np.loadtxt(model_path, dtype=int)
        self.cars = []

        self.start_states = np.argwhere(self.model==1)
        assert self.start_states.size != 0, 'This roundabout contains no start states.'
        self.end_states = np.argwhere(self.model==2)
        assert self.end_states.size != 0, 'This roundabout contains no end states.'

        self.show_animation = show_animation

    def __repr__(self):
        return '\n'.join([np.array2string(row)[1:-1] for row in self.model])

    def read_input(self, path):
        """ MAYBE DEPRECATED

        Create a roundabout model from an input file. On creation, a roundabout does not yet contain any cars.

        Arguments:
            path {string} -- The path that contains the input file.

        Returns:
            np.array -- A 2D numpy array consisting of tuples that show the type of a tile and whether there is a car on that tile.
        """
        with open(path) as f:
            model = [[(x, None) for x in line.split(' ')] for line in f]

        dtype = [('type', int), ('car', object)]
        return np.array(model, dtype=dtype)

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

    def get_grid(self):
        grid = np.copy(self.model)

        for car in self.cars:
            r, c = car.cur_pos
            grid[r][c] = CAR_VALUE

        masked_grid = np.ma.masked_where(grid == CAR_VALUE, grid)
        return masked_grid

    def initialize(self, n_cars=1, animate=True):
        self.cars=[]

        for _ in range(n_cars):
            start_pos = random_row(self.start_states)[0]
            end_pos = random_row(self.end_states)[0]
            orientation = self.get_start_orientation(start_pos)
            car = Car(orientation, start_pos, end_pos)
            self.cars.append(car)

        if DEBUG:
            print(self.cars)

        if animate:
            fig = plt.figure()
            frame = plt.gca()
            frame.axes.get_xaxis().set_visible(False)
            frame.axes.get_yaxis().set_visible(False)

            cmap = cm.Dark2
            cmap.set_bad(color='red')
            grid = self.get_grid()
            masked_grid = np.ma.masked_where(grid == CAR_VALUE, grid)
            sim_grid = plt.imshow(masked_grid, cmap=cmap)

            anime = animation.FuncAnimation(fig, self.step,
                                            fargs=(sim_grid,),
                                            frames=10, #DETERMINE!!
                                            interval=1000,
                                            blit=False)

            plt.show()

    def step(self, i, grid):
        self.process_cars()
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
            state = self.model[r][c]

            if state == 3:
                car.turn_right
            elif state == 7:
                car.turn_right()

            elif state == 2:
                car.toggle_active()
                return

            car.drive()

        if DEBUG:
            print(self.cars)
