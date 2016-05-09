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
from psychopy import core, data, gui
from psychopy.tools.plottools import plotFrameIntervals
import psychopy.logging
import functions as vmt
from ConfigParser import ConfigParser
import csvfunc as vmtcsv

# ----------------CONFIG START----------------
config = ConfigParser()
config.read('pyvdt.ini')

language = config.get('misc', 'language')

resolutionX = int(config.get('monitor', 'resolutionX'))
resolutionY = int(config.get('monitor', 'resolutionY'))
optFullscreen = int(config.get('monitor', 'fullscreen'))

# Monitor refresh rate in Hz.
# This is used to calculate how many frames to present stimuli for.
monitorRefreshRate = int(config.get('monitor', 'refreshRateHz'))

# Digit presentation rate in seconds.
# Actual rate depends on monitor refresh rate.
vmtRate1 = int(config.get('detectiontask', 'rate1'))
vmtRate2 = int(config.get('detectiontask', 'rate2'))
# vmtDuration is used to calculate how many digits to present.
# Default duration is 2 minutes and 32 seconds
# (see Knutson et al., 1991).
vmtDuration = int(config.get('detectiontask', 'duration'))

outputFilePrefix = config.get('misc', 'outputPrefix')

fontHeight = 16
# Use the first font found
fontFace = ['Liberation Serif', 'Times New Roman', 'Verdana', 'Arial']
intervalBetweenTrials = 2
# ----------------- CONFIG END-----------------

# ------------------ additional config start -------------------
optionsDialog = gui.Dlg(title="PyVDT",
                        size=(400, 400))
optionsDialog.addText('Subject info')
optionsDialog.addField('Name:')
optionsDialog.addField('Subject number:')

optionsDialog.addText('Experiment Info')

optionsDialog.addField('Presentation rate (1st test):',
                       vmtRate1,
                       tip='The number of seconds for which to \
                       display digits during the first test')

optionsDialog.addField('Digit sequence (1st test):',
                       1,
                       tip='The line number from \
                       pyvdtSequences-rate1.csv to use as the \
                       digit sequence for the first test')

optionsDialog.addField('Presentation rate (2nd test):',
                       vmtRate2,
                       tip='The number of seconds for which to \
                       display digits during the second test')

optionsDialog.addField('Digit sequence (2nd test):',
                       1,
                       tip='The line number from \
                       pyvdtSequences-rate2.csv to use as the \
                       digit sequence for the second test')

optionsDialog.addField('Monitor refresh rate in Hz',
                       monitorRefreshRate)
optionsDialog.addField('Comment:')
optionsDialog.addField('Output file prefix:',
                       outputFilePrefix,
                       tip='Prefix to add to output files')
optionsDialog.addField('Language:',
                       language,
                       tip='Valid entries are en (English) and \
                       da (Danish)')

optionsDialog.addField('Self-test mode', "n",
                       tip='Set to "y" to generate output data; \
                       "p" to plot frame log file')
optionsDialog.addField('No. of iterations', "5",
                       tip='The number of random subjects to \
                       generate')
optionsDialog.addField('Frame log file to plot', "pyvdt-test-frames.log")

optionsDialog.addText('')
optionsDialog.addText('PyVDT')
optionsDialog.addText('Copyright (c) 2011, 2015, Aarhus University.')
optionsDialog.addText('This program comes with ABSOLUTELY NO WARRANTY.')
optionsDialog.addText('This program is free software, and you are welcome')
optionsDialog.addText('to redistribute it under certain conditions.')
optionsDialog.addText('See LICENSE for further details.')

optionsDialog.show()
if optionsDialog.OK:
    subjName = optionsDialog.data[0]
    subjNumber = optionsDialog.data[1]

    vmtRate1 = optionsDialog.data[2]
    vmt1LineNumber = optionsDialog.data[3] - 1
    vmtRate2 = optionsDialog.data[4]
    vmt2LineNumber = optionsDialog.data[5] - 1

    monitorRefreshRate = optionsDialog.data[6]
    subjComment = optionsDialog.data[7]
    outputFilePrefix = optionsDialog.data[8]
    language = optionsDialog.data[9]

    testMode = optionsDialog.data[10]
    testIterations = optionsDialog.data[11]
    frameLogFile = optionsDialog.data[12]
else:
    core.quit()

vmtLogfile = open(outputFilePrefix + subjNumber + subjName + ".log", 'a')
vmtFrameLogfile = outputFilePrefix + subjNumber + subjName + "-frames.log"
psychopy.logging.LogFile(f=vmtLogfile, level=0)
psychopy.logging.info("Subject name: " + subjName)
psychopy.logging.info("Subject number: " + subjNumber)
psychopy.logging.info("Comment: " + subjComment)

VMTdigitSeqs1 = vmt.VMTdigitSequences("pyvdtSequences-rate1.csv")
listOfDigits1 = VMTdigitSeqs1[vmt1LineNumber]

VMTdigitSeqs2 = vmt.VMTdigitSequences("pyvdtSequences-rate2.csv")
listOfDigits2 = VMTdigitSeqs2[vmt2LineNumber]

introductionText = unicode(config.get(language, 'introText'),
                           errors='replace')
pauseText = unicode(config.get(language, 'pauseText'),
                    errors='replace')
endText = unicode(config.get(language, 'endText'),
                  errors='replace')

vmtDate = data.getDateStr()

outputFilename1 = outputFilePrefix + vmtDate + "-1.csv"
outputFilenameAppend1 = outputFilePrefix + "data-1.csv"
outputFilename2 = outputFilePrefix + vmtDate + "-2.csv"
outputFilenameAppend2 = outputFilePrefix + "data-2.csv"


if testMode == "y":
    testOutputFilenameAppend = "testdata.csv"

    for i in range(1, int(testIterations) + 1):
        thisSubjName = subjName + str(i)
        outputFilePrefix = "test-" + thisSubjName + "-"

        print "Generating random data for subject " + thisSubjName + \
            "(" + str(i) + "/" + testIterations + ")..."

        testOutput, testOutputSum = vmt.selftest(listOfDigits1,
                                                 vmtDuration, vmtRate1)
        testOutputFilename = outputFilePrefix + vmtDate + ".csv"

        vmtcsv.vmtRawScoreOutput(testOutput, testOutputFilename)
        vmtcsv.vmtScoreAppend(i,
                              thisSubjName,
                              vmtDate,
                              testOutputSum['hits'],
                              testOutputSum['misses'],
                              testOutputSum['falseAlarms'],
                              testOutputSum['correctRejections'],
                              subjComment,
                              testOutputFilenameAppend)
    print "Self-test done."
    core.quit()

if testMode == "p":
    with open(frameLogFile, 'r') as f:
        frameLog = f.readline()
    frameLog = frameLog.split(",")
    plotFrameIntervals(frameLog)

else:
    myWin = visual.Window((resolutionX, resolutionY),
                          allowGUI=False,
                          fullscr=optFullscreen,
                          color='white',
                          monitor='testMonitor',
                          units='deg',
                          screen=0)

    # ----------------STIMULI START ------------------------------------

    fixationStim = visual.PatchStim(win=myWin,
                                    size=0.2,
                                    pos=[0, 0],
                                    sf=0,
                                    color=(-1, -1, -1))  # Black
    # ----------------STIMULI END --------------------------------------

    # Show introduction ------------------------------------------------
    vmt.showText(myWin, introductionText, fontFace)

    fixationStim.draw()
    myWin.flip()
    core.wait(intervalBetweenTrials)
    myWin.flip(clearBuffer=True)

    # -------------VMT1 start-------------------------------------------
    vmtRate = vmtRate1

    if vmtRate == 1:
        listOfDigits = listOfDigits1

    if vmtRate == 2:
        listOfDigits = listOfDigits2

    vmt1output, vmt1OutputSum = vmt.vmt(myWin,
                                        vmtRate,
                                        vmtDuration,
                                        monitorRefreshRate,
                                        listOfDigits,
                                        fontFace,
                                        fontHeight,
                                        vmtFrameLogfile)

    vmtcsv.vmtRawScoreOutput(vmt1output, outputFilename1)
    vmtcsv.vmtScoreAppend(subjNumber,
                          subjName,
                          vmtDate,
                          vmt1OutputSum['hits'],
                          vmt1OutputSum['misses'],
                          vmt1OutputSum['falseAlarms'],
                          vmt1OutputSum['correctRejections'],
                          subjComment,
                          outputFilenameAppend1)

    # ----------------VMT1 end -----------------------------------------
    core.wait(intervalBetweenTrials)
    vmt.showText(myWin, pauseText, fontFace)

    fixationStim.draw()
    myWin.flip()
    core.wait(intervalBetweenTrials)
    myWin.flip(clearBuffer=True)

    # -------------VMT2 start-------------------------------------------
    vmtRate = vmtRate2

    if vmtRate == 1:
        listOfDigits = listOfDigits1

    if vmtRate == 2:
        listOfDigits = listOfDigits2

    vmt2output, vmt2OutputSum = vmt.vmt(myWin,
                                        vmtRate,
                                        vmtDuration,
                                        monitorRefreshRate,
                                        listOfDigits,
                                        fontFace,
                                        fontHeight,
                                        vmtFrameLogfile)

    vmtcsv.vmtRawScoreOutput(vmt2output, outputFilename2)
    vmtcsv.vmtScoreAppend(subjNumber,
                          subjName,
                          vmtDate,
                          vmt2OutputSum['hits'],
                          vmt2OutputSum['misses'],
                          vmt2OutputSum['falseAlarms'],
                          vmt2OutputSum['correctRejections'],
                          subjComment,
                          outputFilenameAppend2)
    # ----------------VMT2 end -----------------------------------------

    # -------------------- show end text -------------------------------
    core.wait(intervalBetweenTrials)
    vmt.showText(myWin, endText, fontFace)
    core.quit()
