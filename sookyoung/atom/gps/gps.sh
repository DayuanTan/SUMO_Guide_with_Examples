
python /home/aish/sumo-0.32.0/tools/randomTrips.py -n net5lane.net.xml  -r gps.rou.xml  --period 1
duarouter --net=net5lane.net.xml -r gps.rou.xml  --output-file=dua.rou.xml  --xml-validation never


python gps.py 
 

