# Generate urban net file using OpenStreetMap

## 1. Download OSM file from OSM website.
I followed this page. Go to the [OSM website](https://www.openstreetmap.org/export#map=15/38.8957/-77.0335), click "export". Select "Overpass API". Download the osm file of the area you selected.

It's a 35M file. I rename it with ".osm" ending. 

`-rw-r--r--@ 1 dyt  staff    35M Oct 11 15:34 map`

`-rw-r--r--@ 1 dyt  staff    35M Oct 11 15:34 map.osm`

## 2. Convert osm to net file

There are mulitple pages talking about this:
- https://sumo.dlr.de/docs/OpenStreetMap_file.html
- https://sumo.dlr.de/docs/Networks/Import/OpenStreetMap.html#junctions
- https://sumo.dlr.de/docs/Tutorials/Import_from_OpenStreetMap.html

Finally I choose to use `netconvert` command:
```python
netconvert --type-files ../../data/typemap/osmNetconvert.typ.xml,../../data/typemap/osmNetconvertUrbanDe.typ.xml \
     --osm-files map.osm --output-file dcDowntown.net.xml \
     --geometry.remove --roundabouts.guess --ramps.guess \
     --junctions.join --tls.guess-signals --tls.discard-simple --tls.join 
```

`--> 29M Oct 11 15:46 dcDowntown.net.xml`

Rationale:
- There are multiple degrees of freedom when importing data from OSM. SUMO provides recommended **typemaps in the folder <SUMO_HOME>/data/typemap/**. They are explained below.
- ***osmNetconvert.typ.xml***: default settings. appropriate for rural and motorway scenarios. This is used in the absence of user-specified types. All other typemaps are intended as patches to this typemap
- ***osmNetconvertUrbanDe.typ.xml***: Changes default speeds to reflect typical urban speed limits (50km/h)
- **--geometry.remove**: Simplifies the network (saving space) without changing topology
- **--roundabouts.guess**: This sets the appropriate right-of-way rules at roundabouts. (Explicit right-of-way rules are not imported from OSM). If this option is not used and roundabouts are not defined manually, then traffic jams will likely occur at roundabouts
- **--ramps.guess**. Acceleration/Deceleration lanes are often not included in OSM data. This option identifies likely roads that have these additional lanes and causes them to be added
- **--junctions.join**. See #Junctions
- **--tls.guess-signals, --tls.discard-simple, --tls.join**. See #Traffic_Lights

It tells "Success." with lots of warnings when finish.



## 3. Importing additional Polygons (Buildings, Water, etc.)
OSM-data not only contains the road network but also a wide range of additional polygons such as buildings and rivers. These polygons can be imported using POLYCONVERT and then added to a sumo-gui-configuration.


```
polyconvert --net-file dcDowntown.net.xml --osm-files map.osm --type-file ../../data/typemap/osmPolyconvert.typ.xml -o dcDowntown.poly.xml
```
`--> 4.2M Oct 11 15:47 dcDowntown.poly.xml`

It tells "Success." when finish.

The created polygon file "dcDowntown.poly.xml" can then be added to a sumo-gui configuration "*.sumocfg" file:

```xml
 <configuration>
     <input>
         <net-file value="dcDowntown.net.xml"/>
         <additional-files value="dcDowntown.poly.xml"/>
     </input>
 </configuration>
 ```

 ## 4. trips & routes

 
 `/usr/local/opt/sumo/share/sumo/tools/randomTrips.py -n dcDowntown.net.xml -o dcDowntown.trips.xml  --route-file dcDowntown.rou.xml -p 0.2 --begin 0 --end 1000 --fringe-factor 0`

- ../../../**tools/randomTrips.py**: Find the correct path of randomTrips.py file.
- **-n \*.net.xml**: As input file. Usually it's a network file.
- **-o \*.trips.xml**: As output file. randomTrips.py generates a trip file. Not route file by default.
- **-r / --route-file \*.rou.xml**: Add "--route-file" attribute it will call DUAROUTER automatically backend and generate route file for us.
- **--fringe-factor 0**: The option --fringe-factor increases the probability that trips will start/end at the fringe of the network. If the value 10 is given, edges that have no successor or no predecessor will be 10 times more likely to be chosen as start- or endpoint of a trip. This is useful when modelling through-traffic which starts and ends at the outside of the simulated area.
- **-p 1**: The arrival rate is controlled by option --period/-p (default 1). By default this generates vehicles with a constant period and arrival rate of (1/period) per second. By using values below 1, multiple arrivals per second can be achieved.

 ```shell
$ /usr/local/opt/sumo/share/sumo/tools/randomTrips.py -n dcDowntown.net.xml -o dcDowntown.trips.xml  --route-file dcDowntown.rou.xml -p 0.2 --begin 0 --end 1000 --fringe-factor 0
calling  /usr/local/opt/sumo/share/sumo/bin/duarouter -n dcDowntown.net.xml -r dcDowntown.trips.xml --ignore-errors --begin 0.0 --end 1000.0 --no-step-log --no-warnings -o dcDowntown.rou.xml
Success.
 ```

`--> -rw-r--r--  1 dyt  staff   3.1M Oct 11 16:04 dcDowntown.rou.alt.xml`

`--> -rw-r--r--  1 dyt  staff   2.6M Oct 11 16:04 dcDowntown.rou.xml`

`--> -rw-r--r--  1 dyt  staff   355K Oct 11 16:04 dcDowntown.trips.xml`


Tried `sumo-gui -c dayuan.sumo.cfg` it works well.


