#!/usr/bin/env python3

###
# main.py
#
# Driver program for running roundabout simulations.
# This program can be called from the command-line with different options.
# Run './main.py -h' for a complete overview of all options.
###

import argparse

import pandas as pd
import numpy as np

from simulator import RoundaboutSim
from roundabout import (Regular, Turbo, Magic)

from concurrent import futures


def run_sim(roundabout, density, steps):
    """Run a simulation and return the results. Only used when multithreading is enabled.

    Arguments:
        roundabout {Roundabout} -- The roundabout to be used.
        density {float} -- The car density.
        steps {int} -- The number of iterations to run the simulation.

    Returns:
        data -- The results from running the simulation.
    """
    r = RoundaboutSim(roundabout, density=density,
                      steps=steps, show_animation=False)
    r.run()
    n_finished = r.n_finished
    n_total = n_finished + len(r.cars)
    turns_avg = np.mean(r.turns_per_car)
    turns_std = np.std(r.turns_per_car)
    n_waiting = r.waiting_cars
    data = (n_total, n_finished, turns_avg, turns_std, n_waiting)
    return data


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Driver program for running roundabout simulations.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('roundabout',
                        choices=['regular', 'turbo', 'magic'],
                        type=str,
                        help='roundabout type')
    parser.add_argument('-d', '--density', default=0.5,
                        type=float, help='car density')
    parser.add_argument('-i', '--iterations', default=1000,
                        type=int, help='number of iterations')
    parser.add_argument('-s', '--simulations', default=10,
                        type=int, help='number of simulations')
    parser.add_argument('-a', '--animate', action='store_true',
                        help='show the animations (automatically disabled in \
                              combination with --multithreading)')
    parser.add_argument('-o', '--output', nargs='?', default=False,
                        help='store the results in an output file specified by \
                              the given directory')
    parser.add_argument('-p', '--print', action='store_true',
                        help='print the results to stdout')
    parser.add_argument('-m', '--multithreading', action='store_true',
                        help='use multithreading to speed up the simulation \
                              process')
    parser.add_argument('-A', '--asshole_probability', default=0, type=float,
                        help='asshole probability for a car')

    args = parser.parse_args()

    assert args.density > 0.0 and args.density < 1.0, 'Density should be in range (0, 1)'

    if args.roundabout.lower() == 'regular':
        roundabout = Regular()
    elif args.roundabout.lower() == 'turbo':
        roundabout = Turbo()
    elif args.roundabout.lower() == 'magic':
        roundabout = Magic()
    else:
        raise TypeError('Roundabout does not exist.')

    columns = ['n_total', 'n_finished', 'turns_avg', 'turns_std', 'n_waiting']
    df = pd.DataFrame(columns=columns)

    if args.multithreading:
        # Automatically uses the number of processors on the computer.
        with futures.ProcessPoolExecutor() as executor:
            future_to_roundabout = [executor.submit(
                run_sim, roundabout, args.density, args.iterations) for _ in range(args.simulations)]
            for future in futures.as_completed(future_to_roundabout):
                data = future.result()
                df = df.append(pd.DataFrame(
                    dict(zip(columns, data)), index=[0]), ignore_index=True,
                         sort=False)
    else:
        r = RoundaboutSim(roundabout, density=args.density,
                          steps=args.iterations, show_animation=args.animate)
        for n in range(args.simulations):
            r.reset()
            r.run()
            n_finished = r.n_finished
            n_total = n_finished + len(r.cars)
            turns_avg = np.mean(r.turns_per_car)
            turns_std = np.std(r.turns_per_car)
            n_waiting = r.waiting_cars
            data = [float(n_total), float(n_finished), turns_avg, turns_std,
                    n_waiting]
            df_temp = pd.DataFrame(dict(zip(columns, data)), index=[0])
            df = df.append(df_temp, ignore_index=True, sort=False)

    if args.print:
        print(df)

    if args.output:
        filename = '{}/{}_{}_{}_{}.csv'.format(args.output,
                                               args.roundabout,
                                               args.density,
                                               args.iterations,
                                               args.asshole_probability)
        df.to_csv(filename, index_label="i")
