import numpy as np
from numpy.lib.recfunctions import append_fields
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

class RoundaboutSim():
    def __init__(self, roundabout, show_animation=True):
        self.exceptions = roundabout.exceptions
        self.roundabout_area = roundabout.area
        self.model = roundabout.grid
        self.cars = []

        self.start_states = np.argwhere(self.model==1)
        assert self.start_states.size != 0, 'This roundabout contains no start states.'
        self.end_states = np.argwhere(self.model==2)
        assert self.end_states.size != 0, 'This roundabout contains no end states.'

        self.show_animation = show_animation

    def __repr__(self):
        return '\n'.join([np.array2string(row)[1:-1] for row in self.model])


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

    def initialize(self, n_cars=5, animate=True):
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

            # Little function that stops the animation when all cars have disappeared
            def gen():
                i = 0
                while self.cars != []:
                    i += 1
                    yield i

            anime = animation.FuncAnimation(fig, self.step,
                                            fargs=(sim_grid,),
                                            frames=gen, #DETERMINE!!
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

        self.cars_on_round = []
        self.cars_not_round = []

        # Define which cars are on the roundabout.
        if not self.collision():
            for car in self.cars:
                if (car.cur_pos[0] > 1 and car.cur_pos[0] < 9) and \
                (car.cur_pos[1] > 1 and car.cur_pos[1] < 9):
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

        # remove all cars that have finished
        self.cars = [car for car in self.cars if car.active]

        if DEBUG:
            print(self.cars)

    def drive_roundabout(self, car):
        r, c = car.cur_pos
        state = self.model[r][c]

        # state 8 defines the exceptions
        if state == 8:
            for i in range(4):
                grid = i
                if np.array_equal(car.cur_pos, self.exceptions[i]):
                    # only count the turns for the middle parts of the roundabout
                    car.turn_ctr += 1
                    if car.orientation == np.abs(2 - grid) %4:
                        state = 5
                    elif car.orientation == np.abs(2 - (grid + 1)) %4:
                        state = 4
            for i in range(4, 8):
                grid = i
                if np.array_equal(car.cur_pos, self.exceptions[i]):
                    car.turn_ctr += 1
                    if car.orientation == np.abs(2 + grid) %4:
                        state = 6
                    elif car.orientation == np.abs(2 + (grid + 1)) %4:
                        state = 4

        if car.turn_ctr == 0:
            turn = 0
        else:
            turn = np.random.binomial(1, p=((car.turn_ctr-1) * 1/3))
        outer_turn = np.random.binomial(1, p=(car.turn_ctr * (1/4)))

        if state == 3:
            car.turn_left()
        elif state == 4:
            if turn == 0 or outer_turn == 0:
                car.turn_left()
        elif state == 6:
            if outer_turn == 0:
                car.turn_right()
        elif state == 7:
            car.turn_right()
        
        car.drive()

    def drive_outside(self, car):
        r, c = car.cur_pos
        state = self.model[r][c]

        # Check if nothing is in front of the car
        if self.offside_priority(car):
            print('yes you have checked')
            if state == 2:
                car.toggle_active()
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