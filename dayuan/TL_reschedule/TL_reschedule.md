

# 1. SUMO files structure.
Before we run the SUMO we need to prepare some needed files, showing as gray parallelograms below:

<img src="./structure.gif"></img>


# 2. node file (reschedule.nod.xml)

We just need 5 nodes, the left end node, and the right end node, the top node and the bottom node, and the center node. We need to write it by hand.

Be careful the node 'center' must be type="traffic_light".


# 3. edge file (reschedule.edg.xml) and type file (reschedule.typ.xml)

We just need 8 road edges which connecting the left end node and the right end node, the top and bottom, the bottom and the top node. 

- The first edge is from left node to center node. 
- The second edge is from center ndoe to left node. 
- The third edge is from right node to center node. 
- The fourth edge is from center ndoe to right node. 
- The fifth edge is from top node to center node. 
- The sixth edge is from center ndoe to top node. 
- The seventh edge is from bottom node to center node. 
- The eighth edge is from center ndoe to bottom node. 

We need to write it by hand.

The default number of lanes for each edge is only one. We want to set it to 2 lanes per edge. So we need a link type file (reschedule.typ.xml), in which we set the parameter numLanes="2". We need to write it by hand.

# 4. road net file (reschedule.net.xml)

Then we generate our road net file using the above two files. 

We used the tool provided by SUMO to generate it.

Run the following command:
```
netconvert --node-files=reschedule.nod.xml --type-files=reschedule.typ.xml --edge-files=reschedule.edg.xml --output-file=reschedule.net.xml
```
		
It will print only one line “Success.” if it successes. And there will be one more file called reschedule.net.xml in the current directory.

It will generate the default traffic light logic inside the net.xml:
```
    <tlLogic id="center" type="static" programID="0" offset="0">
        <phase duration="42" state="GGGggrrrrrGGGggrrrrr"/>
        <phase duration="3"  state="yyyyyrrrrryyyyyrrrrr"/>
        <phase duration="42" state="rrrrrGGGggrrrrrGGGgg"/>
        <phase duration="3"  state="rrrrryyyyyrrrrryyyyy"/>
    </tlLogic>
```
   

PS:
```
 $ netconvert --node-files=reschedule.nod.xml --type-files=reschedule.typ.xml --edge-files=reschedule.edg.xml --tllogic-files=reschedule.tllogic.xml --output-file=reschedule.net.xml
Error: Invalid linkIndex 16 for traffic light 'center' with 16 links.
Quitting (on error).
```

## or use ```netconvert -c reschedule.netccfg```: 

The default traffic light logic inside the net.xml is totally same as above.

```
$ netconvert -c reschedule.netccfg
Loading configuration... done.
Parsing types from 'reschedule.typ.xml'... done.
Parsing nodes from 'reschedule.nod.xml'... done.
Parsing edges from 'reschedule.edg.xml'... done.
 Import done:
   5 nodes loaded.
   1 types loaded.
   8 edges loaded.
Removing self-loops... done (0ms).
Removing empty nodes... done (0ms).
   0 nodes removed.
Moving network to origin... done (0ms).
Computing turning directions... done (0ms).
Assigning nodes to traffic lights... done (0ms).
Sorting nodes' edges... done (0ms).
Computing node shapes... done (1ms).
Computing edge shapes... done (0ms).
Computing node types... done (0ms).
Computing priorities... done (0ms).
Computing approached edges... done (0ms).
Guessing and setting roundabouts... done (0ms).
Computing approaching lanes... done (0ms).
Dividing of lanes on approached lanes... done (0ms).
Processing turnarounds... done (0ms).
Rechecking of lane endings... done (0ms).
Computing traffic light control information... done (0ms).
Computing node logics... done (0ms).
Computing traffic light logics... done (1ms).
 1 traffic light(s) computed.
Building inner edges... done (0ms).
-----------------------------------------------------
Summary:
 Node type statistics:
  Unregulated junctions       : 0
  Priority junctions          : 4
  Right-before-left junctions : 0
  Traffic light junctions      : 1
 Network boundaries:
  Original boundary  : 0.00,-100.00,200.00,100.00
  Applied offset     : 0.00,100.00
  Converted boundary : 0.00,0.00,200.00,200.00
-----------------------------------------------------
Writing network... done (2ms).
Success.
```


# 5. Traffic demanding file

We need to generate randomly a route using python script.

Traffic Demand is the word we use to descripte how many vehicles we will have, types of vehicles, the route of each vehicles.

- A trip is a vehicle movement from one place to another defined by the starting edge (street), the destination edge, and the departure time.
- A route is an expanded trip, that means, that a route definition contains not only the first and the last edge, but all edges the vehicle will pass.

The tool we use here is “tools/randomTrips.py”. 
	
The command is :
``` 
python3 ../../tools/randomTrips.py -n reschedule.net.xml -o reschedule.trips.xml -p 1 --route-file reschedule.rou.xml --allow-fringe --begin 0 --end 300 --fringe-factor 100

```	
	
It will print:
```
calling  /usr/local/opt/sumo/share/sumo/bin/duarouter -n reschedule.net.xml -r reschedule.trips.xml -o reschedule.rou.xml --ignore-errors --begin 0.0 --end 300.0 --no-step-log --no-warnings
Success.
```

Note: Here we need pay attention to the path of randomTrips.py file. Make sure you use the right path to it. In the above example I copied the whole “tools” directory here so I use “tools/randomTrips.py”.


It generated actually three files:
-	reschedule.rou.xml
-	reschedule.rou.alt.xml
-	reschedule.trips.xml

Explanation of option flags we used in this command:

- -n reschedule.net.xml: As input file. Usually it's a network file.
- -o reschedule.trips.xml: As output file. randomTrips.py generates a trip file. Not route file by default.
- -p 1: The arrival rate is controlled by option --period/-p (default 1). By default this generates vehicles with a constant period and arrival rate of (1/period) per second. By using values below 1, multiple arrivals per second can be achieved. In our example, we set it to 1 and if we check the generated trips.xml we can find it generated 300 vehicles for us, one vehicle per second. 
- --begin 0 --end 300: the time. 
- --allow-fringe: Allow departing on edges that leave the network and arriving on edges that enter the network (via turnarounds or as 1-edge trips
- --fringe-factor \<FLOAT\> increases the probability that trips will start/end at the fringe of the network. If the value 10 is given, edges that have no successor or no predecessor will be 10 times more likely to be chosen as start- or endpoint of a trip. This is useful when modelling through-traffic which starts and ends at the outside of the simulated area.

	
How to change:
	
If we want to change the number of vehicles it generated, we can change the option flag “-p”. To the number we want. 

So “-p 0.5” will generate two vehicles per second. With --begin 0 --end 300 together, it will generate 600 vehicles totally.

So “-p 2” will generate 1 vehicle per 2 seconds. With --begin 0 --end 300 together, it will generate 150 vehicles totally.

So “-p 0.857” with --begin 0 --end 300 together, it will generate 350 vehicles totally.

So “-p 0.375” with --begin 0 --end 300 together, it will generate 800 vehicles totally.


# 6. Run SUMO

Then we can run it. 

We need sumo configuration file "reschedule.sumocfg” to run it. In which we declare the net file and rout tile and executing time. 

The command:
```
$ sumo-gui -c reschedule.sumocfg
```

It will print: 
```
Loading configuration... done.
```

# 7. Use TraCI via Python.

"rechecule.runMe.py"


Ref: https://sumo.dlr.de/docs/Simulation/Traffic_Lights.html#controlling_traffic_lights_via_traci

Which functions to use?
https://sumo.dlr.de/docs/TraCI/Change_Traffic_Lights_State.html

See [reschedule.runMe.py](reschedule.runMe.py) showing multiple ways to change different values of next cycle or phase. Corresponding log is "log.2021.02.23.1800_trynewlogic_correct_time_success.txt".

About define and use a new traffic logic please see ***line 114 to 137***. **The key question is to determine when to set the new TL**. The answer should be the last simulation step of current cycle, before the first simulation step of next cycle. That why I used "lastPhaseStepCounter".

(Line 81 to 98 tried how to use *setPhaseDuration*. Line 100 to 112 tried how to use a new logic but have an issue.)

---

See [reschedule.GreenLightExtender.runMe.py](reschedule.GreenLightExtender.runMe.py) and [log.2021.06.04.16.45.GLE.md](log.2021.06.04.16.45.GLE.md) and [tripinfo.2021.06.04.16.45.GLE.xml](output/tripinfo.2021.06.04.16.45.GLE.xml) shows only to extend green lights duration at end of each green light. 