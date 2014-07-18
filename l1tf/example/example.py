import csv
from matplotlib import pyplot as plt 
import numpy as np
from l1tf import l1tf, remove_outliers
import pandas as pd


# Downloaded from http://www.barchartmarketdata.com/datasamples/US%20Futures%20Tick%20Query.csv 
with open('US Futures Tick Query.csv') as f:
    lines = list(csv.reader(f))

x = pd.Series(np.asarray([float(e[-2]) for e in lines]))

#plt.figure()
#
#for i, delta in enumerate([1, 10, 50, 100]):
#    plt.subplot(2,2,i+1)
#    filtered = l1tf(x, delta)
#    plt.plot(x, label='Original data')
#    plt.plot(filtered, linewidth=5, label='Filtered, delta=%s' % delta, alpha=0.5)
#    plt.legend(loc='best')
#
# Adding outliers


outliers_percentaje = 0.05
outliers = np.random.random(len(x)) < outliers_percentaje 

x[outliers] = np.random.random(outliers.sum()) * 2 + x[outliers]

plt.figure()

for i, mad_factor in enumerate([1, 3, 10, 30]):
    plt.subplot(2,2,i+1)
    x_wo_outliers = remove_outliers(x, delta=1, mad_factor=mad_factor)
    plt.plot(x, label='Original data')
    plt.plot(x_wo_outliers, linewidth=5, label='Without outliers, mad_factor=%s' % mad_factor, alpha=0.5)
    plt.legend(loc='best')

plt.show()


