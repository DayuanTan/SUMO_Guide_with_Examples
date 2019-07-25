#!/usr/bin/env python
# Eclipse SUMO, Simulation of Urban MObility; see https://eclipse.org/sumo
# Copyright (C) 2011-2017 German Aerospace Center (DLR) and others.
# This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v2.0
# which accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v20.html

# @file    rebuildSchemata.py
# @author  Michael Behrisch
# @date    2011-07-11
# @version $Id$

from __future__ import absolute_import
from __future__ import print_function
import os
import subprocess
homeDir = os.environ.get("SUMO_HOME", os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
for exe in "activitygen dfrouter duarouter marouter jtrrouter netconvert netgenerate od2trips polyconvert sumo".split():
    exePath = os.path.join(homeDir, "bin", exe)
    if os.path.exists(exePath) or os.path.exists(exePath + ".exe"):
        subprocess.call(
            [exePath, "--save-schema", os.path.join(homeDir, "data", "xsd", exe + "Configuration.xsd")])
    else:
        print("Warning! %s not found." % exe)
