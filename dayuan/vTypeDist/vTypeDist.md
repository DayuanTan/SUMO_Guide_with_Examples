
# Building a randomTrips scenario with different vehicle types. 

Sometimes we want to integrate multiple vehicle types into one scenarios to make it closer to read world traffic flow situation. There are two ways to implement it in SUMO.

# Solution 1:

1. Use randomTrips.py twice seperately to generate two route files. 
2. Put them both in \<input>\<route-files> attributes with "," between them in ***"dayuan.grid.sumocfg"*** file.

#### Solution Instruction:

1. myvTypeCar

```netfiles$../../../tools/randomTrips.py -n dayuan.grid.1.net.xml -o dayuan.grid.2.trips.car.xml -r dayuan.grid.2.rou.car.xml --period 0.2 --additional-file dayuan.grid.me.add.vtype.xml --fringe-factor 100 --vehicle-class passenger --prefix=car```

(--trip-attributes="type=\"myvTypeCar\"" doens't work. It says "Error: Another vehicle type (or distribution) with the id 'myvTypeCar' exists.")

```calling  /usr/local/opt/sumo/share/sumo/bin/duarouter -n dayuan.grid.1.net.xml -r dayuan.grid.2.trips.car.xml -o dayuan.grid.2.rou.car.xml --ignore-errors --begin 0 --end 3600 --no-step-log --no-warnings --additional-files dayuan.grid.me.add.vtype.xml```

```Success.```

2. myvTypeBus

 ```netfiles$../../../tools/randomTrips.py -n dayuan.grid.1.net.xml -o dayuan.grid.2.trips.bus.xml -r dayuan.grid.2.rou.bus.xml --period 1 --additional-file dayuan.grid.me.add.vtype.xml --fringe-factor 100 --vehicle-class bus --prefix=bus```

```calling  /usr/local/opt/sumo/share/sumo/bin/duarouter -n dayuan.grid.1.net.xml -r dayuan.grid.2.trips.bus.xml -o dayuan.grid.2.rou.bus.xml --ignore-errors --begin 0 --end 3600 --no-step-log --no-warnings --additional-files dayuan.grid.me.add.vtype.xml```

```Success.```


# Solution 2:

Put the types into a vTypeDistribution and put the distribution id into the type attribute. Files please [***dyt_grid_test_typeDist*** directory](../dyt_grid_test_typeDist). 

```dyt_grid_test_typeDist/netfiles$ ../../../tools/randomTrips.py -n dayuan.grid.1.net.xml -o dayuan.grid.2.trips.xml -r dayuan.grid.2.rou.xml --period 0.2 --additional-file dayuan.grid.me.add.vtype.xml --fringe-factor 100 --trip-attributes="type=\"typedist1\""```

```calling  /usr/local/opt/sumo/share/sumo/bin/duarouter -n dayuan.grid.1.net.xml -r dayuan.grid.2.trips.xml -o dayuan.grid.2.rou.xml --ignore-errors --begin 0 --end 3600 --no-step-log --no-warnings --additional-files dayuan.grid.me.add.vtype.xml```

```Success.```

Then it will generate vType distribution in route files. 
Like *"dayuan.grid.2.rou.alt.xml"*:


```
<routes xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/routes_file.xsd">
    <vType id="myvTypeBus" length="14.63" maxSpeed="30.00" probability="0.90" vClass="bus" guiShape="bus"/>
    <vehicle id="0" type="myvTypeBus" depart="0.00">
        <routeDistribution last="0">
            <route cost="136.49" probability="1.00000000" edges="bottom4E0 E0D0 E0D0.580.00 D0C0 D0C0.580.00 C0B0 C0B0.580.00 B0bottom1"/>
        </routeDistribution>
    </vehicle>
    <vehicle id="1" type="myvTypeBus" depart="0.20">
        <routeDistribution last="0">
            <route cost="191.72" probability="1.00000000" edges="bottom3D0 D0D1 D0D1.480.00 D1D2 D1D2.480.00 D2D3 D2D3.480.00 D3D4 D3D4.480.00 D4E4 D4E4.580.00 E4top4"/>
        </routeDistribution>
    </vehicle>
    <vType id="myvTypeCar" length="4.50" maxSpeed="35.00" probability="0.10" vClass="passenger" guiShape="passenger"/>
    <vehicle id="2" type="myvTypeCar" depart="0.40">
        <routeDistribution last="0">
            <route cost="283.46" probability="1.00000000" edges="right1F1 F1E1 F1E1.580.00 E1D1 E1D1.580.00 D1C1 D1C1.580.00 C1B1 C1B1.580.00 B1B2 B1B2.480.00 B2B3 B2B3.480.00 B3B4 B3B4.480.00 B4top1"/>
        </routeDistribution>
    </vehicle>
```

##### Note:
Then in .sumocfg we **can not** add "dayuan.grid.me.add.vtype.xml" anymore since randomTrips.py already write the vType into route file. 
