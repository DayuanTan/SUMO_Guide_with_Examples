# A Simple SUMO 

I tried a simple SUMO after reading [SUMO official Documents](https://sumo.dlr.de/wiki/SUMO_User_Documentation#Introduction).

Firstly, I set up a road net like this:

There are 12 vertexes and 17 road segments. I only setup the direction from up-left to bottom-right. The directions are also indicated in screenshots.

Those vertexes, called nodes in SUMO, are set up in the configuration file "[dayuan.nod.xml](../docs/tutorial/hello_dyt/data/dayuan.nod.xml)".

Road segments are set up in the configuration file "[dayuan.edg.xml](../docs/tutorial/hello_dyt/data/dayuan.edg.xml)".

Then I used command `netconvert --node-files=dayuan.nod.xml --edge-files=dayuan.edg.xml --output-file=dayuan.net.xml` to create the road network file, which will be stored in "[dayuan.net.xml](../docs/tutorial/hello_dyt/data/dayuan.net.xml)".

Routes are set up in configuration file "[dayuan.rou.xml](../docs/tutorial/hello_dyt/data/dayuan.rou.xml)". I assigned 5 routes. 22 Vehicles will start at up-left node and head to bottom-down node. One vehicle starts per second. They use one of those 5 routes. 

"[dayuan.sumocfg](../docs/tutorial/hello_dyt/data/dayuan.sumocfg)" and "[dayuan.settings.xml](../docs/tutorial/hello_dyt/data/dayuan.settings.xml)" are also needed when you use `sumo-gui`.

Then just run command `sumo-gui -c hello.sumocfg`, you will see the SUMO GUI window. Click start then the simulation will begin.

Here are some screenshots of this simulation.
<img src="./imgs/hello_dyt/1.png"/>
<img src="./imgs/hello_dyt/2.png"/>
<img src="./imgs/hello_dyt/3.png"/>
It's worth to mention that in the third screenshot, two cars around node No. 3 are waiting the car coming from left. So SUMO is really intelligent. 



Also [a recording vedio](./imgs/hello_dyt/Recording.mov) is provided, but it can not play online. You may need to download and then to play it locally.

------
References:
[1] https://sumo.dlr.de/wiki/Tutorials/Hello_Sumo