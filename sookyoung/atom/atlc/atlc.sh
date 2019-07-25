

python /home/aish/sumo-0.32.0/tools/randomTrips.py -n net5lane.net.xml  -r atlc.rou.xml  --period 0.5
duarouter --net=net5lane.net.xml -r atlc.rou.xml  --output-file=dua.rou.xml  --xml-validation never


python baseline1.py 
 

