#!/usr/bin/env python
"""@package SENSOR
   \mainpage SENSOR
   \author Alessandro Filisetti
     
	Statistical functions.
"""

# from numpy import arange#,array,ones,linalg
from numpy import arange, poly1d, polyfit, linspace
from scipy import stats
from scipy.optimize import curve_fit
import pylab
import numpy as np


# from pylab import plot,show

def linearregression(tmpTime, tmpY):
    '''
        Compute linear regression
    '''

    t = arange(0, tmpTime)
    slope, intercept, r_value, p_value, std_err = stats.linregress(t, tmpY)

    # 	line = slope*t+intercept
    # 	plot(t,line,'r-',t,envi.totSolarBasedKW,'o')
    # 	show()

    # print "**** LINEAR REGRESSION\n\t|-Slope: {0} - Intercept: {1} - r_value: {2} - p_value: {3} - str_err: {4}".format(slope, intercept, r_value, p_value, std_err)

    return slope, intercept, r_value, p_value, std_err


def polynomialregression(x, y, polDegree):
    # fit the data with a 4th degree polynomial
    z, res, _, _, _ = polyfit(x, y, polDegree, full=True)
    p = poly1d(z)  # construct the polynomial

    print z
    print p
    print res

    xx = linspace(0, max(x), len(y))
    pylab.plot(x, y, 'o', xx, p(xx), '-g')
    pylab.legend(['data to fit', '2th degree poly'])
    # pylab.axis([0,1,0,1])
    pylab.show()

    return z, res


def curveFitting(x, y):
    '''
        Curve fitting function
        :param x: curve to fit
        :param y: banchmark curve
    '''

    return np.sqrt((sum([pow(i - x[id], 2) for id, i in enumerate(y)])) / (len(x) - 1))
