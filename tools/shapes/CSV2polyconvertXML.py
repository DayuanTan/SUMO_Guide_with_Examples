#!/usr/bin/env python
# Eclipse SUMO, Simulation of Urban MObility; see https://eclipse.org/sumo
# Copyright (C) 2008-2017 German Aerospace Center (DLR) and others.
# This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v2.0
# which accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v20.html

# @file    CSV2polyconvertXML.py
# @author  Daniel Krajzewicz
# @author  Michael Behrisch
# @date    2008-07-17
# @version $Id$

"""
Converts a given CSV-file that contains a list of pois to
 an XML-file that may be read by POLYCONVERT.
"""
from __future__ import absolute_import
from __future__ import print_function

import sys

if len(sys.argv) < 4:
    print("Error: Missing argument(s)")
    print(
        "Call: CSV2polyconvertXML.py <CSV_FILE> <OUTPUT_FILE> <VALUENAME>[,<VALUENAME>]*")
    print(" The values within the csv-file are supposed to be divided by ';'.")
    print(
        " <VALUENAME>s give the attribute names in order of their appearence within the csv-file .")
    exit()


names = sys.argv[3].split(',')
inpf = open(sys.argv[1])
outf = open(sys.argv[2], "w")
outf.write("<pois>\n")
for line in inpf:
    if len(line) == 0 or line[0] == '#':
        continue
    vals = line.strip().split(';')
    outf.write("    <poi")
    for i, n in enumerate(names):
        outf.write(' ' + n + '="' + vals[i] + '"')
    outf.write("/>\n")
outf.write("</pois>\n")
inpf.close()
outf.close()
