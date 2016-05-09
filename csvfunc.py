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

import csv
import detectiontheory as dt
import os

def vmtRawScoreOutput(vmtOutput,outputFilename):
    """Write raw, unprocessed data to .csv files.
    
    These raw data relate to the presentation of stimuli and
    the calculation of sensitivity measures to .csv files.
    These data are provided primarily for diagnostic purposes.
    By default, the output .csv files are given filenames ending in
    "<timestamp>-{1,2}.csv".
    """
    outputCsv = csv.writer(open(outputFilename,'ab'),dialect='excel')
    outputCsv.writerow(['TrialNumber',  # Stimulus serial number
    
                        'Hit',              # Target detected?
                        'Miss',             # Target missed?
                        'FalseAlarm',       # ...and so on.
                        'CorrectRejection',
                        
                        'ShownDigit',       # The digit shown on screen
                        
                        'Signal',           # Signal present?
                        'Decision',         # Participant's decision
                        
                        'TrialDuration',   # Digit shown for x millisecs
                        
                        'DigitStart',  # Time at start of presentation
                        'DigitEnd',    # Time at end
                        'DigitDuration',  # Digit presentation duration
                        
                        'DecisionTimestamp',  # Time at keypress
                        
                        'BlinkStart',         #
                        'BlinkEnd',           #
                        'BlinkDuration',      #
                        
                        'RT'])  # Reaction time
    
    for i, obj in enumerate(vmtOutput):
        if vmtOutput[i][16] == -1:
            RT = ""
        else:
            RT = vmtOutput[i][16]
        outputCsvCurrentRow =   [int(vmtOutput[i][0]),
                                 int(vmtOutput[i][1]),
                                 int(vmtOutput[i][2]),
                                 int(vmtOutput[i][3]),
                                 int(vmtOutput[i][4]),
                                 int(vmtOutput[i][5]),
                                 int(vmtOutput[i][6]),
                                 int(vmtOutput[i][7]),
                                 vmtOutput[i][8],
                                 vmtOutput[i][9],
                                 vmtOutput[i][10],
                                 vmtOutput[i][11],
                                 vmtOutput[i][12],
                                 vmtOutput[i][13],
                                 vmtOutput[i][14],
                                 vmtOutput[i][15],
                                 RT]
        outputCsv.writerow(outputCsvCurrentRow)

def vmtScoreAppend(subjNumber,
                   subjName,
                   vmtDate,
                   hits,
                   misses,
                   falseAlarms,
                   correctRejections,
                   subjComment,
                   outputFilenameAppend):
    """Write main output variables of interest to .csv files.
    
    These variables include sensitivity measures (e.g., d'),
    participant names and IDs, experiment dates, and comments.
    By default, these output .csv files are given filenames ending in
    "data-{1,2}.csv".
    """
    fileExists = os.path.exists(outputFilenameAppend)
    outputCsv = csv.writer(open(outputFilenameAppend,'ab'),
                           dialect='excel')

    H = dt.Hrate(hits, misses)
    F = dt.Frate(hits, misses)
    dprime = dt.dprime(hits, misses, falseAlarms, correctRejections)

    Hadj = dt.Hrate(hits, misses, adjustment = True)
    Fadj = dt.Frate(hits, misses, adjustment = True)
    dprimeAdj = dt.dprime(hits,
                        misses,
                        falseAlarms,
                        correctRejections,
                        adjustment=True)
    
    if fileExists == False:
        # ...then write header; otherwise, simply append the data.
        # In the following, "M & C" refers to Macmillan & Creelman.
        outputCsv.writerow(['ID',                   # Subject number
                            'Name',
                            'Date',
                            
                            'Hits',                 # Sum of hits
                            'Misses',               # Sum of misses
                            'False alarms',         # ...and so on.
                            'Correct rejections',
                            
                            'H',      # Hit rate (M & C, 2004, p. 5)
                            'F',      # False-alarm rate (M & C, p. 5)
                            'd\'',    # d prime (M & C, p. 8)
                            
                            'H adjusted',    # Adjusted hit rate
                            'F adjusted',    # Adjusted false-alarm rate
                            'd\' adjusted',  # Adjusted d'
                            
                            'Comment'])
    
    outputCsv.writerow([subjNumber,
                        subjName,
                        vmtDate,
                        hits,
                        misses,
                        falseAlarms,
                        correctRejections,
                        H,
                        F,
                        dprime,
                        Hadj,
                        Fadj,
                        dprimeAdj,
                        subjComment])

