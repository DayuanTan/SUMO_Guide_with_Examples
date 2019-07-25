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
sumoConfig='atom.sumo.cfg'
sumoCmd = [sumoBinary, "-c", sumoConfig , "--no-warnings" , "True"]


def TFW ():
  l = traci.trafficlights.getControlledLanes(ic[i])
  lanes=[]
  for d in l:
       if d not in lanes:
          lanes.append(d)
  for x in range(len(lanes)):
    edges = traci.lane.getEdgeID(lanes[x])
    S_in.append(edges)
  j=0
  count_r=0
  count_l=0
  count_s= 0
  count_rr = 0
  count_ll = 0
  count_ss =0
  count_ndvr= 0
  count_ndvl= 0
  count_ndvs= 0
  count2_R=0
  count2_L=0
  count2_S = 0
  count_right = []
  count_left = []
  count_straight = []

  for j in xrange(len(S_in)): 
   Fba=S_in[j]
   veh = traci.edge.getLastStepVehicleIDs(Fba)
   phase =traci.trafficlights.getCompleteRedYellowGreenDefinition(ic[i])

   k=0
   elem=0
   v=0
   d=0
   if (len(veh) != 0) :
    for d in veh:
     direction = traci.vehicle.getSignals(d)
     if(direction == 0): count_right.append(d)
     elif(direction == 1): count_left.append(d)
     else: count_straight.append(d)
   else:pass
   global Delay_t_Fba
   Delay_t_Fba = traci.edge.getWaitingTime(Fba)
   global Speed_t_Fba
   Speed_t_Fba = traci.edge.getLastStepMeanSpeed(Fba)
   if(len(count_right) != 0 and len(count_straight) != 0 and len(count_left) != 0) :
     k=0
     for k in range(len(count_right)):					#right
      rou = traci.vehicle.getRoute(count_right[k])
      ro = traci.vehicle.getRouteIndex(count_right[k])
      x = ro+1
      if(x != len(rou)) :
       v1 = traci.edge.getLastStepVehicleIDs(rou[x])
       for elem in v1:
         rou2 = traci.vehicle.getRoute(elem)
         ro2 =  traci.vehicle.getRouteIndex(elem)
         if( rou2[ro2 -1] ==Fba):
           count_r +=1
         else:pass
         pre_edge_vehicles=traci.edge.getLastStepVehicleIDs(rou[ro-1])
         for v in range(len(pre_edge_vehicles)):
          if(traci.vehicle.getNextTLS(pre_edge_vehicles[v]) == ic[i]):
            count2_R+=1
          else:pass
      else: 
       count_r=0
      pre_edge = traci.vehicle.getRoadID(count_right[-1])
      if(pre_edge != Fba):
         count_rr +=1 
      else:pass

      e=0
      for e in count_right:
        roadid = traci.vehicle.getRoadID(e)
        if(roadid ==Fba):
         count_ndvr+=1
        else: pass
     k=0
     for k in range(len(count_straight)):				#straight
      rou = traci.vehicle.getRoute(count_straight[k])
      ro = traci.vehicle.getRouteIndex(count_straight[k])
      x = ro+1
      if(x != len(rou)) :
       v1 = traci.edge.getLastStepVehicleIDs(rou[x])
       for elem in v1:
         rou2 = traci.vehicle.getRoute(elem)
         ro2 =  traci.vehicle.getRouteIndex(elem)
         if( rou2[ro2 -1] ==Fba):
           count_s +=1
         else:pass
         pre_edge_vehicles=traci.edge.getLastStepVehicleIDs(rou[ro-1])
         for v in range(len(pre_edge_vehicles)):
          if(traci.vehicle.getNextTLS(pre_edge_vehicles[v]) == ic[i]):
           count2_S+=1
          else: count_ss += 1  
      else: 
       count_s=0
      pre_edge = traci.vehicle.getRoadID(count_straight[-1])
      if(pre_edge != Fba):
         count_ss +=1 
      else:pass
      pre_edge_vehicles=traci.edge.getLastStepVehicleIDs(rou[ro-1])
      for v in range(len(pre_edge_vehicles)):
        if(traci.vehicle.getNextTLS(pre_edge_vehicles[v]) == ic[i]):
          count2_S+=1
        else: count_ss += 1  
      e=0
      for e in count_straight:
        roadid = traci.vehicle.getRoadID(e)
        if(roadid ==Fba):
         count_ndvs+=1
        else: pass
     k=0
     for k in range(len(count_left)):					#left
      rou = traci.vehicle.getRoute(count_left[k])
      ro = traci.vehicle.getRouteIndex(count_left[k])
      x = ro+1
      if(x != len(rou)) :
       v1 = traci.edge.getLastStepVehicleIDs(rou[x])
       for elem in v1:
         rou2 = traci.vehicle.getRoute(elem)
         ro2 =  traci.vehicle.getRouteIndex(elem)
         if( rou2[ro2 -1] ==Fba):
           count_l +=1
         else:pass
         pre_edge_vehicles=traci.edge.getLastStepVehicleIDs(rou[ro-1])
         for v in range(len(pre_edge_vehicles)):
           if(traci.vehicle.getNextTLS(pre_edge_vehicles[v]) == ic[i]):
            count2_L+=1
           else:pass 
      else: 
       count_l=0
      pre_edge = traci.vehicle.getRoadID(count_left[-1])
      if(pre_edge != Fba):
         count_ll +=1 
      else:pass
       
     e=0
     for e in count_left:
        roadid = traci.vehicle.getRoadID(e)
        if(roadid ==Fba):
         count_ndvl+=1
        else: count_ll += 1
   elif((len(count_right) != 0 or len(count_straight) != 0) and len(count_left) == 0) : 
     count_ll = count_l = count2_L = count_ndvl = 0
     k=0
     for k in range(len(count_right)):					#right
      rou = traci.vehicle.getRoute(count_right[k])
      ro = traci.vehicle.getRouteIndex(count_right[k])
      x = ro+1
      if(x != len(rou)) :
       v1 = traci.edge.getLastStepVehicleIDs(rou[x])
       for elem in v1:
         rou2 = traci.vehicle.getRoute(elem)
         ro2 =  traci.vehicle.getRouteIndex(elem)
         if( rou2[ro2 -1] ==Fba):
           count_r +=1
         else:pass
         pre_edge_vehicles=traci.edge.getLastStepVehicleIDs(rou[ro-1])
         for v in range(len(pre_edge_vehicles)):
           if(traci.vehicle.getNextTLS(pre_edge_vehicles[v]) == ic[i]):
             count2_R+=1
           else:count_rr +=1
      else: 
       count_r=0
      pre_edge = traci.vehicle.getRoadID(count_right[-1])
      if(pre_edge != Fba):
         count_rr +=1 
      else:pass
 
     e=0
     for e in count_right:
        roadid = traci.vehicle.getRoadID(e)
        if(roadid ==Fba):
         count_ndvr+=1
        else: pass
     k=0
     for k in range(len(count_straight)):				#straight
      rou = traci.vehicle.getRoute(count_straight[k])
      ro = traci.vehicle.getRouteIndex(count_straight[k])
      x = ro+1
      if(x != len(rou)) :
       v1 = traci.edge.getLastStepVehicleIDs(rou[x])
       for elem in v1:
         rou2 = traci.vehicle.getRoute(elem)
         ro2 =  traci.vehicle.getRouteIndex(elem)
         if( rou2[ro2 -1] ==Fba):
           count_s +=1
         else:pass
         pre_edge_vehicles=traci.edge.getLastStepVehicleIDs(rou[ro-1])
         for v in range(len(pre_edge_vehicles)):
            if(traci.vehicle.getNextTLS(pre_edge_vehicles[v]) == ic[i]):
             count2_S+=1
            else: count_ss += 1  
      else: 
       count_s=0
      pre_edge = traci.vehicle.getRoadID(count_straight[-1])
      if(pre_edge != Fba):
         count_ss +=1 
      else:pass
      
     e=0
     for e in count_straight:
        roadid = traci.vehicle.getRoadID(e)
        if(roadid ==Fba):
         count_ndvs+=1
        else: pass
   elif ((len(count_right) == 0 or len(count_straight) == 0) and len(count_left) != 0) :           
     k=0
     for k in range(len(count_left)):					#left
      rou = traci.vehicle.getRoute(count_left[k])
      ro = traci.vehicle.getRouteIndex(count_left[k])
      x = ro+1
      if(x != len(rou)) :
       v1 = traci.edge.getLastStepVehicleIDs(rou[x])
       for elem in v1:
         rou2 = traci.vehicle.getRoute(elem)
         ro2 =  traci.vehicle.getRouteIndex(elem)
         if( rou2[ro2 -1] ==Fba):
           count_l +=1
         else:pass
         pre_edge_vehicles=traci.edge.getLastStepVehicleIDs(rou[ro-1])
         for v in range(len(pre_edge_vehicles)):
          if(traci.vehicle.getNextTLS(pre_edge_vehicles[v]) == ic[i]):
             count2_L+=1
          else:pass  
      else: 
       count_l=0
      pre_edge = traci.vehicle.getRoadID(count_left[-1])
      if(pre_edge != Fba):
         count_ll +=1 
      else:pass

     e=0
     for e in count_left:
        roadid = traci.vehicle.getRoadID(e)
        if(roadid ==Fba):
         count_ndvl+=1
        else: count_ll += 1
     count_rr =0 
     count_r = 0
     count2_R = 0
     count_ndvr = 0
     count_ss = 0
     count_s = 0
     count2_S =0 
     count_ndvs = 0
   else:
     CL_t_ic =  0
     CL_t_Fba=  []
     CL_t_ph = []
     Delay_t_ic=0.5
     TH_t_ic=0.5
     OR_t_ic=0.5
     dur_t1_ph=[]
     dur_CYC_t1 =120  
   #print( count2_R,count_r,count_rr,count_ndvr)
   NEV_t1_Fba.extend([count2_R ,count2_L ,count2_S])
   TH_t_Fba.extend([count_r ,count_l ,count_s])
   NAV_t_Fba.extend([count_rr ,count_ll ,count_ss]) 
   NDV_t_Fba.extend([count_ndvr ,count_ndvl ,count_ndvs])
   j+=1
   Delay_Fba.append(Delay_t_Fba)
#end of for loop
  #print(TH_t_Fba, NEV_t_Fba , NDV_t1_Fba,Delay_t1_Fba)

  NEV_t_ic =sum(NEV_t1_Fba) 
  TH_t_ic= sum(TH_t_Fba)
  NAV_t_ic=sum(NAV_t_Fba)
  NDV_t_ic=sum(NDV_t_Fba)
  m=0
  ll=0
  p=0
  qq = 0
  OR_t_Fba = []
  for m in range(len(lanes)) :
    CP= traci.lane.getLength(lanes[m])/7
    ll = NDV_t_Fba[m] + NAV_t_Fba[m]
    qq = Delay_t_Fba*((ll)/CP)
    OR_t_Fba.append(qq)
  OR_t_ic = sum(OR_t_Fba)/N_in
  CL_t_Fba =[]
  dur_t1_ph =  []
  CL_Fba=0
  dur_ph =0 
  for p in range(len(l)) : 
    if(OR_t_ic!=0 and TH_t_Fba[p]!=0 and NEV_t_ic!=0 ):
      CL_Fba =  (OR_t_Fba[p]/OR_t_ic) + (TH_t1_ic/TH_t_Fba[p]) + (NEV_t1_Fba[p]/NEV_t_ic)
    else : CL_Fba = 0
    CL_t_Fba.append(CL_Fba)
    if(Speed_t_Fba != 0):
          dur_ph = (avl*(NDV_t_Fba[p]+NAV_t_Fba[p]+NEV_t1_Fba[p]))/Speed_t_Fba
    else:
          dur_ph = (avl*(NDV_t_Fba[p]+NAV_t_Fba[p]+NEV_t1_Fba[p]))/0.1
    dur_t1_ph.append(dur_ph)
    dur_CYC_t1= sum(dur_t1_ph)
  k=0 
  CL_t_ph =[]
  g_index = []
  ALL_ph = traci.trafficlights.getCompleteRedYellowGreenDefinition(ic[i]) 
  for k in range(len(ALL_ph)):
    logics =ALL_ph[k]
    #print(logics)
    ph = logics.getPhases()
    ph0 = ph[0]
    ctph = ph0._phaseDef
    for w in range(len(ctph)):
      if(ctph[w] == 'g' or ctph[w] == 'G'):
        g_index.append(w)
      else:pass
      #print(g_index)
    CL_ph = sum(CL_t_Fba[y] for y in g_index)
    CL_t_ph.append(CL_ph)
  #print(CL_t_ph)
  Delay_t_ic = sum(Delay_Fba) / N_in  
  TH_t_ic = sum(TH_t_Fba) /N_in  
  NDV_t_ic = sum(NDV_t_Fba) / N_in  
  CL_t_ic =  sum(CL_t_Fba)/ N_in
  return (CL_t_ic , CL_t_Fba,CL_t_ph  ,Delay_t_ic,Delay_t1_ic,TH_t_ic,TH_t1_ic,OR_t_ic,dur_t1_ph,dur_CYC_t1,TH_t1_Fba ,TH_t_Fba ,Delay_Fba,Delay_t1_Fba ,NEV_t_Fba,NEV_t1_Fba ,NDV_t_Fba,NDV_t1_Fba )
  
def CMD (OR_t_ic , CL_t_ic ,Delay_t_ic,Delay_t1_ic,TH_t_ic,TH_t1_ic,OR_t_Fba,Mode_ic,P_ffp):
  if (OR_t_ic <= P_ffp):
    if (Mode_ic != all(g[i] for i in range(0,3))):
      Mode_ic = g[0]
      #print("a")
    elif( (TH_t1_ic >= TH_t_ic) and ( Delay_t1_ic <= Delay_t_ic )):   
      if ( Mode_ic == g[3]):
       # print("b")
        Mode_ic = g[4]
        P_ffp = OR_t_ic
      else: 
	if( Mode_ic == g[1]):
          #print("c")
          Mode_ic = g[2]
        else:
          Mode_ic = g[1] 
       
  else:
    if (Mode_ic == g[3]):
      if( ((OR_t_ic > P_ffp) and (TH_t1_ic >=TH_t_ic)  and  (Delay_t1_ic <= Delay_t_ic)) or any(OR_t_Fba[i] > P_ffp for i in range(len(l))) ):
        Mode_ic = g[4]
        #print("d")
      else: pass
    elif ( Mode_ic == g[2]):
      if(OR_t_ic > P_ffp):
        Mode_ic = g[3]
        #print("e")
      else: pass
    elif (Mode_ic == g[4]):
      if((CL_t_ic > P_ffp) and all(OR_t_Fba[i] <= P_ffp for i in range(len(l)))):
        Mode_ic = g[3]
        #print("f")
      else: pass
    else: pass	
  #print(P_ffp , OR_t_ic)	   
  return Mode_ic


def PS (CL_t_Fba,dur_t1_Fba,dur_t_Fba):
  global PH_CYC_t,dur_t1_ph 
  if (Mode_ic == g[0]):
    pass
  elif( Mode_ic == g[1] or Mode_ic == g[2] or Mode_ic == g[3] ):
    phase = traci.trafficlights.getCompleteRedYellowGreenDefinition(ic[i])
    arr1 = [list(l) for l in zip(CL_t_ph , phase)] 
    sorted(arr1, key=lambda arrays: arr1[0][:] ,reverse=True)
    for row in arr1:
      del row[0]
    PH_CYC_t = arr1 
  elif( Mode_ic == g[4] ):  
    PH_CYC_t = []
    Tmp_f = traci.trafficlights.getControlledLanes(ic[i])
    for p in range(len(Tmp_f)):
      ALL_ph = traci.trafficlights.getCompleteRedYellowGreenDefinition(ic[i]) 
      #print(ALL_PH, dur_t1_Fba, dur_t_Fba)
      for ph in ALL_ph :
        if(dur_t1_Fba - dur_t_Fba < 10):
          PH = ph
        else:pass
        PH_CYC_t.append(PH)
      dur_t1_ph = max(dur_t1_Fba)
      Tmp_f.pop(p) 
  #print("a")
  return (PH_CYC_t,dur_t1_ph)


def DA (TH_t1_Fba ,TH_t_Fba ,Delay_Fba,Delay_t1_Fba ,NEV_t_Fba,NEV_t1_Fba ,NDV_t_Fba,NDV_t1_Fba):
  global dur_t_Fba,dur_t1_Fba
  dur_t_Fba = dur_t1_Fba
  if (Mode_ic == g[0] or Mode_ic == g[1]):  
     dur_t1_Fba = dur_t_Fba
  elif(Mode_ic == g[2] or Mode_ic == g[3]):  
    dur_t1_Fba = dur_t_Fba
  else:  ####if(Mode_ic == CFP):   change
   CR=1
   t=0
   for t,tt in zip(range(N_in,len(Delay_t1_Fba))):
    if((TH_t1_Fba[t] !=0) and (Delay_t1_Fba[tt]!=0) and  (NDV_t1_Fba[t] !=0) and (NEV_t_Fba[t] != 0)):    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
     R_th= TH_t_Fba[t] / TH_t1_Fba[t]
     R_delay = Delay_Fba[tt] / Delay_t1_Fba[tt]
     R_ndv = NDV_t_Fba[t]/NDV_t1_Fba[t]
     R_nev = NEV_t1_Fba[t]/NEV_t_Fba[t]
     if (R_th >1):
      if(R_delay <=1):
        if(R_ndv <=1):
          CR = 1
        else:
          CR = R_ndv
      else:
        if(R_ndv <=1):
          CR = 1
        else:
          CR = R_ndv  
     else:
      if(R_th <=1):
        if(R_ndv > 1):
          CR = 1
        else:
          CR = R_delay
      else:
        if(R_ndv > 1):
          CR = 1
        else:
          CR = R_th
     dur_t1_Fba = dur_t_Fba * CR  #### till here
     
  if (dur_t1_Fba > MDT ):
      pass
  else:
      dur_t1_Fba = 0

  
  return dur_t1_Fba
   


if __name__ == "__main__":
 traci.start(sumoCmd)
 while (traci.simulation.getCurrentTime() <3600*1000):
  traci.simulationStep()
  ic = traci.trafficlights.getIDList()
#ATOM operation starts hereee
  step=0
  i=0
  j=0
  k=0
  PH = ""
  ph = ""
  MDT = 5 			#seconds

  dur_CYC_t = 120    #seconds
  CP = 28.5               	# 200/7
  dur_t_Fba =0
  dur_t1_ph= 0
  dur_t1_Fba =0
  avl = 7
  y=0
  w=0
  g =[ 'FFP_1','FFP_2','FFP_3', 'r2l','cfp'] 
  global Mode_ic , hmd , caldur
  Mode_ic = ''
  caldur =0
  hmd =0
  global phase,CL_t_Fba, CL_t_ph,CL_t_ic, NAV_t1_Fba , NEV_t_Fba,  TH_t_Fba , OR_t_Fba,OR_t_ic , NAV_t_Fba,TH_t1_ic,TH_t_ic,NEV_t1_Fba,NDV_t1_Fba , NDV_t_Fba
  global Delay_t_ic,TH_t1_Fba,Delay_t1_ic,Delay_Fba ,Delay_t1_Fba
  Delay_t_ic =0
  CL_t_ic =  0
  OR_t_ic = 0
  NAV_t_ic = 0
  Delay_Fba=[]
  NDV_t_ic = 0
  NEV_t_ic = 0
  TH_t_ic = 0
  NAV_t_Fba=[]
  NDV_t_Fba=[]
  NDV_t1_Fba=[]
  TH_t_Fba=[]
  TH_t_ic= 0 
  TH_t1_Fba =[]
  Delay_t_Fba=[]
  NEV_t_Fba = []
  NEV_t1_Fba = []
  NEV_t_ic = 0
  OR_t_Fba = [] 
  Delay_t1_Fba = []
  NDV_t_Fba = [] 
  TH_t_Fba = []
  NAV_t1_Fba = []
  NAV_t_Fba = []
  CL_t_Fba= []
  CL_t_ph = []
  TH_t1_ic = 0
  Delay_t1_ic = 0
  global P_ffp
  for i in xrange(len(ic)):
   P_ffp=0.5 
   ct_time = 0
   dur_CYC_t1= 0
   CL_t_Fba =  []
   l = traci.trafficlights.getControlledLanes(ic[i])
   N_in =len(l)
   phase =traci.trafficlights.getCompleteRedYellowGreenDefinition(ic[i]) 
   dur_t_Fba = dur_CYC_t/len(phase) 
   Delay_t1_ic=Delay_t_ic
   NEV_t_Fba = NEV_t1_Fba 
   NAV_t1_Fba = NAV_t_Fba 
   NDV_t1_Fba = NDV_t_Fba
   TH_t1_ic = TH_t_ic 
   TH_t1_Fba = TH_t_Fba
   Delay_t1_Fba = Delay_Fba
   if(step == ct_time+dur_CYC_t1):
    S_in = []
    global PH_CYC_t , CL_t_ph 			#list of phases for the cycle at t
    PH_CYC_t = [] 
    global phase
    CL_t_ic , CL_t_Fba,CL_t_ph  ,Delay_t_ic,Delay_t1_ic,TH_t_ic,TH_t1_ic,OR_t_ic,dur_t1_ph,dur_CYC_t1,TH_t1_Fba ,TH_t_Fba ,Delay_t_Fba,Delay_t1_Fba ,NEV_t_Fba,NEV_t1_Fba ,NDV_t_Fba,NDV_t1_Fba=TFW()
    Mode_ic =CMD(OR_t_ic , CL_t_ic ,Delay_t_ic,Delay_t1_ic,TH_t_ic,TH_t1_ic,OR_t_Fba,Mode_ic,P_ffp)
    #print(Mode_ic)
    if (Mode_ic == g[0]):   
      #print("ffp1") 
      dur_CYC_t1 = Delay_t_ic * len(phase)
      traci.trafficlights.setPhaseDuration( ic[i] ,dur_CYC_t1)
    elif(Mode_ic == g[1] ): 
      #print("ffp2")  
      PH_CYC_t,dur_t1_ph = PS(CL_t_Fba,dur_t1_Fba,dur_t_Fba)
      dur_CYC_t1 = sum(dur_t1_ph)  
      for o in range(len(PH_CYC_t)) : 
       PH1 = ''.join(PH_CYC_t[o])
       phase =traci.trafficlights.getCompleteRedYellowGreenDefinition(ic[i])
       y =phase.index(PH1)
       traci.trafficlights.setPhase(ic[i],y)
      for q in range(len(dur_t1_ph)) : 
       tt = int(float(dur_t1_ph[q]))
       traci.trafficlights.setPhaseDuration(ic[i], tt)                   
     # traci.trafficlights.setPhaseDuration( ic[i] , dur_t1_ph)
    elif(Mode_ic == g[2] or Mode_ic == g[3]):
      #print("ffp3")  
      dur_t1_Fba = DA(TH_t1_Fba ,TH_t_Fba ,Delay_t_Fba,Delay_t1_Fba ,NEV_t_Fba,NEV_t1_Fba ,NDV_t_Fba,NDV_t1_Fba)
      PH_CYC_t,dur_t1_ph = PS(CL_t_Fba,dur_t1_Fba,dur_t_Fba)
      dur_CYC_t1 =sum(dur_t1_ph)                      #summation of dur_t1_ph
      for o in range(len(PH_CYC_t)) : 
       PH2 = ''.join(PH_CYC_t[o])
       phase =traci.trafficlights.getCompleteRedYellowGreenDefinition(ic[i])
       traci.trafficlights.setPhase(ic[i],ww)
      for q in range(len(dur_t1_ph)) : 
        ttt = int(float(dur_t1_ph[q]))        
        traci.trafficlights.setPhaseDuration(ic[i], ttt)  
    else :	######if(Mode_ic == CFP) :        change  
      #print("cfp")                 
      dur_t1_Fba = DA(TH_t1_Fba ,TH_t_Fba ,Delay_t_Fba,Delay_t1_Fba ,NEV_t_Fba,NEV_t1_Fba ,NDV_t_Fba,NDV_t1_Fba)
      PH_CYC_t,dur_t1_ph = PS(CL_t_Fba,dur_t1_Fba,dur_t_Fba)
      dur_CYC_t1 =sum(dur_t1_ph)    		         #summation of dur_t1_ph    
      for o in range(len(PH_CYC_t)) : 
       PH2 = ''.join(PH_CYC_t[o])
       phase =traci.trafficlights.getCompleteRedYellowGreenDefinition(ic[i])
       ww = phase.index(PH2)
       traci.trafficlights.setPhase(ic[i],ww)
      for q in dur_t1_ph : traci.trafficlights.setPhaseDuration(ic[i], q)
   ct_time = traci.simulation.getCurrentTime()
   step=+1
   
 traci.close()
 sys.stdout.flush()
  
