
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
    
    # while traci.simulation.getTime() < 300:
    while traci.simulation.getMinExpectedNumber() > 0:# run until all vehicles have arrived
        traci.simulationStep() # forward one step

        print("\n\n\ncurrent step: ", traci.simulation.getTime())
        
        # print("vehicles info on edge ltoc: ")
        # v_IDs_on_edge1 = traci.edge.getLastStepVehicleIDs("ltoc")
        # print(v_IDs_on_edge1)
        # print("vehicles info on edge ctol: ")
        # v_IDs_on_edge2 = traci.edge.getLastStepVehicleIDs("ctol")
        # print(v_IDs_on_edge2)
        # # add something here to implement your algorithm
        # for v_IDs_i in v_IDs_on_edge1:
        #     print("vehicle ID: ", v_IDs_i, "speed: ", traci.vehicle.getSpeed(v_IDs_i))
        #     print("vehicle ID: ", v_IDs_i, "acceleration: ", traci.vehicle.getAcceleration(v_IDs_i))
        #     print("vehicle ID: ", v_IDs_i, "position: ", traci.vehicle.getPosition(v_IDs_i))

        
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

        # cycle 0 is 42s + 3s + 42s + 3s from time 0 to time 90.
        # set new traffic lights
        if (phaseCurrentStep == 0) and (phasePreviousStep == phasesTotalAmount - 1):
            if (cycleCounter == 1):
                # set a new phase duration only for second cycle (from time 91 to time 152)
                # 13s + 3s + 42s + 3s = 61s
                traci.trafficlight.setPhaseDuration("center", 13)
                # then the third cycle it will change back to default duration 42s
        
            if (cycleCounter == 2):
                # set the third cycle to start from phase 2,  
                # but actually sumo won't do it immediately, from north side aspect, it will take 3s green and 3s for yellow than change to phase2(red)
                # so it has totally phase 0 (3s) phase 1 (3s) phase 2 (42s) and phase 3 (3s) = 51s (from time 152 to time 203) and go to next cycle
                traci.trafficlight.setPhaseDuration("center", 2)

            if (cycleCounter == 3):
                
                # class Phase __init__(self, duration, state, minDur=-1, maxDur=-1, next=(), name='')
                p1 = traci.trafficlight.Phase(5, "GGGggrrrrrGGGggrrrrr", 5, 5, "", "")
                p2 = traci.trafficlight.Phase(5, "yyyyyrrrrryyyyyrrrrr", 5, 5, "", "")
                p3 = traci.trafficlight.Phase(5, "rrrrrGGGggrrrrrGGGgg", 5, 5, "", "")
                p4 = traci.trafficlight.Phase(5, "rrrrryyyyyrrrrryyyyy", 5, 5, "", "")
                # class Logic __init__(self, programID, type, currentPhaseIndex, phases=None, subParameter=None)
                newLogic = traci.trafficlight.Logic("0", 0, 0, [p1, p2, p3, p4], {})
                traci.trafficlight.setCompleteRedYellowGreenDefinition("center", newLogic)
                # it works but it's not early enough. it will finish a phase with 42s (from time 204 to time 245)
                # before our newLogic (after time 246)
                # cylce 3: 42s + 5s + 5s + 5s, from time 204 to time 245, to time 260.

        if (phaseCurrentStep == phasesTotalAmount - 1) and (phasePreviousStep == phasesTotalAmount - 2):
            lastPhaseStepCounter = 0
        if (phaseCurrentStep == phasesTotalAmount - 1):
            lastPhaseStepCounter += 1
            print("lastPhaseStepCounter: ", lastPhaseStepCounter)
            if (cycleCounter == 3): # wait for the last step of cycle 3 to setup logic for cycle 4
                if (lastPhaseStepCounter == traci.trafficlight.getPhaseDuration("center")):
                    print("bingo! ")
                    # class Phase __init__(self, duration, state, minDur=-1, maxDur=-1, next=(), name='')
                    p1 = traci.trafficlight.Phase(6, "GGGggrrrrrGGGggrrrrr", 6, 6, "", "")
                    p2 = traci.trafficlight.Phase(4, "yyyyyrrrrryyyyyrrrrr", 4, 4, "", "")
                    p3 = traci.trafficlight.Phase(6, "rrrrrGGGggrrrrrGGGgg", 6, 6, "", "")
                    p4 = traci.trafficlight.Phase(4, "rrrrryyyyyrrrrryyyyy", 4, 4, "", "")
                    # class Logic __init__(self, programID, type, currentPhaseIndex, phases=None, subParameter=None)
                    newLogic = traci.trafficlight.Logic("0", 0, 0, [p1, p2, p3, p4], {})
                    traci.trafficlight.setCompleteRedYellowGreenDefinition("center", newLogic)
                    # this doesn't work
                    # it cannot recognize p1, its cycle has only phase p2 p3 p4 and repeat without p1

                    # try add this setPhase 
                    traci.trafficlight.setPhase("center", 0)


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