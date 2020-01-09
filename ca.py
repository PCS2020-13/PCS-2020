#!/usr/bin/env python3

import cellpylib as cpl

ca = cpl.init_random2d(30, 30, k=3)

ca = cpl.evolve2d(ca, 30, lambda n, c, t: cpl.totalistic_rule(n, 2, 126), neighbourhood='Moore')

cpl.plot2d_animate(ca)
