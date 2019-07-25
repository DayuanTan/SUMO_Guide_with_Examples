#!/usr/bin/env python
from __future__ import absolute_import
from __future__ import print_function
import optparse
import os
import sys
import subprocess
import random
import sumolib
import traci

# we need to import python modules from the $SUMO_HOME/tools directory
try:
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', "tools"))  # tutorial in tests
    sys.path.append(os.path.join(os.environ.get("SUMO_HOME", os.path.join(os.path.dirname(__file__), "..", "..", "..")), "tools"))  # tutorial in docs
    from sumolib import checkBinary  
except ImportError:
    sys.exit("please declare environment variable 'SUMO_HOME' as the root directory of your sumo installation (it should contain folders 'bin', 'tools' and 'docs')")


sumoBinary='sumo'
sumoConfig='tapioca.sumo.cfg'
sumoCmd = [sumoBinary, "-c", sumoConfig , "--no-warnings" , "True"]

def intvalues(TFsum):
# initializations
 global lane_oselected, LS, GE , RD, laneoselected,selected
 lane_oselected = []
 laneoselected = []
 LS = []
 GE =[]
 SS= []
 RD=[]
 S= []
 LSS=[]
 GEE=[]
 selected=[]
 RDD=[]
 global r, D , Tmax, Ts, Th, Tf ,TF
 Tf= 0
 veh_id_p = []
 ls = 0
 ge =0
 rd =0
 lss=0
 gee=0
 rdd= 0
 veh_no_p = 0
 V1 =0
 idx = 0
 N1 = 0
 Vd =[]
 N2 = 0
 Nsd= []
# calculations for each lane first and then combine them to get intersection values
 links = traci.trafficlights.getControlledLinks(aa[TLSID])
 #print(links)
 i=0
 for i in range(len(r)): 
  veh_id_p = traci.lane.getLastStepVehicleIDs(r[i])
  veh_no_p = traci.lane.getLastStepVehicleNumber(r[i])
  lane_oselected.extend([i,veh_no_p])
 laneoselected = [lane_oselected[i:i+2] for i in range(0, len(lane_oselected), 2)]
 if(len(laneoselected) >1 ):
  sorted(laneoselected , key = lambda arrays: laneoselected[:][1] , reverse=True)
 else: pass
 j=0
 Nmax = laneoselected[0][1]
 
 for x in range(len(r)):
   l1 = [y[0] for y in links[x]]
   l2 = [y[1] for y in links[x]]
   #print(l1,l2)
   if((l1 != []) or (l2!=[])):
     N1 = traci.lane.getLastStepVehicleNumber(l1[0])
     V1 = traci.lane.getLastStepVehicleNumber(l2[0])
   else:pass
   N2 = N1 + V1
  # print(x )
   Nsd.insert(x,N2)

   Vd.insert(x,V1)
   #print(Nsd,Vd)
 Nab = sum(Nsd)
 #print(Nsd,Vd)
 if((TFsum ==0) or (Nab == 0)):
   selected = r
   #print("s")
 else: 
   #print("n")
   i=0
   for i in range(len(r)):
    ls = (Nsd[i] / Nab ) + ( TF[i] / TFsum)
    ge = Nsd[i] -Vd[i]
    LS.append(ls)
    GE.append(ge)
    rd = (len(r)-i) /len(r)
    RD.append(rd)
   LSsum = sum(LS)
   GEsum = sum(GE)
   RDsum = sum(RD)
   #print(len(LS),len(RD),len(GE))
  #print(LSsum, GEsum , RDsum)
   i=0
   for i in range(len(r)):
    if((LSsum ==0) or (GEsum == 0) or (RDsum ==0)):
      lss=0
      gee=0
      rdd=0
    else:
      lss = LS[i] / LSsum
      gee = GE[i] / GEsum
      rdd = RD[i] / RDsum
    LSS.append(lss)
    GEE.append(gee)
    RDD.append(rdd)
   LSGE = [x + y for x, y in zip(LSS, GEE)]
   u=0
   for u in range(len(r)):
    idx = laneoselected[u][0]
    s = LSGE[idx] + RDD[u]
    SS.extend([s,idx])
   i=0
   S = [SS[i:i+2] for i in range(0, len(SS), 2)]
   sorted(S , key = lambda arrays: S[:][0] , reverse=True)
   i=0
   for i in range(len(r)):
    x = S[i][0]
    selected.append(x)

 return selected,Nmax


if __name__ == "__main__":
 traci.start(sumoCmd)
 while (traci.simulation.getCurrentTime() < 3600*10000):
  traci.simulationStep()
  aa = traci.trafficlights.getIDList()
  step=0
  TF = []
  r =[]
  TF = []
  global TFsum
  TFsum =0
  Tp= 0

  Tmax = 120
  Ts = Th = 4
  for TLSID in xrange(len(aa)): 
   r = traci.trafficlights.getControlledLanes(aa[TLSID])
   D = len(r)
   selected,Nmax = intvalues(TFsum)
   phase =0
   i= 0
   for i in range(len(r)):
    if(r[i] == selected[0]):
      lane1 = i
    else: pass
   if(len(selected)>1):
    for i in range(len(r)):
     if(r[i] == selected[1]):
       lane2 = i
     else: pass
   else: lane2 = lane1
   ctph =traci.trafficlight.getRedYellowGreenState(aa[TLSID])
  #print(ctph,len(ctph))
   n = "r" * len(ctph)
   nt = list(n)

   nt[lane1] = 'G'
   nt[lane2] = 'G'
   ntph = "".join(nt)
  #print(ntph)
   traci.trafficlight.setRedYellowGreenState(aa[TLSID],ntph)

   Tf = traci.simulation.getCurrentTime()
   TF.append(Tf) 
   Tp =  Ts + (Nmax*Th)
   traci.trafficlights.setPhaseDuration(aa[TLSID] , Tp)
  TFsum = sum(TF)
  step=+1
 traci.close()
 sys.stdout.flush()
  
