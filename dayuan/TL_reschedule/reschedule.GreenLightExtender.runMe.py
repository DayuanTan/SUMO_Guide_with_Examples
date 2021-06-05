
# @file    rechecule.runMe.py
# @author  Dayuan Tan
# @date    2021 02 18
# @version $Id$


from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import optparse
import random
import xml.etree.ElementTree as ET


# we need to import python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)

    # make sure you change this path to your path
    #/usr/local/Cellar/sumo/1.3.1/......
    dayuanSUMOpath = os.path.join("/usr","local","Cellar","sumo","1.3.1","share","sumo","tools")
    sys.path.append(dayuanSUMOpath)
    print("PATH:",sys.path)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")


from sumolib import checkBinary  
import traci  
import traci.constants as tc # used for subscription
import traci._trafficlight


def run():
    """execute the TraCI control loop"""
    step = 0
    phasePreviousStep = -1
    cycleCounter = 0
    lastPhaseStepCounter = 0
    greenPhaseStepCounter = 0
    
    # while traci.simulation.getTime() < 300:
    while traci.simulation.getMinExpectedNumber() > 0:# run until all vehicles have arrived
        traci.simulationStep() # forward one step

        print("\n\n\ncurrent step: ", traci.simulation.getTime())
     

        
        # print the traffic light information
        print("[TL id]:", "center")
        phaseCurrentStep = traci.trafficlight.getPhase("center")
        print("[phaseCurrentStep]:", phaseCurrentStep)
        print("[phasePreviousStep]:", phasePreviousStep)
        print("[Phase duration]:", traci.trafficlight.getPhaseDuration("center"))
        print("[Phase Name]:", traci.trafficlight.getPhaseName("center"))
        print("[Program]:", traci.trafficlight.getProgram("center"))
        print("[getRedYellowGreenState]:", traci.trafficlight.getRedYellowGreenState("center"))
        allProgramLogicInThisTL = traci.trafficlight.getCompleteRedYellowGreenDefinition("center") #=getAllProgramLogics()
        print("[getAllProgramLogics]:", allProgramLogicInThisTL) # output is 'logic' data structure
        allPhasesOfThisProgramLogicInThisTL = allProgramLogicInThisTL[0].getPhases() # get content
        print("[phases all]:", allPhasesOfThisProgramLogicInThisTL)
        phasesTotalAmount = len(allPhasesOfThisProgramLogicInThisTL)
        print("[phasesTotalAmount]:", phasesTotalAmount) # the length is how much phases this TL program logic has in one cycle

        
        if (phaseCurrentStep == 0) and (phasePreviousStep == phasesTotalAmount - 1):
            cycleCounter += 1
        print("[Cycle Counter]:", cycleCounter)

        # OLD: cycle 0 is 42s + 3s + 42s + 3s from time 0 to time 90.
        # NEW: cycle 0 is 42s + 3s green (0 ~ 45 )
        #                   + 3s (46 ~  48)
        #                   + 42s + 3s green (49 ~ 93)
        #                   + 3s (94 ~ 96)from time 0 to time 96.
        # 97 ~ 141: 42 green + 3 green
        # 142 ~ 144: 3 yellow
        # 145 ~ 189: 42 green + 3 green
        # 190 ~ 192: 3 yellow 
        # Green light extender GLE
        if (phaseCurrentStep == 0) and (phasePreviousStep == phasesTotalAmount - 1): # reset greenPhaseStepCounter at the begin of green light phase
            greenPhaseStepCounter = 0
        if (phaseCurrentStep == 2) and (phasePreviousStep == 1): # reset greenPhaseStepCounter at the begin of green light phase
            greenPhaseStepCounter = 0

        if (phaseCurrentStep == 0) or phaseCurrentStep == 2: #phase 0 and 2 are green lights
            greenPhaseStepCounter += 1
            print("greenPhaseStepCounter:", greenPhaseStepCounter)

            if greenPhaseStepCounter == traci.trafficlight.getPhaseDuration("center"):#  at the last step of green phase
                traci.trafficlight.setPhaseDuration("center", 3) # add 3s more
        
        # for next simulation step
        step += 1
        phasePreviousStep = phaseCurrentStep

    traci.close()
    sys.stdout.flush()

def calAvgWaitTime():
    tree = ET.parse('output/tripinfo.xml') # get the file
    root = tree.getroot() # loc the root

    vCount = 0
    vWaitingTimeTotal = 0
    for tripinfo in root.findall('tripinfo'):
        vCount += 1
        vID = tripinfo.get('id')
        vType = tripinfo.get('vType')
        vDuration = tripinfo.get('duration')
        vRouteLength = tripinfo.get('routeLength')
        vWaitingTime = tripinfo.get('waitingTime')
        vWaitingCount = tripinfo.get('waitingCount')
        vWaitingTimeTotal += float(vWaitingTime)
        #print(vID)
        #print(vType)
        #print(vWaitingTime)


    vWaitingTimeAvg = vWaitingTimeTotal / vCount
    print("vWaitingTimeTotal:", vWaitingTimeTotal)
    print("vCount:", vCount)
    return vWaitingTimeAvg

def get_options():
    optParser = optparse.OptionParser()
    optParser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = optParser.parse_args()
    return options

# this is the main entry point of this script
if __name__ == "__main__":
    options = get_options()

    # this script has been called from the command line. It will start sumo as a
    # server, then connect and run
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    

    # this is the normal way of using traci. sumo is started as a
    # subprocess and then the python script connects and runs
    traci.start([sumoBinary, "-c", "reschedule.sumocfg",
                             "--tripinfo-output", "output/tripinfo.xml"])
    

    # implement my alg
    run()

    # calculate avg waiting time
    vWaitingTimeAvg = calAvgWaitTime()
    print("vWaitingTimeAvg:", vWaitingTimeAvg)