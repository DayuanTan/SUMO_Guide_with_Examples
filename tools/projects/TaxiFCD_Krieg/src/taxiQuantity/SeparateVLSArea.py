#!/usr/bin/env python
# -*- coding: Latin-1 -*-
# Eclipse SUMO, Simulation of Urban MObility; see https://eclipse.org/sumo
# Copyright (C) 2008-2017 German Aerospace Center (DLR) and others.
# This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v2.0
# which accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v20.html

# @file    SeparateVLSArea.py
# @author  Sascha Krieg
# @author  Daniel Krajzewicz
# @author  Michael Behrisch
# @date    2008-04-07
# @version $Id$

from __future__ import absolute_import
from __future__ import print_function

import util.Path as path
import util.Reader as reader


def main():
    print("start")
    generateVLS_FCD_File()
    print("end")


def generateVLS_FCD_File():
    """Creates a new FCD-file which contains only the rows which edges belongs to the VLS-Area"""
    outputVLSFile = open(path.vls, 'w')
    inputFile = open(path.fcd, 'r')

    vlsEdgeList = reader.readVLS_Edges()

    for line in inputFile:
        words = line.split("\t")
        # check if edge belongs to the VLS-Area
        if words[1] in vlsEdgeList:
            outputVLSFile.write(line)
    inputFile.close()
    outputVLSFile.close()


# start the program
main()
