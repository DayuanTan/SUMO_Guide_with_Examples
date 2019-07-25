#!/usr/bin/env python
# Eclipse SUMO, Simulation of Urban MObility; see https://eclipse.org/sumo
# Copyright (C) 2010-2017 German Aerospace Center (DLR) and others.
# This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v2.0
# which accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v20.html

# @file    addSchema.py
# @author  Daniel Krajzewicz
# @author  Michael Behrisch
# @date    2010
# @version $Id$

from __future__ import absolute_import
from __future__ import print_function

import os
import shutil
import glob

schema = 'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'

proc = {
    "*.rou.xml": '<routes %s xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/routes_file.xsd"' % schema,
    "*.edg.xml": '<edges %s xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/edges_file.xsd"' % schema,
    "*.nod.xml": '<nodes %s xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/nodes_file.xsd"' % schema,
    "*.typ.xml": '<types %s xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/types_file.xsd"' % schema,
    "*.con.xml": '<connections %s xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/connections_file.xsd"' % schema
}

srcRoot = os.path.join(os.path.dirname(__file__), "..", "..")

for root, dirs, files in os.walk(srcRoot):
    for pattern, repTo in proc.iteritems():
        for name in glob.glob(os.path.join(root, pattern)):
            repFrom = repTo[:repTo.find(' ')]
            print("Patching '%s'" % name)
            shutil.copy(name, "totest.xml")
            fdi = open("totest.xml")
            fdo = open("totest.patch", "w")
            for line in fdi:
                if repFrom in line and schema not in line:
                    line = line.replace(repFrom, repTo)
                fdo.write(line)
            fdo.close()
            fdi.close()
            shutil.copy("totest.patch", name)
        for ignoreDir in ['.svn', 'foreign']:
            if ignoreDir in dirs:
                dirs.remove(ignoreDir)
