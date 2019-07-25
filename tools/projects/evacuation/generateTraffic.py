# -*- coding: cp1252 -*-
# Eclipse SUMO, Simulation of Urban MObility; see https://eclipse.org/sumo
# Copyright (C) 2009-2017 German Aerospace Center (DLR) and others.
# This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v2.0
# which accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v20.html

# @file    generateTraffic.py
# @author  Martin Taraz
# @author  Michael Behrisch
# @date    2015-09-09
# @version $Id$

from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import subprocess
from optparse import OptionParser
from xml.sax import parse

SUMO_HOME = os.environ.get("SUMO_HOME", os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
sys.path.append(os.path.join(SUMO_HOME, "tools"))

import edgesInDistricts as EID
import sumolib  # noqa


def generate(netFile, mappedSiteFile, intersectionFile, tripFile):
    # EdgesInDistricts
    # evakuierungsbereich
    options = OptionParser()
    options.maxspeed = 1000.
    options.minspeed = 0.
    options.complete = False
    options.internal = False
    options.vclass = None
    options.assign_from = True
    options.verbose = False
    options.weighted = False
    options.shapeinfo = False
    options.output = "edgesInIntersections.taz.xml"
    net = sumolib.net.readNet(netFile)
    reader = EID.DistrictEdgeComputer(net)
    polyReader = sumolib.shapes.polygon.PolygonReader(True)
    parse(intersectionFile, polyReader)
    reader.computeWithin(polyReader.getPolygons(), options)
    reader.writeResults(options)

    # Evakuierungsziele
    options.output = "evacuationsiteEdges.taz.xml"
    reader = EID.DistrictEdgeComputer(net)
    polyReader = sumolib.shapes.polygon.PolygonReader(True)
    parse(mappedSiteFile, polyReader)
    reader.computeWithin(polyReader.getPolygons(), options)
    reader.writeResults(options)
    print("EdgesInDistricts - done")

    # O/D Matrix
    import xml.etree.cElementTree as ET
    Districts = ET.ElementTree(file=intersectionFile)
    root = Districts.getroot()
    EVA = ET.ElementTree(file='evacuationsiteEdges.taz.xml')
    EV = EVA.getroot()
    EV.remove(EV[0])
    with open('ODMatrix.fma', 'w') as odm:
        odm.write('$OR \n* From-Tome To-Time \n1.00 2.00\n* Factor \n1.00\n')
        for elem in root.findall("./poly"):
            for ESite in EV.findall("./*"):
                CarAmount = str(
                    int(float(elem.attrib["inhabitants"]) / float(3 * (len(EV.findall("./*")) - 1))))
                odm.write(
                    elem.attrib["id"] + '\t' + ESite.attrib["id"] + '\t' + CarAmount + '\n')
    print("OD Matrix - done")

    # OD2TRIPS
    od2t = sumolib.checkBinary('od2trips')
    od2tOptions = [od2t, '--no-step-log', '-d', odm.name, '-n',
                   'edgesInIntersections.taz.xml,evacuationsiteEdges.taz.xml', '-o', tripFile]
    subprocess.call(od2tOptions)
