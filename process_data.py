#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import scipy.stats as spstats

import fnmatch
import os

ROUNDABOUTS = ['regular', 'turbo', 'magic']
DENSITY = np.arange(0.5, 10, 0.5)/10
STEPS = 1000
ASSHOLE_PROB = [0, 0.05, 0.1]

plt.rc('text', usetex=True)
plt.rc('font', family='serif')
plt.style.use('seaborn-poster')


def read_data():
    r_data = []
    for r in ROUNDABOUTS:
        a_data = []

        for a in ASSHOLE_PROB:
            d_data = []

            for d in DENSITY:
                filename = 'output/{}_{}_{}_{}.csv'.format(r, d, STEPS, a)
                d_data.append(np.loadtxt(filename, skiprows=1,
                                         usecols=range(1, 5), delimiter=','))

            a_data.append(d_data)

        r_data.append(a_data)

    return r_data


def make_graph(data, error=False, save=False):
    for i, r in enumerate(ROUNDABOUTS):
        fig = plt.figure()

        for j, _ in enumerate(ASSHOLE_PROB):
            avg_throughput = []
            err_throughput = []

            for d in data[i][j]:
                throughput = d[:, 1]/STEPS
                avg_throughput.append(np.mean(throughput))
                err_throughput.append(mean_confidence_interval(throughput))

            avg_throughput = np.array(avg_throughput)
            err_throughput = np.array(err_throughput)

            if error:
                plt.fill_between(DENSITY, avg_throughput - err_throughput,
                                 avg_throughput + err_throughput, alpha=0.2)

            plt.plot(DENSITY, avg_throughput)

        plt.ylim(0, 3)
        plt.title('{} roundabout'.format(r.capitalize()))
        plt.xlabel('Density')
        plt.ylabel('Average throughput')
        plt.legend(ASSHOLE_PROB, title='Asshole Probability', loc=4)

        if save:
            fig.savefig('figures/{}.pdf'.format(r),
                        transparant=True, bbox_inches='tight')
            fig.savefig('figures/{}.png'.format(r),
                        transparant=True, bbox_inches='tight')


def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    se = spstats.sem(a)
    return se * spstats.t.ppf((1 + confidence) / 2., n - 1)


if __name__ == '__main__':
    data = read_data()
    make_graph(data, error=True, save=True)
    plt.show()
