

python /home/aish/sumo-0.32.0/tools/randomTrips.py -n b4atom.net.xml  -r atom.rou.xml  --period 3.0 
duarouter --net=b4.net.xml -r atom.rou.xml  --output-file=dua.rou.xml --route-choice-method logit  --xml-validation never 


python atom.py 

python baseline1.py

python tapioca.py
 

