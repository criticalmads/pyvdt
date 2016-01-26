#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2011, 2015, Aarhus University (http://www.au.dk/en/).

This file is part of PyVDT.

PyVDT is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

PyVDT is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with PyVDT.  If not, see <http://www.gnu.org/licenses/>.

Additional license terms:

In accordance with Section 7(b) of the GNU General Public License
version 3, modified versions of this software must preserve the
original copyright notices within the source code files.
"""

import math

# The adjustment avoids infinite d' values by adding 0.5 to all data cells
# (hits, misses, false alarms, correct rejections) regardless of whether
# zeroes are present.
# See Macmillan & Creelman "Detection Theory: A User's Guide", 2nd edition,
# pp. 8-9.
#
# d' = 4.65 is considered an effective maximum (Macmillan & Creelman, 2008, p. 8)

def Hrate(hits, misses, adjustment=False):
    """Calculates and returns H (hit rate)
    >>> Hrate(20,5)
    0.8
    >>> Hrate(0,0,True)
    0.5
    >>> Hrate(0,0)
    -1
    """
    if hits==0 and misses==0 and adjustment==False: return -1 #division; TODO: fix
    
    if adjustment==True:
        hits=hits+0.5
        misses=misses+0.5
        
    if misses>0:
        H = float(hits)/(hits+misses)
    else:
        H = (hits - 0.5)/(hits+misses)
    
    #TODO: add other adjustments (Macmillan & Creelman; Corwin, 1994) 
    #if adjustment==1 and H=1:
    
    return H

def Frate(falseAlarms, correctRejections, adjustment=False):
    """Calculates and returns F (false-alarm rate)
    >>> Frate(10,15)
    0.4
    >>> Frate(0,0,True)
    0.5
    >>> Frate(0,0)
    -1
    """
    if falseAlarms==0 and correctRejections==0 and adjustment==False: return -1 #division by zero; TODO: fix

    if adjustment==True:
        falseAlarms=falseAlarms+0.5
        correctRejections=correctRejections+0.5

    if falseAlarms>0:
        F = float(falseAlarms)/(falseAlarms+correctRejections)
    else:
        F = 0.5/(falseAlarms+correctRejections)

    #TODO: add other adjustments (Macmillan & Creelman; Corwin, 1994) 
    #if adjustment==1:

    return F

def normsinv(p):
    """Returns the quantile function (aka percent point function/inverse cumulative distribution function)
    >>> round(normsinv(0.1),7)
    -1.2815516
    >>> round(normsinv(0.15),7)
    -1.0364334
    >>> normsinv(0)
    
    """
    # Adapted from LGPL-licensed Visual Basic code written by Christian d'Heureuse.
    # Original code available at: http://www.source-code.biz/snippets/vbasic/9.htm
    a1 = -39.6968302866538
    a2 = 220.946098424521
    a3 = -275.928510446969
    a4 = 138.357751867269
    a5 = -30.6647980661472
    a6 = 2.50662827745924
    b1 = -54.4760987982241
    b2 = 161.585836858041
    b3 = -155.698979859887
    b4 = 66.8013118877197
    b5 = -13.2806815528857
    c1 = -7.78489400243029E-03
    c2 = -0.322396458041136
    c3 = -2.40075827716184
    c4 = -2.54973253934373
    c5 = 4.37466414146497
    c6 = 2.93816398269878
    d1 = 7.78469570904146E-03
    d2 = 0.32246712907004
    d3 = 2.445134137143
    d4 = 3.75440866190742
    p_low = 0.02425
    p_high = 1 - p_low
    if p <= 0 or p >= 1:
        return None #TODO: throw error
    elif p < p_low:
        q = math.sqrt(-2 * math.log(p))
        z = (((((c1 * q + c2) * q + c3) * q + c4) * q + c5) * q + c6) / \
             ((((d1 * q + d2) * q + d3) * q + d4) * q + 1)
    elif p <= p_high:
        q = p - 0.5
        r = q * q
        z = (((((a1 * r + a2) * r + a3) * r + a4) * r + a5) * r + a6) * q / \
            (((((b1 * r + b2) * r + b3) * r + b4) * r + b5) * r + 1)
    else:
        q = math.sqrt(-2 * math.log(1 - p))
        z = -(((((c1 * q + c2) * q + c3) * q + c4) * q + c5) * q + c6) / \
              ((((d1 * q + d2) * q + d3) * q + d4) * q + 1)
    return z

def dprime(hits, misses, falseAlarms, correctRejections, adjustment=False):
    """Calculates and returns d'
    >>> dprime(20,5,10,15)
    1.09496834
    >>> dprime(10,0,2,8)
    2.48647486
    >>> dprime(9,1,0,10)
    2.92640519
    >>> dprime(25,0,10,15,True)
    2.31330601
    """
    if hits == 0 and misses == 0 and correctRejections == 0 and falseAlarms == 0:
        adjustment = True
    H = Hrate(hits, misses, adjustment)
    F = Frate(falseAlarms, correctRejections, adjustment)
    zH = normsinv(H)
    zF = normsinv(F)
    if zH == None or zF == None:
        return -1
    dprime = zH - zF
    return round(dprime,8)
    
if __name__ == "__main__":
    import doctest
    doctest.testmod()