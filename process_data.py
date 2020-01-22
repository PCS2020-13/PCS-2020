#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

import fnmatch
import os

ROUNDABOUTS = ['regular', 'turbo', 'magic']
DENSITY = np.arange(0.5, 10, 0.5)/10
STEPS = 1000
ASSHOLE_PROB = [0, 0.1]

def read_data(ROUNDABOUTS, DENSITY, STEPS, ASSHOLE_PROB):
    r_data = []
    for r in ROUNDABOUTS:
        a_data = []
        for a in ASSHOLE_PROB:
            d_data = []
            for d in DENSITY:
                filename = 'output/{}_{}_{}_{}.csv'.format(r, d, STEPS, a)
                d_data.append(np.loadtxt(filename, skiprows=1, 
                                         usecols=range(1,5), delimiter=','))
            a_data.append(d_data)
        r_data.append(a_data)
    return r_data

def make_graph(data, ROUNDABOUTS, DENSITY, STEPS, ASSHOLE_PROB, error=False):
    fig, axs = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle('Average traffic flow of each roundabout per density')
    for i,r in enumerate(ROUNDABOUTS):
        for j,a in enumerate(ASSHOLE_PROB):
            avg_throughput = []
            std_throughput = []
            for d in data[i][j]:
                throughput = d[:,1]/STEPS
                avg_throughput.append(np.mean(throughput))
                std_throughput.append(np.std(throughput))

            if error:
                axs[i].errorbar(DENSITY, avg_throughput, yerr=std_throughput)
            else:
                axs[i].plot(DENSITY, avg_throughput)
        axs[i].set_ylim(0,3)
        axs[i].set_title(r)
        axs[i].set_xlabel('Density')
        axs[i].set_ylabel('Average throughput')
        plt.legend(ASSHOLE_PROB, title='Asshole Probability', loc=4)#, bbox_to_anchor=(1.45, 1))

if __name__ == '__main__':
    data = read_data(ROUNDABOUTS, DENSITY, STEPS, ASSHOLE_PROB)
    make_graph(data, ROUNDABOUTS, DENSITY, STEPS, ASSHOLE_PROB)
    plt.show()
