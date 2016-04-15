#!/usr/bin/env python

import pylab
import operator
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

fig = plt.figure()
ax = fig.add_subplot(111)
pos=[1,2,3,4,5,6,7]
neg=[8,9,10,11,12,13,14]
time=[0,1,2,3,4,5,6]
plt.xlabel("Time Step")
plt.ylabel("Word Count")
#plt.plot(time, pos, 'bo', time, pos, 'b', time, neg, 'go', time, neg, 'g')
plt.plot(time, pos, 'bo-', time, neg, 'go-')
ax.legend(('positive', 'negative'), loc='upper left')
#ax.legend(loc='upper left', shadow=True, fontsize='x-large')
ax1 = plt.subplot()
ax1.set_xlim(xmin=-1)
ax1.set_ylim(ymin=0)
ax1.set_autoscale_on(True)
plt.show()

