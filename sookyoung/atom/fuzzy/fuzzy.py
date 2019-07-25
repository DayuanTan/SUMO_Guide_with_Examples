#!/usr/bin/env python
from __future__ import absolute_import
from __future__ import print_function
import optparse
import os
import sys
import subprocess
import random
import traci

# we need to import python modules from the $SUMO_HOME/tools directory
try:
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', "tools"))  # tutorial in tests
    sys.path.append(os.path.join(os.environ.get("SUMO_HOME", os.path.join(os.path.dirname(__file__), "..", "..", "..")), "tools"))  # tutorial in docs
    from sumolib import checkBinary  
except ImportError:
    sys.exit("please declare environment variable 'SUMO_HOME' as the root directory of your sumo installation (it should contain folders 'bin', 'tools' and 'docs')")


sumoBinary='sumo'
sumoConfig='fuzzy.sumo.cfg'
sumoCmd = [sumoBinary, "-c", sumoConfig , "--no-warnings" , "True"]

def phasepriority(lanes):
  vehlen = []
  Thn = 66
  Thm = 133
  volume = []
  global phasepri , phases,vehlensum
  vehlensum =[]
  phases = []
  indicesmax = []
  indicesmed = []
  indicesmin = []
  phasepri =[]
  for j in xrange(len(lanes)):
    x = traci.lane.getLastStepLength(lanes[j])
    vehlen.append(x)
  ids =[1,4,7,10]
  for i in sorted(ids,reverse=True):
     del vehlen[i]
  for i in range(0,4):
    q = vehlen[i] + vehlen[i+4]
    vehlensum.extend([i,q])
  for j in xrange(len(vehlen)):
    if(vehlen[j] < Thn): volume.append("normal")
    elif(Thn <= vehlen[j] and vehlen[j]<= Thm): volume.append("medium")
    elif(vehlen[j] >Thm): volume.append("long")
    else:pass
  for i in range(0,4):
    if(volume[i] =="normal" and (volume[i+4] == "normal" or volume[i+4] == "medium")):  phasepri.append("min")
    elif(volume[i] =="medium" and volume[i+4] == "normal"):  phasepri.append("min")
    elif(volume[i] =="medium" and volume[i+4] == "medium"):  phasepri.append("medium")
    elif((volume[i] =="long" and volume[i+4] == "normal") or (volume[i] =="normal" and volume[i+4] == "long")):  phasepri.append("medium")
    elif(volume[i] =="normal" and (volume[i+4] == "normal" or volume[i+4] == "medium")):  phasepri.append("min")
    elif(volume[i] =="medium" and volume[i+4] == "normal"):  phasepri.append("min")  
    elif(volume[i] =="long" and (volume[i+4] == "long" or volume[i+4] == "medium")):  phasepri.append("max")
    elif(volume[i] =="long" and volume[i+4] == "long"):  phasepri.append("max")
    else: pass
  indicesmax = [i for i, x in enumerate(phasepri) if x == "max"]
  indicesmed = [i for i, x in enumerate(phasepri) if x == "medium"]
  indicesmin = [i for i, x in enumerate(phasepri) if x == "min"]
  phases = indicesmax + indicesmed + indicesmin
  return phases , phasepri, vehlensum


def setphase(phases , phasepri,vehlensum):
   sorted(vehlensum , key = lambda arrays: vehlensum[:][1] , reverse=True)
   #print(vehlensum)
   PH =[]
   PHH = []
   a = 0
   dur = 0
   DUR=[]
   A=[]
   
   for i in range(0,8,2):
     ph = vehlensum[i]
     phh = vehlensum[i+1]
     PH.append(ph)
     PHH.append(phh)
   for i in range(0,4):
    a = PH[i]
    p1 = phasepri[a]
    if(p1 == "max"): dur = 30
    elif(p1 == "med"): dur = 20
    else: dur = 10
    A.append(a)
    DUR.append(dur)
   return A,DUR

  

#which index of phasepri is phases [0] set phase accorodingly for it and others and their duration max = 30 med = 20 min = 10    

if __name__ == "__main__":
 traci.start(sumoCmd)
 while (traci.simulation.getCurrentTime() < 3600*1000):
  traci.simulationStep()
  aa = traci.trafficlights.getIDList()
  global lanes, A, DUR
  lanes =[]
  for i in xrange(len(aa)):
    lanes = traci.trafficlights.getControlledLanes(aa[i])  
    phases , phasepri,vehlensum =phasepriority(lanes)
    A,DUR=setphase(phases , phasepri,vehlensum)
    for i in range(len(DUR)):
      c = A[i]
      d = DUR[i]
      traci.trafficlights.setPhase(aa[i],c)
      traci.trafficlights.setPhaseDuration(aa[i], d)

  step=+1
 traci.close()
 sys.stdout.flush()
  
