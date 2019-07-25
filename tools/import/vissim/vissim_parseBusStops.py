#!/usr/bin/env python
# Eclipse SUMO, Simulation of Urban MObility; see https://eclipse.org/sumo
# Copyright (C) 2009-2017 German Aerospace Center (DLR) and others.
# This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v2.0
# which accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v20.html

# @file    vissim_parseBusStops.py
# @author  Daniel Krajzewicz
# @author  Michael Behrisch
# @date    2009-05-27
# @version $Id$

"""

Parses bus stops and bus routes given in the Vissim file (first parameter).

The read bus lines are saved as <OUTPUT_PREFIX>_busses.rou.xml
The read routes are saved as <OUTPUT_PREFIX>_stops.add.xml

(Starting?) edges of the route may be renamed by setting them within "edgemap"
 variable (see below).
"""
from __future__ import absolute_import
from __future__ import print_function

edgemap = {}
edgemap["203"] = "203[0]"
edgemap["78"] = "78[0]"
edgemap["77"] = "77[0]"
edgemap["203"] = "203[0]"


import sys
from random import *


def getName(vals, beg):
    name = vals[beg]
    while name.count('"') != 2:
        beg = beg + 1
        name = name + " " + vals[beg]
    return name.replace('"', '')


def parseBusStop(bs):
    vals = bs.split()
    id = int(vals[1])
    i = vals.index("NAME")
    name = getName(vals, i + 1)
    i = vals.index("STRECKE", i)
    strecke = vals[i + 1]
    i = vals.index("SPUR", i)
    spur = int(vals[i + 1]) - 1
    i = vals.index("BEI", i)
    von = float(vals[i + 1])
    i = vals.index("LAENGE", i)
    bis = von + float(vals[i + 1])
    return (id, name, strecke, spur, von, bis)


def parseBusRoute(br, stops):
    vals = br.split()
    id = vals[1]
    i = vals.index("NAME")
    name = getName(vals, i + 1)
    i = vals.index("EINFAHRT", i)
    startKante = vals[i + 2]
    i = vals.index("ZIEL", i)
    ziel = vals[i + 2]
    zeiten = []
    endI = vals.index("HALTESTELLE", i)
    i = vals.index("STARTZEITEN", i)
    i = i + 1
    while i > 0 and i < endI:
        zeiten.append(int(float(vals[i])))
        i = i + 5
    stops = []
    while i > 0 and i < len(vals):
        try:
            i = vals.index("HALTESTELLE", i)
            i = i + 1
            stops.insert(0, int(vals[i]))
        except:
            i = len(vals) + 1
    return (id, name, startKante, ziel, zeiten, stops)


def sorter(idx):
    def t(i, j):
        if i[idx] < j[idx]:
            return -1
        elif i[idx] > j[idx]:
            return 1
        else:
            return 0


if len(sys.argv) < 3:
    print("Usage: " + sys.argv[0] + " <VISSIM_NETWORK> <OUTPUT_PREFIX>")
    sys.exit()

print("Parsing Vissim input...")
fd = open(sys.argv[1])
haveStop = False
haveRoute = False
currentItem = ""
stopsL = []
routesL = []
for line in fd:
    # process bus stops ("HALTESTELLE")
    if line.find("HALTESTELLE") == 0:
        if haveStop:
            stopsL.append(" ".join(currentItem.split()))
        haveStop = True
        currentItem = ""
    elif line[0] != ' ':
        if haveStop:
            stopsL.append(" ".join(currentItem.split()))
        haveStop = False
    if haveStop:
        currentItem = currentItem + line
    # process bus routes ("LINIE")
    if line.find(" LINIE") == 0:
        if haveRoute:
            routesL.append(" ".join(currentItem.split()))
        haveRoute = True
        currentItem = ""
    elif len(line) > 2 and line[0] != ' ' and line[1] != ' ':
        if haveRoute:
            routesL.append(" ".join(currentItem.split()))
        haveRoute = False
    if haveRoute:
        currentItem = currentItem + line

# build stops map
sm = {}
for bs in stopsL:
    (id, name, strecke, spur, von, bis) = parseBusStop(bs)
    sm[id] = (id, name, strecke, spur, von, bis)


# process bus routes
#  build departure times
emissions = []
for br in routesL:
    (pid, name, startKante, ziel, zeiten, stops) = parseBusRoute(br, sm)
    edges = []
    edges.append(startKante)
    for s in stops:
        if sm[s][2] not in edges:
            edges.append(sm[s][2])
    if ziel not in edges:
        edges.append(ziel)
    for i in range(0, len(edges)):
        if edges[i] in edgemap:
            edges[i] = edgemap[edges[i]]
    for t in zeiten:
        id = str(pid) + "_" + str(t)
        emissions.append((int(t), id, edges, stops))

# sort emissions
print("Sorting routes...")
emissions.sort(sorter(0))
# write routes
print("Writing bus routes...")
fdo = open(sys.argv[2] + "_busses.rou.xml", "w")
fdo.write("<routes>\n")
for emission in emissions:
    if len(emission[2]) < 2:
        continue
    fdo.write('    <vehicle id="' + emission[1] + '" depart="' + str(emission[
              0]) + '" type="bus" color="0,1,0"><route>' + " ".join(emission[2]) + '</route>\n')
    for s in emission[3]:
        fdo.write(
            '        <stop bus_stop="' + str(s) + '_0" duration="20"/>\n')
    fdo.write('    </vehicle>\n')
fdo.write("</routes>\n")

# process bus stops
print("Writing bus stops...")
fdo = open(sys.argv[2] + "_stops.add.xml", "w")
fdo.write("<add>\n")
for bs in stopsL:
    (id, name, strecke, spur, von, bis) = parseBusStop(bs)
    fdo.write('    <busStop id="' + str(id) + '" lane="' + strecke + "_" +
              str(spur) + '" from="' + str(von) + '" to="' + str(bis) + '" lines="--"/>\n')
fdo.write("</add>\n")
fdo.close()
