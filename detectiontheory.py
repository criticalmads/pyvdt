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

from scipy.stats import norm

# The adjustment avoids infinite d' values by adding 0.5 to all data cells
# (hits, misses, false alarms, correct rejections) regardless of whether
# zeroes are present.
# See Macmillan & Creelman "Detection Theory: A User's Guide", 2nd edition,
# pp. 8-9.
#
# d' = 4.65 is considered an effective ceiling (Macmillan & Creelman, 2008, p. 8)

def Hrate(hits, misses, adjustment=False):
    """Calculates and returns H (hit rate)"""
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
    """Calculates and returns F (false-alarm rate)"""
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

def dprime(hits, misses, falseAlarms, correctRejections, adjustment=False):
    """Calculates and returns d'"""
    H = Hrate(hits, misses, adjustment)
    F = Frate(falseAlarms, correctRejections, adjustment)
    zH = norm.ppf(H)
    zF = norm.ppf(F)
    dprime = zH - zF
    return dprime

