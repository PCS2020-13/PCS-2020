#!/usr/bin/env python3

import argparse

import pandas as pd
import numpy as np

from simulator import RoundaboutSim
from roundabout import (Regular, Turbo, Magic)
from utils import (h5load, h5store)

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
                        help='show the animations')
    parser.add_argument('-o', '--output', nargs='?', default=False,
                        help='store the results in an output file specified by the given directory')
    parser.add_argument('-p', '--print', action='store_true',
                        help='print the results to stdout')
    args = parser.parse_args()

    if args.roundabout == 'regular':
        roundabout = Regular()
    elif args.roundabout == 'turbo':
        roundabout = Turbo()
    elif args.roundabout == 'magic':
        roundabout = Magic()
    else:
        raise TypeError('Roundabout does not exist.')

    r = RoundaboutSim(roundabout, density=args.density,
                      steps=args.iterations, show_animation=args.animate)

    columns = ['n_total', 'n_finished', 'turns_avg', 'turns_std']
    df = pd.DataFrame(columns=columns)

    metadata = {
        'roundabout': args.roundabout,
        'density': args.density,
        'iterations': args.iterations
    }

    for n in range(args.simulations):
        r.reset()
        r.run()
        n_finished = r.n_finished
        n_total = n_finished + len(r.cars)
        turns_avg = np.mean(r.turns_per_car)
        turns_std = np.std(r.turns_per_car)
        data = [float(n_total), float(n_finished), turns_avg, turns_std]
        df_temp = pd.DataFrame(dict(zip(columns, data)), index=[0])
        df = df.append(df_temp, ignore_index=True)

    if args.print:
        print(df)

    if args.output:
        filename = '{}/{}_{}_{}.h5'.format(args.output,
                                        args.roundabout,
                                        args.density,
                                        args.iterations)
        h5store(filename, df, **metadata)
