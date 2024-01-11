# SUMO
 
This includes [**SUMO offical packages**](https://github.com/eclipse/sumo). 


Files tree:

|Dir path|Dir or File|Notes|
|:-|:-:|:-|
|- data|d|Official dir.|
|- docs|d|Official dir.| 
|- - tutorial|d|Official examples.|
|- tools|d|Official dir.|
|- dayuan|d|My sumo projects, examples.|
|- - [aSimpleSumo.md](dayuan/aSimpleSumo.md)|f|My example for a simple road net.|
|- - [2ndSimpleSumo.md](dayuan/2ndSimpleSumo.md)|f|My 2nd SUMO example. A bit more complex then above one.|
|- - [3rdSumoTraCI.md](dayuan/3rdSumoTraCI.md)|f|Third exmaple about how to use TraCI.|
|- - [generateNetfileOSM.md](dayuan/generateNetfileOSM.md), [generate2_DCdowntown.md](dayuan/generate2_DCdowntown.md)|f|About generate net file using OSM.|
|- - [vTypeDist](dayuan/vTypeDist)|d|How to set up different vehicle types in SUMO.|
|- - [TL_reschedule](dayuan/TL_reschedule)|d|How to change/reschedule traffic lights cycles.|
|- - [platoon](dayuan/platoon)|d|Setup platoon and get platoon info.|
|- - imgs|d|Some screenshots or recording vedios for my projects or examples.|
||


------
# File structure for a SUMO project 

<img src="./dayuan/imgs/structure.gif"/>

- (*) Link geometry data can also be defined in the link file quickstart.edg.xml.
- (**) It is an optional file. If this file is not given, lane connections and traffic movements will be generated by defaults.

## For executing:

<img src="./dayuan/imgs/2nd/4.gif">

------

# [My simple SUMO example](./dayuan/aSimpleSumo.md)

I set up a simple SUMO, it's friednly to beginners. You can find it [here](./dayuan/aSimpleSumo.md).

Few screenshots about it:

<img src="./dayuan/imgs/hello_dyt/1.png" width=250/> <img src="./dayuan/imgs/hello_dyt/2.png" width=250/> <img src="./dayuan/imgs/hello_dyt/3.png" width=250/>

------
# [Second SUMO example: a bit more complex](./dayuan/2ndSimpleSumo.md)

**Difference** **& Improvement**:
- The road condition is more complex, two direction three lanes are added.
- Different edge(road segment) types are used.
- Different lane is assigned to specific lane.
- Use `netconvert -c dayuan.netccfg` to generate "net.xml" file.

Few screenshots about it:

<img src="./dayuan/imgs/2nd/r1.png" width=250/> <img src="./dayuan/imgs/2nd/r2.png" width=250/> <img src="./dayuan/imgs/2nd/r3.png" width=250/>

# [Third SUMO example: use TraCI](./dayuan/3rdSumoTraCI.md)

This is an example using TraCI to control and change traffic lights.

# [Generate urban net file using OpenStreetMap](./dayuan/generateNetfileOSM.md)

# [Generate smaller net file using OpenStreetMap (DC downtown)](./dayuan/generate2_DCdowntown.md)

# [Generate NYC road net file using OpenStreetMap (updated 3/12/2022)](./dayuan/generate3_nyc.md)


#
# SUMO Example for Traffic Lights - Actuated TL (ATL)

[ATL](https://sumo.dlr.de/docs/Simulation/Traffic_Lights.html#actuated_traffic_lights)

[Code file: <SUMO_HOME>/tests/sumo/basic/tls/actuated/dualring_simple/](https://github.com/eclipse/sumo/blob/master/tests/sumo/basic/tls/actuated/dualring_simple)

To run it:
```
.../dualring_simple$ sumo-gui -n net.net.xml -r input_routes.rou.xml -a "input_additional.add.xml"
```

The original TL logic (programID="0") defined in net.net.xml don't work since an additional TL logic (programID="1") is defined in add.xml which actually works. We can observe the minDur and maxDur works.

The offcial wiki mentions the "next" option and it logic to select next phase. But I didn't see how it works in this example. So far only minDur/maxDur have been proved. 

ref: [1 Simulation/Traffic Lights.](https://sumo.dlr.de/docs/Simulation/Traffic_Lights.html#automatically_generated_tls-programs)

[2 Actuated Traffic Lights.](https://sumo.dlr.de/docs/Simulation/Traffic_Lights.html#actuated_traffic_lights)

------
# [Building a randomTrips scenario with different vehicle types.](./dayuan//vTypeDist/vTypeDist.md)

This is a short tutorial about how to implement different vehicle types in one scenario composed by me. 

------
# [How to change traffic lights schedule while sumo running?](./dayuan/TL_reschedule/TL_reschedule.md)

This is a tutorial about how to change the current/default traffic lights schedule while sumo running, which will be useful for those traffic lights dynamic re-schedule project.


------
# [How to setup platoon and get platoon information?](./dayuan/platoon/platoon.md)

There is no official good way to get platoon information like which vehicles are forming platoon. 

I found a way that to check vehicle type. Those vehicles which are in platoons their vehicle type will be changed. 

After SUMO 1.19.0 https://github.com/DayuanTan/simpla_official_example_run


