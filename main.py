#!/usr/bin/env python3

import argparse

import pandas as pd

from simulator import RoundaboutSim
from roundabout import (Roundabout, Regular, Turbo, Magic)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Driver program for running roundabout simulations.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('roundabout',
                        choices=['regular', 'turbo', 'magic'],
                        type=str,
                        help='roundabout type')
    parser.add_argument('-d', '--density', default=0.5, type=float, help='car density')
    parser.add_argument('-i', '--iterations', default=1000, type=int, help='number of iterations (multiple possible)')
    parser.add_argument('-s', '--simulations', default=10, type=int, help='number of simulations')
    parser.add_argument('-a', '--animate', action='store_true', help='show the animations')
    args = parser.parse_args()
    print(args)


    r = RoundaboutSim(roundabout_path, density=args.density, steps=args.iterations, show_animation=args.animate)
    df = pd.DataFrame()

    for n in range(args.simulations):
        r.reset()
        r.run()
        print(r.n_finished)
