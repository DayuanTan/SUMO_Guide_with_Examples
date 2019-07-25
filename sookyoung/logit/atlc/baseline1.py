#!/usr/bin/env python
from __future__ import absolute_import
from __future__ import print_function
import optparse
import os
import sys
import subprocess
import random
import traci
import sumolib
import heapq
	
# we need to import python modules from the $SUMO_HOME/tools directory
try:
    sys.path.append(os.path.join(os.path.dirname(
        __file__), '..', '..', '..', '..', "tools"))  # tutorial in tests
    sys.path.append(os.path.join(os.environ.get("SUMO_HOME", os.path.join(
        os.path.dirname(__file__), "..", "..", "..")), "tools"))  # tutorial in docs
    from sumolib import checkBinary  
except ImportError:
    sys.exit("please declare environment variable 'SUMO_HOME' as the root directory of your sumo installation (it should contain folders 'bin', 'tools' and 'docs')")


sumoBinary='sumo'
sumoConfig='atlc.sumo.cfg'
sumoCmd = [sumoBinary, "-c", sumoConfig , "--no-warnings" , "True","--log", "logfile.txt"]

 


##### traffic data function
##### called per time solt whenevery the next phase is picked, 
##### Collect real-time traffic data such as traffic vol., avg. waiting time, # of stops of each car
def trafficdata (): 
  i=0
  j=0
  d =0
  arr2=[]
  arr1 = []
  gld=0 
  cc=[]
  ccc =[]
  for i in xrange(len(r)): # configure traffic vol., for each lane
    vehicles= []   
    tvl = []         
    wtl = []        
    nsl = []       
    tvl = traci.lane.getLastStepVehicleNumber(r[i])
    wtl=traci.lane.getWaitingTime(r[i])
    nsl=traci.lane.getLastStepHaltingNumber(r[i])
    b=0.5
    l_bc = []    
    
    blanks = 1 - traci.lane.getLastStepOccupancy(r[i]) 
    #print(blanks)
    bc = blanks * traci.lane.getLength(r[i])
    #print(a[TLSID],case_matrix)
    p = traci.trafficlight.getRedYellowGreenState(a[TLSID])
    allp = traci.trafficlight.getCompleteRedYellowGreenDefinition(a[TLSID])
    g_allp = allp.count("G")
    g = p.count("G")
    if g_allp !=0:
     hl = g / g_allp
    else:
     hl=1 
    gld = (b*wtl)+(b*tvl)+(b*nsl)+(b*hl)+(b*bc) 
    arr1.extend([gld,i])
  j=0
  while j<len(arr1):
    arr2.append(arr1[j:j+2])
    j+=2
  sorted(arr2, key=lambda arrays: arr2[:][0] )
  c = list(heapq.nlargest(2, arr2,key=None))
  #print(c)
  if (len(c) == 2 ):
   l1 = c[0][1]
   l2 = c[1][1]
  else: l1 = l2 = c[0][1]
  ctph =traci.trafficlight.getRedYellowGreenState(a[TLSID])
  #print(ctph,len(ctph))
  n = "r" * len(ctph)
  nt = list(n)

  nt[l1] = 'G'
  nt[l2] = 'G'
  ntph = "".join(nt)
  #print(ntph)
  traci.trafficlight.setRedYellowGreenState(a[TLSID],ntph)

####### duration function

  v1 = []
  v2 = []
  t1 = []
  t2 = []
  n1 = 0
  n2 = 0
  lane1 = r[l1]
  lane2 = r[l2]
  tv1 = traci.lane.getLastStepVehicleNumber(lane1)
  tv2 = traci.lane.getLastStepVehicleNumber(lane2)
  v1 =traci.lane.getLastStepVehicleIDs(lane1)
  v2 =traci.lane.getLastStepVehicleIDs(lane2)
  count1 = traci.lane.getLastStepVehicleNumber(lane1)
  count2 = traci.lane.getLastStepVehicleNumber(lane2)
  s1 =traci.lane.getLastStepMeanSpeed(lane1)
  s2 =traci.lane.getLastStepMeanSpeed(lane2)
  if (s1 == 0 or s2 ==0):
    len_p=0
  else:  len_p = max(tv1, tv2) / max(s1,s2)

  trm = 0
  tmax = 50
  thd = tmax - len_p
  if (tv1 ==0 or tv2==0 ): 
    #duration = len_p + thd

    traci.trafficlight.setPhaseDuration(a[TLSID], 11 )    
  else:
    pre_edge1 =  traci.vehicle.getRoadID(v1[0])
    pre_edge2 =  traci.vehicle.getRoadID(v2[0]) 
    pre_tls1 = traci.vehicle.getNextTLS(v1[0])
    pre_tls2 =traci.vehicle.getNextTLS(v2[0])
    #print(pre_tls1,pre_tls2)
    if(pre_tls1==[] or pre_tls2==[]):
     if( len(pre_tls1)==0 and len(pre_tls2)!=0 ):
      p2 = pre_tls2[0][0]
      p1=p2
     elif(len(pre_tls2)==0 and len(pre_tls1)!=0):
      p1  =pre_tls1[0][0]
      p2=p1
     else: 
      p1 = a[TLSID]
      p2 = p1
    else: 
     p1  =pre_tls1[0][0]
     p2  =pre_tls2[0][0]

    nextswitch1 = traci.trafficlight.getNextSwitch(p1)
    nextswitch2 = traci.trafficlight.getNextSwitch(p2)
    currenttime1 = traci.simulation.getCurrentTime()
    currenttime2 = traci.simulation.getCurrentTime()
    trm1 = nextswitch1 - currenttime1
    trm2 = nextswitch2 - currenttime2
    mintrm = min(trm1,trm2) 
    t1 = traci.edge.getLastStepVehicleIDs(pre_edge1)
    t2 = traci.edge.getLastStepVehicleIDs(pre_edge2)
    n1 = traci.vehicle.getNextTLS(t1[0])
    n2 = traci.vehicle.getNextTLS(t2[0])

    if ( n1 != a[TLSID] and n2 != a[TLSID] ):    ##########change to m
     len_o = 0
    elif n1 != a[TLSID] :   ##########change to m
     if trm2>=thd:
	  len_o = thd
     else:
	  len_o = trm2
    elif n2!= a[TLSID] :    ##########change to m
     if trm1>=thd:
    	  len_o = thd
     else:
	  len_o = trm1
    else:
     if(mintrm>=thd):
  	len_o = thd
     else:
	len_o = mintrm
    duration = len_p + len_o +0.1
    if(duration < 100):
      traci.trafficlight.setPhaseDuration(a[TLSID],duration)    
    else:
       traci.trafficlight.setPhaseDuration(a[TLSID],100)

   


if __name__ == "__main__":

 traci.start(sumoCmd)
 while ((traci.simulation.getCurrentTime() < 3600*1000)) :
  traci.simulationStep()
  a=[]
  TLSID=0
  step=0
  a =   traci.trafficlight.getIDList()
  for TLSID in xrange(len(a)): 
   r = traci.trafficlight.getControlledLanes(a[TLSID])
   trafficdata()
   TLSID+=1
   step=+1
   
 traci.close()
 sys.stdout.flush()







