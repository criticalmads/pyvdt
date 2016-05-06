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

# Import psychopy.visual first,
# so that avbin.dll is loaded correctly (Windows).
from psychopy import visual
import math
import random
from psychopy import core, event
import psychopy.logging
import csv

def vmtTargets(vmtDigits):
    """Identifies even-odd-even sequences (targets) in a list of digits
    """
    #  List of targets (1) and non-targets (0);
    # no target sequence is possible before three digits have been shown,
    # so two 0's are added at the beginning.
    oddEvenOdd = [0,0]
    for id,thisDigit in enumerate(vmtDigits):
        # Start at third digit (ie. first possible three-digit sequence)        
        if id>1:
            firstDigit = int(vmtDigits[id-2])
            secondDigit = int(vmtDigits[id-1])
            thisDigit = int(thisDigit)

            if firstDigit%2==0 and secondDigit%2!=0 and thisDigit%2==0:
                oddEvenOdd.append(1)
            else:
                oddEvenOdd.append(0)
    return oddEvenOdd

def calculateDigitPresentationRate(vmtRate,monitorRefreshRate):
    vmtRateMs = vmtRate*1000
    msPerFrame = round(float(1000)/monitorRefreshRate,1) #using float() on the numerator forces Python to return a float instead of an integer
    digitFrames = int(math.floor(float(vmtRateMs)/msPerFrame))
    return(digitFrames)

def vmt(myWin,vmtRate,vmtDuration,monitorRefreshRate,listOfDigits,fontFace,fontHeight,vmtFrameLogfile):
    digitStim0 = visual.TextStim(myWin,text="0",color='black',
                                font=fontFace,height=fontHeight)
                  
    digitStim1 = visual.TextStim(myWin,text="1",color='black',
                                font=fontFace,height=fontHeight)
                  
    digitStim2 = visual.TextStim(myWin,text="2",color='black',
                                font=fontFace,height=fontHeight)
                  
    digitStim3 = visual.TextStim(myWin,text="3",color='black',
                                font=fontFace,height=fontHeight)
                  
    digitStim4 = visual.TextStim(myWin,text="4",color='black',
                                font=fontFace,height=fontHeight)
                  
    digitStim5 = visual.TextStim(myWin,text="5",color='black',
                                font=fontFace,height=fontHeight)
                  
    digitStim6 = visual.TextStim(myWin,text="6",color='black',
                                font=fontFace,height=fontHeight)
                  
    digitStim7 = visual.TextStim(myWin,text="7",color='black',
                                font=fontFace,height=fontHeight)
                  
    digitStim8 = visual.TextStim(myWin,text="8",color='black',
                                font=fontFace,height=fontHeight)
                  
    digitStim9 = visual.TextStim(myWin,text="9",color='black',
                                font=fontFace,height=fontHeight)
                                
    digitStims = {0: digitStim0,
                  1: digitStim1,
                  2: digitStim2,
                  3: digitStim3,
                  4: digitStim4,
                  5: digitStim5,
                  6: digitStim6,
                  7: digitStim7,
                  8: digitStim8,
                  9: digitStim9}

    signal = vmtTargets(listOfDigits)
    
    vmtOutput = [[0 for x in range(17)] for x in range(vmtDuration/vmtRate)] 
    vmtOutputSum = {'hits': 0,
                    'misses': 0,
                    'falseAlarms': 0,
                    'correctRejections': 0}

    try: trialClock
    except NameError:
        trialClock=core.Clock()
    else:
        trialClock.reset()
    event.clearEvents(eventType='keyboard')
    
    # Make log timestamps start at the beginning of the test
    # instead of at the beginning of the program.
    psychopy.logging.setDefaultClock(trialClock)
    myWin.setRecordFrameIntervals()
    
    digitFrames = calculateDigitPresentationRate(vmtRate,monitorRefreshRate)
    
    digitCounter = 0
    currentDigit = 0
    
    while digitCounter<(vmtDuration/vmtRate):
        currentDigit = listOfDigits[digitCounter]
        currentDigitStim = digitStims.get(int(currentDigit))
    
        for frameN in range(digitFrames):
            if frameN==0:
                currentDigitStim.draw()
                myWin.flip(clearBuffer=False)
                currentDigitStartTimestamp=trialClock.getTime()
            else:
                currentDigitStim.draw()
                myWin.flip()
        

        currentDigitEndTimestamp=trialClock.getTime()
        currentBlinkStartTimestamp=trialClock.getTime()
        
        # Get list of timestamped space keypresses        
        trialKeys = event.getKeys(["space"],timeStamped=trialClock)
        if len(trialKeys)>0:
            # Get first tuple ('space', <timestamp>) in list of
            # tuples of space keypresses and timestamps;
            # shorten this to just the timestamp.
            currentDigitSpaceTimestamp = (trialKeys[0])[1]
            currentDigitDecision=1
        else:
            currentDigitSpaceTimestamp = 0
            currentDigitDecision=0
        
        # To abort testing, press q
        quitKeys = event.getKeys(["q"])
        if len(quitKeys)>0: core.quit()
    
        myWin.clearBuffer()
        # Shows one blank frame between digits;
        # lets participants notice when there are two
        # identical digits in a row        
        myWin.flip()
        currentBlinkEndTimestamp=trialClock.getTime()
        
        
        if signal[digitCounter] == 1 and currentDigitDecision == 1:
            hit=1
            miss=0
            falseAlarm=0
            correctRejection=0
        if signal[digitCounter] == 1 and currentDigitDecision == 0:
            hit=0
            miss=1
            falseAlarm=0
            correctRejection=0
        if signal[digitCounter] == 0 and currentDigitDecision == 1:
            hit=0
            miss=0
            falseAlarm=1
            correctRejection=0
        if signal[digitCounter] == 0 and currentDigitDecision == 0:
            hit=0
            miss=0
            falseAlarm=0
            correctRejection=1
    
        vmtOutputSum['hits'] += hit
        vmtOutputSum['misses'] += miss
        vmtOutputSum['falseAlarms'] += falseAlarm
        vmtOutputSum['correctRejections'] += correctRejection
    
        
        # TrialNumber Hit Miss FalseAlarm
        # CorrectRejection ShownDigit Signal Decision
        # TrialDuration DigitStart DigitEnd DigitDuration
        # DecisionTimestamp BlinkStart BlinkEnd BlinkDuration RT
        vmtOutput[digitCounter][0] = digitCounter+1
        vmtOutput[digitCounter][1] = hit
        vmtOutput[digitCounter][2] = miss
        vmtOutput[digitCounter][3] = falseAlarm
        vmtOutput[digitCounter][4] = correctRejection
        vmtOutput[digitCounter][5] = currentDigit
        vmtOutput[digitCounter][6] = signal[digitCounter]
        vmtOutput[digitCounter][7] = currentDigitDecision
        vmtOutput[digitCounter][8] = (currentBlinkEndTimestamp-currentDigitStartTimestamp)
        vmtOutput[digitCounter][9] = currentDigitStartTimestamp
        vmtOutput[digitCounter][10] = currentDigitEndTimestamp
        vmtOutput[digitCounter][11] = (currentDigitEndTimestamp-currentDigitStartTimestamp)
        vmtOutput[digitCounter][12] = currentDigitSpaceTimestamp
        vmtOutput[digitCounter][13] = currentBlinkStartTimestamp
        vmtOutput[digitCounter][14] = currentBlinkEndTimestamp
        vmtOutput[digitCounter][15] = (currentBlinkEndTimestamp-currentBlinkStartTimestamp)
        if currentDigitDecision==1: vmtOutput[digitCounter][16] = (currentDigitSpaceTimestamp-currentDigitStartTimestamp)
        else: vmtOutput[digitCounter][16] = -1 # space wasn't pressed; -1 is removed from the output file
        digitCounter += 1
    
    myWin.saveFrameIntervals(vmtFrameLogfile)
    
    myWin.flip(clearBuffer=True)
    myWin.setRecordFrameIntervals(False)
    
    return vmtOutput, vmtOutputSum

# ----self-test start---

def selftest(listOfDigits,vmtDuration,vmtRate):
    
    signal = vmtTargets(listOfDigits)
    
    vmtOutput = [[0 for x in range(17)] for x in range(vmtDuration/vmtRate)] 
    vmtOutputSum = {'hits': 0,
                    'misses': 0,
                    'falseAlarms': 0,
                    'correctRejections': 0}

    
    digitCounter = 0
    currentDigit = 0
    
    while digitCounter<(vmtDuration/vmtRate):
    
        currentDigit = listOfDigits[digitCounter]
    
        currentDigitDecision = random.randint(0,1)
        
        
        if signal[digitCounter] == 1 and currentDigitDecision == 1:
            hit=1
            miss=0
            falseAlarm=0
            correctRejection=0
        if signal[digitCounter] == 1 and currentDigitDecision == 0:
            hit=0
            miss=1
            falseAlarm=0
            correctRejection=0
        if signal[digitCounter] == 0 and currentDigitDecision == 1:
            hit=0
            miss=0
            falseAlarm=1
            correctRejection=0
        if signal[digitCounter] == 0 and currentDigitDecision == 0:
            hit=0
            miss=0
            falseAlarm=0
            correctRejection=1
    
        vmtOutputSum['hits'] += hit
        vmtOutputSum['misses'] += miss
        vmtOutputSum['falseAlarms'] += falseAlarm
        vmtOutputSum['correctRejections'] += correctRejection
    
        
        # TrialNumber Hit Miss FalseAlarm
        # CorrectRejection ShownDigit Signal Decision
        # TrialDuration DigitStart DigitEnd DigitDuration
        # DecisionTimestamp BlinkStart BlinkEnd BlinkDuration RT
        vmtOutput[digitCounter][0] = digitCounter+1
        vmtOutput[digitCounter][1] = hit
        vmtOutput[digitCounter][2] = miss
        vmtOutput[digitCounter][3] = falseAlarm
        vmtOutput[digitCounter][4] = correctRejection
        vmtOutput[digitCounter][5] = currentDigit
        vmtOutput[digitCounter][6] = signal[digitCounter]
        vmtOutput[digitCounter][7] = currentDigitDecision
        vmtOutput[digitCounter][8] = 0
        vmtOutput[digitCounter][9] = 0
        vmtOutput[digitCounter][10] = 0
        vmtOutput[digitCounter][11] = 0
        vmtOutput[digitCounter][12] = 0
        vmtOutput[digitCounter][13] = 0
        vmtOutput[digitCounter][14] = 0
        vmtOutput[digitCounter][15] = 0
        vmtOutput[digitCounter][16] = 0
        digitCounter += 1
    
    return vmtOutput, vmtOutputSum


# ----self-test end-----


def showText(myWin,textToShow,fontFace):
    try: textClock
    except NameError:
        textClock=core.Clock()
    else:
        textClock.reset()
    textStim = visual.TextStim(myWin,
                               text = textToShow,
                               color='black',
                               font=fontFace,
                               height=1)
    continueInstruct=True
    while continueInstruct:
        # Get current time
        t=textClock.getTime()
        
        # Update/draw components on each frame
        if (0 <= t):
            textStim.draw()
        if (0 <= t):
            keypresses = event.getKeys()
            if len(keypresses)>0:
                # At least one key was pressed.
                # Abort routine on response
                continueInstruct=False
                # Check for quit (the [Esc] key).
                if keypresses[0] == "escape": core.quit()
        # Refresh the screen
        myWin.flip()

def VMTdigitSequences(filename):
    """Returns a nested list containing VMT digit sequences"""
    csvReader = csv.reader(open(filename, 'rb'), delimiter=',', quotechar='"')
    nestedListOfTargets = []
    for row in csvReader:
        nestedListOfTargets.append(row)
    return nestedListOfTargets
