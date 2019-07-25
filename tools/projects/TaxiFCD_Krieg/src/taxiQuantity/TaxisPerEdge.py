#!/usr/bin/env python
# -*- coding: Latin-1 -*-
# Eclipse SUMO, Simulation of Urban MObility; see https://eclipse.org/sumo
# Copyright (C) 2008-2017 German Aerospace Center (DLR) and others.
# This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v2.0
# which accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v20.html

# @file    TaxisPerEdge.py
# @author  Sascha Krieg
# @author  Daniel Krajzewicz
# @author  Michael Behrisch
# @date    2008-04-08
# @version $Id$

"""
Counts for every edge in the given FCD-file the number of Taxis which used this edge.
After that this information can be visualized with an script called mpl_dump_onNet from Daniel.

"""
from __future__ import absolute_import
from __future__ import print_function

import util.Path as path

# global vars
edgeList = {}


def main():
    print("start program")
    countTaxisForEachEdge()
    writeOutput()
    print("end")


def countTaxisForEachEdge():
    """counts the frequency of each edge"""
    inputFile = open(path.vls, 'r')
    for line in inputFile:
        words = line.split("\t")
        edgeList.setdefault(words[1], set())
        edgeList[words[1]].add(words[4])

    for k in edgeList:
        print(k)
        print(len(edgeList[k]))
    print(len(edgeList))


def writeOutput():
    """Writes an XML-File with the extracted results"""
    outputFile = open(path.taxisPerEdge, 'w')
    outputFile.write("<netstats>\n")
    outputFile.write("\t<interval begin=\"0\" end=\"899\" id=\"dump_900\">\n")
    for k in edgeList:
        outputFile.write(
            "\t\t<edge id=\"%s\" no=\"%s\" color=\"1.0\"/>\n" % (k, len(edgeList[k])))
    outputFile.write("\t</interval>\n")
    outputFile.write("</netstats>")


# start the program
main()
