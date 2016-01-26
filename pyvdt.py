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


#TODO: log win.frameintervals


#from psychopy import core, data, event, visual, gui
from psychopy import visual # import psychopy.visual before any other libraries, so that avbin.dll is loaded correctly (Windows)
from psychopy import core, data, gui
import psychopy.log
import functions as vmt
from ConfigParser import ConfigParser
import csvfunc as vmtcsv

#----------------CONFIG START----------------
config = ConfigParser()
config.read('pyvdt.ini')

language = config.get('misc','language')

resolutionX = int(config.get('monitor','resolutionX'))
resolutionY = int(config.get('monitor','resolutionY'))
optFullscreen = int(config.get('monitor','fullscreen'))

monitorRefreshRate = int(config.get('monitor','refreshRateHz')) #Monitor refresh rate in Hz; used to calculate how many frames to present stimuli for

vmtRate1 = int(config.get('vmt','rate1')) #Digit presentation rate in seconds; actual rate depends on monitor refresh rate
vmtRate2 = int(config.get('vmt','rate2'))
vmtDuration = int(config.get('vmt','duration')) #2 minutes and 32 seconds (Knutson et al., 1991); used to calculate how many digits to present

outputFilePrefix = config.get('misc','outputPrefix')
#outputFileUUID = uuid.uuid4()

#listOfDigits = config.get('vmtTargets','1')

#logDir=""
fontHeight = 16
fontFace = ['Liberation Serif','Times New Roman','Verdana','Arial'] #use the first font found
intervalBetweenTrials=2
#----------------- CONFIG END-----------------

# ------------------ additional config start -------------------

optionsDialog = gui.Dlg(title="Visual Monitoring Task",size=(400,400))
optionsDialog.addText('Subject info')
optionsDialog.addField('Name:')
optionsDialog.addField('Subject number:')#use number of lines in output file as default value

optionsDialog.addText('Experiment Info')
optionsDialog.addField('VMT rate (1st test):',vmtRate1,tip='The number of seconds for which to display digits during the first test')
optionsDialog.addField('Digit sequence (1st test):',1,tip='The line number from pyvdtSequences-rate1.csv to use as the digit sequence for the first test')
optionsDialog.addField('VMT rate (2nd test):',vmtRate2,tip='The number of seconds for which to display digits during the second test')
optionsDialog.addField('Digit sequence (2nd test):',1,tip='The line number from pyvdtSequences-rate2.csv to use as the digit sequence for the second test')

optionsDialog.addField('Monitor refresh rate in Hz',monitorRefreshRate)
optionsDialog.addField('Comment:')
optionsDialog.addField('Output file prefix:',outputFilePrefix,tip='Prefix to add to output files')
optionsDialog.addField('Language:', language,tip='Valid entries are en (English) and da (Danish)')

optionsDialog.addText('')
optionsDialog.addText('PyVDT')
optionsDialog.addText('Copyright (c) 2011, 2015, Aarhus University.')
optionsDialog.addText('This program comes with ABSOLUTELY NO WARRANTY.')
optionsDialog.addText('This program is free software, and you are welcome')
optionsDialog.addText('to redistribute it under certain conditions.')
optionsDialog.addText('See LICENSE for further details.')



optionsDialog.show()
if optionsDialog.OK:
    subjName = optionsDialog.data[0] #TODO: generate uuid if unset
    subjNumber = optionsDialog.data[1] #TODO: generate uuid if unset
    
    vmtRate1 = optionsDialog.data[2]
    vmt1LineNumber = optionsDialog.data[3]-1
    vmtRate2 = optionsDialog.data[4]
    vmt2LineNumber = optionsDialog.data[5]-1
    
    monitorRefreshRate = optionsDialog.data[6]
    subjComment = optionsDialog.data[7]
    outputFilePrefix = optionsDialog.data[8] #TODO: generate uuid if unset
    language = optionsDialog.data[9]
else:
    core.quit()

#TODO: fix unicode strings; replacing unicode chars is not optimal
#subjName=unicode(subjName,errors='replace')
#subjNumber=unicode(subjNumber,errors='replace')
#subjComment=unicode(subjComment,errors='replace')

vmtLogfile = open(outputFilePrefix+subjNumber+subjName+".log",'a')
vmtFrameLogfile = outputFilePrefix+subjNumber+subjName+"-frames.log"
psychopy.log.LogFile(f=vmtLogfile,level=0)
psychopy.log.info("Subject name: "+subjName)
psychopy.log.info("Subject number: "+subjNumber)
psychopy.log.info("Comment: "+subjComment)

VMTdigitSeqs1 = vmt.VMTdigitSequences("pyvdtSequences-rate1.csv")
listOfDigits1 = VMTdigitSeqs1[vmt1LineNumber]

VMTdigitSeqs2 = vmt.VMTdigitSequences("pyvdtSequences-rate2.csv")
listOfDigits2 = VMTdigitSeqs2[vmt2LineNumber]

#TODO: fix unicode strings
introductionText = unicode(config.get(language,'introText'),errors='replace')
pauseText = unicode(config.get(language,'pauseText'),errors='replace')
endText = unicode(config.get(language,'endText'),errors='replace')

vmtDate = data.getDateStr()

outputFilename1 = outputFilePrefix+vmtDate+"-1.csv"
outputFilenameAppend1 = outputFilePrefix+"data-1.csv"
outputFilename2 = outputFilePrefix+vmtDate+"-2.csv"
outputFilenameAppend2 = outputFilePrefix+"data-2.csv"


#listOfDigits = vmt(vmtRate,vmtDuration) #TODO: don't use hardcoded list of targets
#listOfDigits = [7, 1, 5, 1, 0, 5, 6, 1, 8, 0, 7, 1, 2, 5, 1, 4, 5, 1, 5, 0, 7, 6, 4, 3, 4, 0, 4, 8, 3, 2, 8, 1, 5, 3, 2, 6, 0, 6, 3, 2, 0, 8, 7, 6, 2, 6, 3, 7, 0, 1, 7, 1, 4, 8, 1, 6, 2, 4, 5, 0, 6, 4, 0, 7, 0, 6, 3, 5, 3, 2, 4, 2, 1, 4, 7, 6, 7, 3, 7, 5, 0, 6, 1, 2, 3, 8, 4, 1, 4, 0, 7, 3, 8, 4, 5, 8, 7, 6, 2, 0, 6, 2, 7, 5, 1, 6, 4, 0, 8, 2, 7, 4, 5, 1, 0, 5, 6, 2, 1, 7, 1, 2, 1, 5, 8, 2, 6, 4, 7, 3, 5, 7, 8, 3, 8, 3, 4, 3, 6, 5, 3, 2, 6, 0, 6, 0, 2, 1, 6, 1, 7, 6]


myWin = visual.Window((resolutionX,resolutionY),
                      allowGUI=False,
                      fullscr=optFullscreen,
                      color='white',
                      monitor='testMonitor',
                      units ='deg',
                      screen=0)


#----------------STIMULI START --------------------------------------------

fixationStim = visual.PatchStim(win=myWin,
                                size=0.2,
                                pos=[0,0],
                                sf=0,
                                color=(-1,-1,-1))#black
#----------------STIMULI END --------------------------------------------





#Show introduction -----------------------------------------------------------
vmt.showText(myWin,introductionText,fontFace)


fixationStim.draw()
myWin.flip()
core.wait(intervalBetweenTrials)
myWin.flip(clearBuffer=True)

#-------------VMT1 start--------------------------------------------------------
vmtRate = vmtRate1

if vmtRate == 1:
    listOfDigits = listOfDigits1

if vmtRate == 2:
    listOfDigits = listOfDigits2

vmt1output, vmt1OutputSum = vmt.vmt(myWin,vmtRate,vmtDuration,monitorRefreshRate,listOfDigits,fontFace,fontHeight,vmtFrameLogfile)

vmtcsv.vmtRawScoreOutput(vmt1output,outputFilename1)
vmtcsv.vmtScoreAppend(subjNumber,
                      subjName,
                      vmtDate,
                      vmt1OutputSum['hits'],
                      vmt1OutputSum['misses'],
                      vmt1OutputSum['falseAlarms'],
                      vmt1OutputSum['correctRejections'],
                      subjComment,
                      outputFilenameAppend1)

#----------------VMT1 end -------------------------------------------
# pause
core.wait(intervalBetweenTrials)
vmt.showText(myWin,pauseText,fontFace)
#core.wait(intervalBetweenTrials)
#myWin.flip(clearBuffer=True)

fixationStim.draw()
myWin.flip()
core.wait(intervalBetweenTrials)
myWin.flip(clearBuffer=True)

#-------------VMT2 start--------------------------------------------------------
vmtRate = vmtRate2

if vmtRate == 1:
    listOfDigits = listOfDigits1

if vmtRate == 2:
    listOfDigits = listOfDigits2

vmt2output, vmt2OutputSum = vmt.vmt(myWin,vmtRate,vmtDuration,monitorRefreshRate,listOfDigits,fontFace,fontHeight,vmtFrameLogfile)

vmtcsv.vmtRawScoreOutput(vmt2output,outputFilename2)
vmtcsv.vmtScoreAppend(subjNumber,
                      subjName,
                      vmtDate,
                      vmt2OutputSum['hits'],
                      vmt2OutputSum['misses'],
                      vmt2OutputSum['falseAlarms'],
                      vmt2OutputSum['correctRejections'],
                      subjComment,
                      outputFilenameAppend2)
#----------------VMT2 end -------------------------------------------


# -------------------- show end text ----------------------------------------
core.wait(intervalBetweenTrials)
#Show endText
vmt.showText(myWin,endText,fontFace)
core.quit()