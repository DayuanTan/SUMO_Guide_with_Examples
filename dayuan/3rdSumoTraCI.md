# 3rd SUMO project using TraCI

This is a SUMO example using [**TraCI**](https://sumo.dlr.de/docs/TraCI.html).


I want to implement this road network:

<img src="./imgs/2nd/2ndSimpleSumoRoadNet.png" />

## Example description
Our example plays on a simple signalized intersection with four approaches. We only have traffic on the horizontal axis and important vehicles (like trams, trains, fire engines, ...) on the vertical axis from north to south. On the approach in the north we have an induction loop to recognize entering vehicles. While no vehicle enters from the north we give green on the horizontal axis all the time but when a vehicle enters the induction loop we switch the signal immediately so the vehicle can cross the intersection without a stop. [1]


## Step 1: Nodes
    
All nodes are set up in ["dayuan.cross.nod.xml"](../docs/tutorial/traci_tls_dyt/data/dayuan.cross.nod.xml) file. In this file, each node is assigned with its coordinates (x,y).

The definitions of the attributes in the node file are listed below.

- (a) id: the ID name of the node, defined by users with numbers, word strings or both.
- (b) x: the x-coordinate location of the defined node (in meters)
- (c) y: the y-coordinate location of the defined node (in meters)
- (d) type: the signal control type of the defined node. It is an optional attribute and defined with priority and traffic_light for unsignalized and signalized intersections respectively.

## Step 2: Edges (links)

All edges (road segments, or called "link" in SUMO) are set up in ["dayuan.cross.edg.xml"](../docs/tutorial/traci_tls_dyt/data/dayuan.cross.edg.xml) file.

The defined attributes include:

- (a) id: link ID, defined by users with numbers, word strings or both.
- (b) from: ID of the upstream node of the respective link.
- (c) to: ID of the downstream node of the respective link.
- (d) priority: driving priority based on traffic regulations and is defined with numbers. The higher the number, the higher the priority for the respective road. The priority information will override information from the node file, if both of them exist.
- (e) numLanes: number of lanes on the respective road.
- (f) speed: maximum allowed link speed.
- // We can also put priority, numLanes, speed properties in a seperate *.typ.xml as [example 2](2ndSimpleSumo.md).
- // (g) type: ID of the link type, defined in the link type file. 
- // (h) allow/disallow: ID of the vehicle group which is defined in the SUMO and might not be identical with the vehicle types defined by users. 




## Step 3: Connections between lanes

Each edges are connected with others. The connection between edges are set up in in ["dayuan.cross.con.xml"](../docs/tutorial/traci_tls_dyt/data/dayuan.cross.con.xml) file.

```
NOTE: If each edge has more than 2 lanes, they can not connect to each other freely. The connection between each lanes are set up in "dayuan.cross.con.xml" file using "fromLane/toLane" attributes, see more on 2nd example.
```

The meaning of each attribute is as following:

- (a) from: ID of the link which the traffic movements will be specified.
- (b) to: ID of the link which is the downstream link of the above defined link.
- // (c) fromLane/toLane: lane number of the defined link in (a) and the lane number of the link in (b), which are connected.



## Step 4: Network generation

All 3 files above will be used to generate the network file ["dayuan.cross.net.xml"](../docs/tutorial/traci_tls_dyt/data/dayuan.cross.net.xml) using `netconvert` command. 

Before that, let set up all parameters into 1 file ["dayuan.cross.netccfg"](../docs/tutorial/traci_tls_dyt/data/dayuan.cross.netccfg) since there are too much parameters. 

In this parameter file ["dayuan.cross.netccfg"](../docs/tutorial/traci_tls_dyt/data/dayuan.cross.netccfg),  we will set ["dayuan.cross.nod.xml"](../docs/tutorial/traci_tls_dyt/data/dayuan.cross.nod.xml),  ["dayuan.cross.edg.xml"](../docs/tutorial/traci_tls_dyt/data/dayuan.cross.edg.xml), ["dayuan.cross.con.xml"](../docs/tutorial/traci_tls_dyt/data/dayuan.cross.con.xml) all 3 above files as input files. And then set a out put file, which is our network file ["dayuan.cross.net.xml"](../docs/tutorial/traci_tls_dyt/data/dayuan.cross.net.xml).

As shown in SUMO project files structure:
<img src="./imgs/structure.gif"/>

BTW, If u-turn movements are not allowed, the command `<no-turnarounds value="true"/>` should be added to the configuration file. As stated previously, the prohibition of u-turn movements can only be conducted globally.

Run `netconvert -c dayuan.cross.netccfg` to generate file ["dayuan.cross.net.xml"](../docs/tutorial/quickstart_dyt/data/dayuan.cross.net.xml).

## Step 4: Traffic demand

Then I set up traffic flow information into ["dayuan.rou.xml"](../docs/tutorial/traci_tls_dyt/data/dayuan.rou.xml).

**Firstly** I define 4 types of cars. BTW the sigma parameter means all drivers are 50% perfect in driving.

Vehicle type related attributes include:

- (a) id: ID of the vehicle type, defined by users with numbers, word strings or both;
- (b) accel: maximum acceleration of the respective vehicle type (in m/s2);
- (c) decal: maximum deceleration of the respective vehicle type (in m/s2);
- (d) sigma: drivers’ imperfection in driving (between 0 and 1);
- (e) length: vehicle length (in meters);
- (f) maxSpeed: maximum vehicular velocity (in m/s);
- (g) color: color of the vehicle type. It is defined with 3 numbers (between 0 and 1) for red, green and blue respectively. Values are separated by comma and in quotes with no space between the values. For example, 1,0,0 represents the red color, 0,1,0 represents green color and 0,0,1 represents blue color.
- The sequence of the attributes can be changed. The attribute sigma is assigned as 0.5 for all vehicle types.

**Secondly** 12 routes are assigned to let each vehicle to select from.

Following the vehicle type information traffic route data need to be defined as well. The input attributes include:

- (a) id: ID of a certain route and defined by users with numbers, word strings or both.
- (b) edges: The sequence of the names of the links, composing the defined route.


**Thirdly** it's the traffic flow (traffic demand) design.

Traffic demand data are defined with four attributes:

- (a) depart: departure time of a certain vehicle.
- (b) id: ID of a certain vehicle and defined by users with numbers, word strings or both.
- (c) route: the route used by the defined vehicle;
- (d) type: ID of the defined vehicle type.

## Step 5: Run

All having all above, we can run the simulation using this command `sumo-gui -c dayuan.sumocfg`. 
<img src="./imgs/2nd/4.gif" />

## Result

Few screenshots of runing the simulation:
<img src="./imgs/2nd/r1.png"/>
<img src="./imgs/2nd/r2.png">
<img src="./imgs/2nd/r3.png">

FYI, in ["dayuan.settings.xml"](../docs/tutorial/traci_tls_dyt/data/dayuan.settings.xml) I set the run time from 54000 to 54100. You can change it as you want.

```
    <time>
        <begin value="54000"/>
        <end value="54100"/>
    </time>
```

----
Reference:

[1] https://sumo.dlr.de/docs/Tutorials/TraCI4Traffic_Lights.html#TraCI

