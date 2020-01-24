#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import scipy.stats as spstats

import argparse
import fnmatch
import os

plt.rc('font', family='serif')
plt.style.use('seaborn-poster')

ROUNDABOUTS = ['regular', 'turbo', 'magic']
DENSITY = np.arange(0.5, 10, 0.5)/10
ASSHOLE_PROB = [0, 0.05, 0.1, 0.15, 0.2, 0.25]


def read_data(steps, asshole_probs):
    r_data = []
    for r in ROUNDABOUTS:
        a_data = []

        for a in asshole_probs:
            d_data = []

            for d in DENSITY:
                filename = 'output/{}_{}_{}_{}.csv'.format(r, d, steps, a)
                d_data.append(np.loadtxt(filename, skiprows=1,
                                         usecols=range(1, 5), delimiter=','))

            a_data.append(d_data)

        r_data.append(a_data)

    return r_data


def make_graph(data, steps, asshole_probs, save=False):
    for i, r in enumerate(ROUNDABOUTS):
        fig = plt.figure()

        for j, _ in enumerate(asshole_probs):
            avg_throughput = []
            err_throughput = []

            for d in data[i][j]:
                throughput = d[:, 1]/steps
                avg_throughput.append(np.mean(throughput))
                err_throughput.append(mean_confidence_interval(throughput))

            avg_throughput = np.array(avg_throughput)
            err_throughput = np.array(err_throughput)

            plt.fill_between(DENSITY, avg_throughput - err_throughput,
                                 avg_throughput + err_throughput, alpha=0.2)
            plt.plot(DENSITY, avg_throughput)

        plt.ylim(0, 3)
        plt.title('{} roundabout'.format(r.capitalize()))
        plt.xlabel('Density')
        plt.ylabel('Average throughput')
        plt.legend(asshole_probs, title='Asshole Probability', loc=4)

        if save:
            if not os.path.isdir('figures/'):
                os.mkdir('figures/')
            fig.savefig('figures/{}_{}.png'.format(r, steps),
                        transparant=True, bbox_inches='tight')


def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    se = spstats.sem(a)
    return se * spstats.t.ppf((1 + confidence) / 2., n - 1)


if __name__ == '__main__':
    STEPS = 1000

    parser = argparse.ArgumentParser(
        description='Program for processing and visualising roundabout simulation data',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('steps', type=int, default=1000, help='The number of simulation steps')
    parser.add_argument('asshole_probs', nargs='*', default=ASSHOLE_PROB, help='The asshole probabilities to use')
    parser.add_argument('-s', '--save', action='store_true', help='Save the figures')
    args = parser.parse_args()
    print(args)

    data = read_data(args.steps, args.asshole_probs)
    make_graph(data, args.steps, args.asshole_probs, save=args.save)
    plt.show()
