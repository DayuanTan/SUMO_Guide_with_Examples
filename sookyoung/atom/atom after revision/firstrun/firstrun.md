# 20190725 First try to run
# The commands I used:


```
dyt@ubuntu:/usr/share/sumo/sookyoung/atom/atom after revision$ python /usr/share/sumo/tools/randomTrips.py -n b4atom.net.xml -r atom.rou.xml --period 1
```
```
calling  duarouter -n b4atom.net.xml -r trips.trips.xml -o atom.rou.xml --ignore-errors --begin 0 --end 3600 --no-step-log --no-warnings
Success.
```




## ------
```
dyt@ubuntu:/usr/share/sumo/sookyoung/atom/atom after revision$ duarouter --net=b4.net.xml -r atom.rou.xml --output-file=dua.rou.xml --xml-validation never
```
```
Error: The network file 'b4.net.xml' is not accessible.
Quitting (on error).
dyt@ubuntu:
```

## ------
```
dyt@ubuntu:/usr/share/sumo/sookyoung/atom/atom after revision$ duarouter --net=b4atom.net.xml -r atom.rou.xml --output-file=dua.rou.xml --xml-validation never
```
```
Success.up to time step: 3600.00
```

## ------
```
dyt@ubuntu:/usr/share/sumo/sookyoung/atom/atom after revision$ python atom.py 
```
```
atom.py:520: SyntaxWarning: name 'CL_t_ph' is assigned to before global declaration
  global PH_CYC_t , CL_t_ph 			#list of phases for the cycle at t
atom.py:522: SyntaxWarning: name 'phase' is assigned to before global declaration
  global phase
 Retrying in 1 seconds
Loading configuration... done.
***Starting server on port 38347 ***
Loading net-file from 'b4atom.net.xml'... done (65ms).
Loading additional-files from 'atom.add.xml'... done (3ms).
Loading done.
Simulation started with time: 0.00
/usr/share/sumo/sookyoung/atom/atom after revision/traci/domain.py:113: UserWarning: The domain trafficlights is deprecated, use trafficlight instead.
  self._name, self._deprecatedFor))  # , DeprecationWarning)
Simulation ended at time: 3601.00~146222.22UPS, TraCI: 33ms, vehicles TOT 2367
Reason: TraCI requested termination.
Performance: 
 Duration: 127975ms
 Real time factor: 28.1383
 UPS: 19445.133815
Vehicles: 
 Inserted: 2367 (Loaded: 2964)
 Running: 1316
 Waiting: 597
Teleports: 1309 (Jam: 825, Yield: 393, Wrong Lane: 91)
Emergency Stops: 37
Statistics (avg):
 RouteLength: 547.35
 Duration: 575.23
 WaitingTime: 479.69
 TimeLoss: 508.20
 DepartDelay: 26.83

dyt@ubuntu:
```

