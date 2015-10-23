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


import math # floor() is used for rounding down
from psychopy import core, data, event, visual, gui
import psychopy.log
from numpy import *
import csv

def vmtDigits(presentationRate,duration):
    #calculate number of digits to present
    numDigits=duration/presentationRate
    #generate random digits
    randomDigits = randint(1,9,size=numDigits)
    return randomDigits

def vmtTargets(vmtDigits): #Identifies even-odd-even sequences (targets) in a list of digits
    oddEvenOdd = [0,0] #list of targets (1) and non-targets (0); no target sequence is possible before three digits have been shown, so two 0's are added at the beginning
    for id,thisDigit in enumerate(vmtDigits):
        if id>1:#start at third digit (ie. first possible three-digit sequence)
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
    # stimuli
    digitStim = visual.TextStim(myWin,text="",color='black',
                                font=fontFace,height=fontHeight)
                  
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
    
    vmtOutput = zeros(((vmtDuration/vmtRate),17))#set up numpy array in which to store data
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
    #TODO: clear screen buffer as well?
    
    psychopy.log.setDefaultClock(trialClock) # make log timestamps start at the beginning of the test instead of at the beginning of the program
    myWin.setRecordFrameIntervals()
    
    digitFrames = calculateDigitPresentationRate(vmtRate,monitorRefreshRate)
    
    digitCounter = 0
    currentDigit = 0
    
    while digitCounter<(vmtDuration/vmtRate):
        #myWin.logOnFlip("Digit "+str(digitCounter+1)+" START", psychopy.log.WARNING)
    
        currentDigit = listOfDigits[digitCounter]
        currentDigitStim = digitStims.get(int(currentDigit))
    
        for frameN in range(digitFrames):#for exactly digitFrames frames
            if frameN==0:
                currentDigitStim.draw()
                myWin.flip(clearBuffer=False)
                currentDigitStartTimestamp=trialClock.getTime()
            else:
                #myWin.flip(clearBuffer=False)
                currentDigitStim.draw()
                myWin.flip()
        

        currentDigitEndTimestamp=trialClock.getTime()
        currentBlinkStartTimestamp=trialClock.getTime()#TODO: should take place after flip
        
        trialKeys = event.getKeys(["space"],timeStamped=trialClock)#get list of timestamped space keypresses
        if len(trialKeys)>0:
            currentDigitSpaceTimestamp = (trialKeys[0])[1]#get first tuple ('space', <timestamp>) in list of tuples of space keypresses and timestamps; shorten this to just the timestamp
            currentDigitDecision=1
        else:
            currentDigitSpaceTimestamp = 0
            currentDigitDecision=0
        
        quitKeys = event.getKeys(["q"])
        if len(quitKeys)>0: core.quit()
    
        myWin.clearBuffer()
        myWin.flip()#shows one blank frame between digits; lets participants notice when there are two identical digits in a row
        currentBlinkEndTimestamp=trialClock.getTime() #TODO: should take place just before the following flip
        
        
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
    
        
        #TrialNumber Hit Miss FalseAlarm CorrectRejection ShownDigit Signal Decision TrialDuration DigitStart DigitEnd DigitDuration DecisionTimestamp BlinkStart BlinkEnd BlinkDuration RT
        vmtOutput[digitCounter,0] = digitCounter+1
        vmtOutput[digitCounter,1] = hit
        vmtOutput[digitCounter,2] = miss
        vmtOutput[digitCounter,3] = falseAlarm
        vmtOutput[digitCounter,4] = correctRejection
        vmtOutput[digitCounter,5] = currentDigit
        vmtOutput[digitCounter,6] = signal[digitCounter]
        vmtOutput[digitCounter,7] = currentDigitDecision
        vmtOutput[digitCounter,8] = (currentBlinkEndTimestamp-currentDigitStartTimestamp)
        vmtOutput[digitCounter,9] = currentDigitStartTimestamp
        vmtOutput[digitCounter,10] = currentDigitEndTimestamp
        vmtOutput[digitCounter,11] = (currentDigitEndTimestamp-currentDigitStartTimestamp)
        vmtOutput[digitCounter,12] = currentDigitSpaceTimestamp
        vmtOutput[digitCounter,13] = currentBlinkStartTimestamp
        vmtOutput[digitCounter,14] = currentBlinkEndTimestamp
        vmtOutput[digitCounter,15] = (currentBlinkEndTimestamp-currentBlinkStartTimestamp)
        if currentDigitDecision==1: vmtOutput[digitCounter,16] = (currentDigitSpaceTimestamp-currentDigitStartTimestamp)
        else: vmtOutput[digitCounter,16] = -1 # space wasn't pressed; -1 is removed from the output file
        digitCounter += 1
    
    myWin.saveFrameIntervals(vmtFrameLogfile)
    
    myWin.flip(clearBuffer=True)
    myWin.setRecordFrameIntervals(False)
    
    return vmtOutput, vmtOutputSum

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
        #get current time
        t=textClock.getTime()
        
        #update/draw components on each frame
        if (0 <= t):
            textStim.draw()
        if (0 <= t):
            keypresses = event.getKeys()
            if len(keypresses)>0:#at least one key was pressed
                #abort routine on response
                continueInstruct=False
                #check for quit (the [Esc] key)
                #introEsc = introKeypresses(["escape"]) #TODO: fix this (causes TypeError: 'list' object is not callable)
                #if len(introEsc)>0: core.quit()
        #refresh the screen
        myWin.flip()

def VMTdigitSequences(filename):
    """Returns a nested list containing VMT digit sequences"""
    csvReader = csv.reader(open(filename, 'rb'), delimiter=',', quotechar='"')
    nestedListOfTargets = []
    for row in csvReader:
        nestedListOfTargets.append(row)
    return nestedListOfTargets

#def getVMTtarget(vmtRate)
