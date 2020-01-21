#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

import fnmatch
import os

ROUNDABOUTS = ['regular', 'turbo', 'magic']
STEPS = 250 #TEMPORARY
ASSHOLE_PROB = 0 #TEMPORARY

if __name__ == '__main__':
    x = np.arange(1, 10) / 10
    print(x)
    for r in ROUNDABOUTS:
        avg_throughput = []
        std_throughput = []
        fig = plt.figure()

        for d in range(1, 10):
            filename = "output/{}_{}_{}_{}.csv".format(r, d/10, STEPS, ASSHOLE_PROB)
            data = np.loadtxt(filename, skiprows=1, usecols=range(1,5), delimiter=',')
            n_finished = data[:,1]
            throughput = (n_finished) / STEPS
            avg_throughput.append(np.mean(throughput))
            std_throughput.append(np.std(throughput))

        plt.errorbar(x, avg_throughput, yerr=std_throughput)
        plt.ylim(0, 3)
        plt.title(r)
    plt.show()
