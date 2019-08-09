# 2nd Simple SUMO 

This is a bit more complex SUMO example based on the [first simple sumo](./aSimpleSumo.md).

**Difference** **& Improvement**:
- The road condition is more complex, two direction three lanes are added.
- Different edge(road segment) types are used.
- Different lane is assigned to specific lane.
- Use `netconvert -c dayuan.netccfg` to generate "net.xml" file.


I want to implement this road network:


<img src="./imgs/2ndSimpleSumoRoadNet.png" />


----
Reference:

[1] https://sumo.dlr.de/wiki/Tutorials/Quick_Start_old_style (better, used configuration files to set up.)

[2] https://sumo.dlr.de/wiki/Tutorials/quick_start (Use gui to set up but not easy to do.)