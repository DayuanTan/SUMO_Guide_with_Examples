
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


def run():
    """execute the TraCI control loop"""
    step = 0
    
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
        print("[Phase]:", phaseCurrentStep)
        print("[Phase duration]:",traci.trafficlight.getPhaseDuration("center"))
        print("[Phase Name]:", traci.trafficlight.getPhaseName("center"))
        print("[Program]:", traci.trafficlight.getProgram("center"))
        print("[getRedYellowGreenState]:", traci.trafficlight.getRedYellowGreenState("center"))
        allProgramLogicInThisTL = traci.trafficlight.getCompleteRedYellowGreenDefinition("center")
        print("[getAllProgramLogics]:", allProgramLogicInThisTL) # output is 'logic' data structure
        allPhasesOfThisProgramLogicInThisTL = allProgramLogicInThisTL[0].getPhases() # get content
        print("[phases all]:", allPhasesOfThisProgramLogicInThisTL)
        phasesTotalAmount = len(allPhasesOfThisProgramLogicInThisTL)
        print("[phasesTotalAmount]:", phasesTotalAmount) # the length is how much phases this TL program logic has in one cycle

        # set new traffic lights

        step += 1
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