###
# simulator.py
# This file contains the RoundaboutSim class which performs the actual
# roundabout simulations.
###

import numpy as np
from numpy.random import RandomState

import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.animation as animation
import sys

from utils import (DEBUG, random_row, NORTH, EAST, SOUTH, WEST)
from car import Car
from magic import process_cars_magic
from regular_turbo import process_cars_reg

CAR_VALUE = -1


class RoundaboutSim():
    def __init__(self, model, density=0.05, steps=1000, show_animation=True,
                 asshole_probability=0):
        self.model = model
        self.aimed_density = density
        self.true_density = 0
        self.waiting_cars = 0
        self.steps = steps
        self.exceptions = model.exceptions
        self.asshole_probability = asshole_probability

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

    def set_steps(self, steps):
        """Sets the number of time steps the simulation should take.

        Arguments:
            steps {int} -- The number of time steps.
        """
        self.steps = steps

    def get_cars(self):
        """Returns a list of the cars currently on the grid.

        Returns:
            np.array -- An array containing the cars.
        """
        return self.cars

    def get_start_orientation(self, start_pos):
        """Helper function for determining the initial orientation of a car.

        Arguments:
            start_pos {(int, int)} -- A tuple with the x and y coordinates of
                                      the starting position.

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
        else:
            raise ValueError('No valid start position')

    def get_grid(self):
        """Creates a grid with all cars currently on the road. The cells that
           have a car on them will take on CAR_VALUE.

        Returns:
            np.array -- The model with all cars currently on the grid.
        """
        grid = np.copy(self.model.grid)

        for car in self.cars:
            r, c = car.cur_pos
            grid[r][c] = CAR_VALUE

        masked_grid = np.ma.masked_where(grid == CAR_VALUE, grid)
        return masked_grid

    def draw_model(self, with_cars=True, blocking=True, beautiful=True):
        """Draws the model of the roundabout.

        Keyword Arguments:
            with_cars {bool} -- If the model should be drawn with or without
                                cars on it. (default: {True})
            blocking {bool} -- If set to 'True', the figure is displayed
                               immediately and the program waits
                               until the figure is closed. Otherwise it waits
                               until a blocking show() somewhere else in the
                               program is called.
            (default: {True})
            beautiful {bool} -- Show the roundabout with nice asphalt colors.
                                (default: {True})
        """
        cmap = cm.get_cmap('Dark2')

        if beautiful:
            norm = cm.colors.Normalize(vmin=0.1, vmax=0.9)
        else:
            norm = cm.colors.Normalize(vmin=0.1)

        cmap.set_bad(color='red')
        cmap.set_under(color='green')
        cmap.set_over(color='grey')

        if with_cars:
            grid = self.get_grid()
            masked_grid = np.ma.masked_where(grid == CAR_VALUE, grid)
            plt.imshow(masked_grid, cmap=cmap)
        else:
            plt.imshow(self.model.grid, cmap=cmap)

        plt.axis('off')
        plt.show(block=blocking)

    def spawn_cars(self):
        """Spawns cars onto the roundabout so the aimed density is reached."""
        while self.free_starts.size != 0 and \
                self.true_density < self.aimed_density:
            start_pos = random_row(self.free_starts)[0]
            end_pos = random_row(self.end_states)[0]
            orientation = self.get_start_orientation(start_pos)

            # Define 'assholes' with a certain asshole factor that stop randomly in traffic.
            if RandomState().binomial(1, p=self.asshole_probability):
                car = Car(orientation, start_pos, end_pos, asshole_factor=0.05)
            else:
                car = Car(orientation, start_pos, end_pos)
            self.cars.append(car)
            self.true_density = len(self.cars) / self.road_size

            # Delete the start position from the list of possible starts
            self.free_starts = np.delete(self.free_starts, (np.where(
                (self.free_starts == start_pos).all(axis=1))[0][0]), axis=0)

    def reset(self):
        """Resets the simulation."""
        self.cars = []
        self.n_finished = 0
        self.true_density = 0
        self.free_starts = np.copy(self.start_states)

    def run(self, beautiful=True):
        """Initializes the simulation.

        Keyword Arguments:
            beautiful {bool} -- Show the roundabout with nice asphalt colors.
                                (default: {True})
        """
        self.spawn_cars()
        grid = self.get_grid()

        if DEBUG:
            print(self.cars)

        if self.show_animation:
            fig = plt.figure(figsize=(8, 8))
            fig.canvas.set_window_title("Roundabout simulator: {}".format(self.model.name))
            frame = plt.gca()
            frame.axes.get_xaxis().set_visible(False)
            frame.axes.get_yaxis().set_visible(False)

            cmap = cm.get_cmap('Dark2')

            if beautiful:
                norm = cm.colors.Normalize(vmin=0.1, vmax=0.9)
            else:
                norm = cm.colors.Normalize(vmin=0.1)

            cmap.set_bad(color='red')
            cmap.set_under(color='green')
            cmap.set_over(color='grey')

            sim_grid = plt.imshow(grid, cmap=cmap, norm=norm)
            sim_title = plt.title("")

            # Interval defines the time between different frames in ms.
            # The lower the number, the faster the animation.
            
            anim = animation.FuncAnimation(fig,
                                    self.step,
                                    fargs=(sim_grid,sim_title),
                                    interval=10,
                                    frames=self.steps,
                                    repeat=False
                                   )

            plt.show()

        else:
            for i in range(self.steps):
                self.step(i, grid)

        if DEBUG:
            print("== FINAL STATISTICS ==")
            print("CARS IN TOTAL: {}".format(len(self.cars)+self.n_finished))
            print("CARS FINISHED: {}".format(self.n_finished))
            print("CARS FINISHED PER STEP: {}".format(self.n_finished/self.steps))
            print("WAITING CARS: {}".format(self.waiting_cars))
            print("AVERAGE WAITING PER CARS: {}".format(round(self.waiting_cars/(len(self.cars)+self.n_finished), 3)))
            print("AVERAGE WAITING PER STEP: {}".format(round(self.waiting_cars/self.steps, 3)))
            print("======================")

    def step(self, i, grid, title=None):
        """Calculates the state of the roundabout in the next time step.

        Arguments:
            i {int} -- The frame number
            grid {plt.figure} -- A matplotlib figure containing the current
                                 state of the roundabout.

        Returns:
            plt.figure -- The new state of the roundabout.
        """
        if DEBUG:
            print("== Iteration {} ==".format(i))

        self.process_cars()
        self.spawn_cars()

        if self.show_animation:
            title.set_text("step = {}\ndensity = {}".format(i + 1, round(self.true_density, 3)))
            grid.set_data(self.get_grid())

        return grid,

    def process_cars(self):
        """Process the cars. The next step of a car depends on the state of the
           current cell it is on. This can be one of the following states:
        0 = Grass (non-road)
        1 = Start
        2 = Stop
        3 = Left
        4 = Left and straight
        5 = Straight
        6 = Right and straight
        7 = Right
        8 = Exception
        9 = Switch to right lane
        10 = Switch to left lane
        """

        if self.model.name == 'Magic':
            process_cars_magic(self)
        else:
            process_cars_reg(self)

        # Delete cars that are finished from the self.cars list.
        self.cars = list(filter(lambda c: c.active, self.cars))
        self.true_density = len(self.cars) / self.road_size

        if DEBUG:
            print("CARS ON THE ROAD: {}".format(len(self.cars)))
            print("DENSITY: {}".format(self.true_density))
            print("CARS FINISHED: {}".format(self.n_finished))

    def priority(self, car, orientation):
        """Check whether a car has priority and can drive.

        Arguments:
            car {Car} -- The car that should drive
            orientation {int} -- The orientation that the car should turn to.

        Returns:
            bool -- Whether the car can drive.
        """
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
        """Checks whether a collision has happened.

        Returns:
            bool -- Whether a collision has happened.
        """
        cur_pos = [car.cur_pos for car in self.cars]
        if len(np.unique(cur_pos, axis=0)) == len(cur_pos):
            return False
        return True
