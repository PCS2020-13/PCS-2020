#!/usr/bin/env python3

import argparse

import pandas as pd
import numpy as np

from simulator import RoundaboutSim
from roundabout import (Regular, Turbo, Magic)

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
                        type=int, help='number of iterations (multiple possible)')
    parser.add_argument('-s', '--simulations', default=10,
                        type=int, help='number of simulations')
    parser.add_argument('-a', '--animate', action='store_true',
                        help='show the animations')
    args = parser.parse_args()
    print(args)

    if args.roundabout == 'regular':
        roundabout = Regular()
    elif args.roundabout == 'turbo':
        roundabout = Turbo()
    elif args.roundabout == 'magic':
        roundabout = Magic()
    else:
        raise TypeError('Roundabout does not exist.')

    r = RoundaboutSim('input/regular_roundabout.input', density=args.density,
                      steps=args.iterations, show_animation=args.animate)

    columns = ['n_finished', 'turns_avg', 'turns_std']
    df = pd.DataFrame(columns=columns)
    df.roundabout = args.roundabout
    df.density = args.density
    df.iterations = args.iterations
    print(df)

    for n in range(args.simulations):
        r.reset()
        r.run()
        turns_avg = np.mean(r.turns_per_car)
        turns_std = np.std(r.turns_per_car)
        data = [r.n_finished, turns_avg, turns_std]
        df_temp = pd.DataFrame(dict(zip(columns, data)), index=[0])
        df = df.append(df_temp, ignore_index=True)

    print(df)
