#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import scipy.stats as spstats
import itertools as ittool

import fnmatch
import os

ROUNDABOUTS = ['regular', 'turbo', 'magic']
DENSITY = np.arange(0.5, 10, 0.5)/10
STEPS = 1000
ASSHOLE_PROB = [0, 0.05, 0.1, 0.15, 0.2, 0.25]

plt.rc('font', family='serif')
plt.style.use('seaborn-poster')


def read_data(test=True):
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

    if test:
        ttest(r_data)

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


def ttest(data, test_ass=False, test_round=False):
    if test_ass:
        for i in range(len(ROUNDABOUTS)):
            print('=========================')
            print('========= {} ========='.format(ROUNDABOUTS[i]))
            data_reg = []
            for asshole in data[i]:
                data_ass = []
                for d in asshole:
                    throughput = d[:, 1]/STEPS
                    data_ass.append(np.mean(throughput))
                data_reg.append(data_ass)

            iters = list(ittool.combinations(range(6), 2))
            for i in iters:
                print('== {} vs {} =='.format(ASSHOLE_PROB[i[0]], ASSHOLE_PROB[i[1]]))
                t, p = spstats.ttest_ind(data_reg[i[0]], data_reg[i[1]])
                print('t-stat: {}'.format(abs(round(t, 5))))
                print('p-value: {}\n'.format(round(p, 5)))
    
    if test_round:
        iters = list(ittool.combinations(range(3), 2))
        for i in iters:
            print('== {} vs {} =='.format(ROUNDABOUTS[i[0]], ROUNDABOUTS[i[1]]))
            data_a = []
            for d in data[i[0]][0]:
                throughput = d[:, 1]/STEPS
                data_a.append(np.mean(throughput))
            
            data_b = []
            for d in data[i[1]][0]:
                throughput = d[:, 1]/STEPS
                data_b.append(np.mean(throughput))
            
            t, p = spstats.ttest_ind(data_a, data_b)
            print('t-stat: {}'.format(abs(round(t, 5))))
            print('p-value: {}\n'.format(round(p, 5)))

if __name__ == '__main__':
    data = read_data()
    make_graph(data, error=True, save=False)
    plt.show()
