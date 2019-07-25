#!/usr/bin/env python
from __future__ import absolute_import
from __future__ import print_function
import optparse
import os
import sys
import subprocess
import random
import traci
 # author:Aiswarya
 # this code is the SUMO realisation of  "Traffic responsive intersection control algorithm using GPS data" by Craig B. Rafter, Bani Anvari, and Simon Box
 # created on :2018-04-30
 


# we need to import python modules from the $SUMO_HOME/tools directory
try:
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', "tools"))  # tutorial in tests
    sys.path.append(os.path.join(os.environ.get("SUMO_HOME", os.path.join(os.path.dirname(__file__), "..", "..", "..")), "tools"))  # tutorial in docs
    from sumolib import checkBinary  
except ImportError:
    sys.exit("please declare environment variable 'SUMO_HOME' as the root directory of your sumo installation (it should contain folders 'bin', 'tools' and 'docs')")


sumoBinary='sumo'
sumoConfig='gps.sumo.cfg'
sumoCmd = [sumoBinary, "-c", sumoConfig , "--no-warnings" , "True"]


def gpsva(r):
 DUR =[]
 dur = []
 for i in range(len(r)):
   ctphase = traci.trafficlights.getRedYellowGreenState(aa[ic])
   if ( ctphase[i] == "G" ):
     vehs = traci.lane.getLastStepVehicleIDs(r[i])
     if(len(vehs) == 0): nearestvehspeed =0
     else:     nearestvehspeed = traci.vehicle.getSpeed(vehs[0])
     if (nearestvehspeed != 0):
	nearestvehdist = traci.vehicle.getPosition(vehs[0])
        qct = nearestvehdist[0] / nearestvehspeed
     else: 
        nearestvehdist =0
	qct = nearestvehdist * 0.45
     remtime = traci.trafficlights.getNextSwitch(aa[ic]) - traci.simulation.getCurrentTime()
     stageduration1 =max(qct,remtime)
     stageduration2 = min(stageduration1 , maxgreen)
     dur.append(stageduration2)

   else:
     lanevehlen = traci.lane.getLastStepLength(r[i])
     if ( lanevehlen != 0):
       qct = lanevehlen* 0.45
       remtime = traci.trafficlights.getNextSwitch(aa[ic]) - traci.simulation.getCurrentTime()
       stageduration1 = max(qct,remtime)
       stageduration2 = min(stageduration1 , maxgreen)
     else:
       stageduration2 = mingreen
   DUR.append(stageduration2)

 return dur,DUR
   
 
if __name__ == "__main__":
 traci.start(sumoCmd)
 while (traci.simulation.getCurrentTime() < 3600*1000):
  traci.simulationStep()
  global maxgreen ,mingreen
  maxgreen = 50
  mingreen = 10
  aa = traci.trafficlights.getIDList()
  for ic in xrange(len(aa)):
    r = traci.trafficlights.getControlledLanes(aa[ic])
    ids =[1,4,7,10]
    for i in sorted(ids,reverse=True):
      del r[i]
    dur,DUR = gpsva(r)
    rtime = traci.trafficlights.getNextSwitch(aa[ic]) - traci.simulation.getCurrentTime()
    elapsedtime =traci.trafficlights.getPhaseDuration(aa[ic]) - rtime
    if (elapsedtime < max(dur)):
     elapsedtime = elapsedtime+ traci.simulation.getCurrentTime()
    else:
      for i in range(len(DUR)):
        
        d = DUR[i]
        traci.trafficlights.setPhase(aa[ic],i)
        traci.trafficlights.setPhaseDuration(aa[ic], d)
      elapsedtime = 0
      stageduration2 =0
      DUR = []
  step=+1
 traci.close()
 sys.stdout.flush()
  
