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

#TODO: save name, date, vmtRate, vmtDuration inside the output file or append the variables to the filename (remove illegal chars)

import csv
import detectiontheory as dt
import os


#TODO: check if file exists
def vmtRawScoreOutput(vmtOutput,outputFilename):
    outputCsv = csv.writer(open(outputFilename,'ab'),dialect='excel')
    outputCsv.writerow(['TrialNumber',
                        'Hit',
                        'Miss',
                        'FalseAlarm',
                        'CorrectRejection',
                        'ShownDigit',
                        'Signal',
                        'Decision',
                        'TrialDuration',
                        'DigitStart',
                        'DigitEnd',
                        'DigitDuration',
                        'DecisionTimestamp',
                        'BlinkStart',
                        'BlinkEnd',
                        'BlinkDuration',
                        'RT'])
    
    for i, obj in enumerate(vmtOutput):
        if vmtOutput[i,16] == -1:
            RT=""
        else:
            RT=vmtOutput[i,16]
        outputCsvCurrentRow =   [int(vmtOutput[i,0]),
                                 int(vmtOutput[i,1]),
                                 int(vmtOutput[i,2]),
                                 int(vmtOutput[i,3]),
                                 int(vmtOutput[i,4]),
                                 int(vmtOutput[i,5]),
                                 int(vmtOutput[i,6]),
                                 int(vmtOutput[i,7]),
                                 vmtOutput[i,8],
                                 vmtOutput[i,9],
                                 vmtOutput[i,10],
                                 vmtOutput[i,11],
                                 vmtOutput[i,12],
                                 vmtOutput[i,13],
                                 vmtOutput[i,14],
                                 vmtOutput[i,15],
                                 RT]
        #outputCsv.writerow(vmtOutput[i,])
        outputCsv.writerow(outputCsvCurrentRow)
    #close(outputFilename) #yields "NameError: name 'close' is not defined" TODO: fix

def vmtScoreAppend(subjNumber,subjName,vmtDate,hits,misses,falseAlarms,correctRejections,subjComment,outputFilenameAppend):
    fileExists = os.path.exists(outputFilenameAppend)
    outputCsv = csv.writer(open(outputFilenameAppend,'ab'),dialect='excel')

    H=dt.Hrate(hits,misses)
    F=dt.Frate(hits,misses)
    dprime=dt.dprime(hits,misses,falseAlarms,correctRejections)

    Hadj=dt.Hrate(hits,misses,adjustment=True)
    Fadj=dt.Frate(hits,misses,adjustment=True)
    dprimeAdj=dt.dprime(hits,misses,falseAlarms,correctRejections,adjustment=True)
    
    if fileExists == False: # then write header; otherwise just append the data
        outputCsv.writerow(['ID',
                            'Name',
                            'Date',
                            'Hits',
                            'Misses',
                            'False alarms',
                            'Correct rejections',
                            'H',
                            'F',
                            'd\'',
                            'H adjusted',
                            'F adjusted',
                            'd\' adjusted',
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

