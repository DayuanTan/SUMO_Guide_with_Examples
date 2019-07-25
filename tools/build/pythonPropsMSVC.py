#!/usr/bin/env python
# Eclipse SUMO, Simulation of Urban MObility; see https://eclipse.org/sumo
# Copyright (C) 2011-2017 German Aerospace Center (DLR) and others.
# This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v2.0
# which accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v20.html

# @file    pythonPropsMSVC.py
# @author  Michael Behrisch
# @author  Daniel Krajzewicz
# @author  Jakob Erdmann
# @date    2011
# @version $Id$

"""
This script rebuilds "../../build/msvc/python.props", the file which
gives information about the python includes and library.
"""
from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import re
import distutils.sysconfig
from os.path import dirname, join, exists


def generateDefaultProps(propsFile):
    print('generating %s ' % propsFile)
    with open(propsFile, "w") as props:
        props.write("""<?xml version="1.0" encoding="utf-8"?>
<Project DefaultTargets="Build" ToolsVersion="4.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">
  <PropertyGroup Label="UserMacros">
""")
        for platform in ("", "_64"):
            for lib in ("XERCES", "PROJ_GDAL", "FOX16", "OSG", "FFMPEG"):
                props.write("    <%s%s>$(%s%s)</%s%s>\n" %
                            (3 * (lib, platform)))
            props.write("    <%s%s_LIB_DIR></%s%s_LIB_DIR>\n" %
                        (2 * ("PYTHON", platform)))
            props.write("    <%s%s_INCLUDE_DIR></%s%s_INCLUDE_DIR>\n" %
                        (2 * ("PYTHON", platform)))
        props.write("""  </PropertyGroup>
</Project>
""")

propsFile = join(
    dirname(__file__), '..', '..', 'build', 'msvc10', 'config.props')
if not exists(propsFile):
    generateDefaultProps(propsFile)
if sys.maxsize > 2**32:
    py = "PYTHON_64"
else:
    py = "PYTHON"
libDir = join(sys.prefix, "libs")
if not exists(libDir):
    print("Warning, %s not found, keeping config unmodfied!" %
          libDir, file=sys.stderr)
    sys.exit(1)

propsBak = propsFile + ".bak"
if exists(propsBak):
    print("Warning, %s exists and will be overwritten!" %
          propsBak, file=sys.stderr)
    os.remove(propsBak)
os.rename(propsFile, propsBak)
modified = False
with open(propsFile, "w") as props:
    for line in open(propsBak):
        newLine = re.sub('<%s_LIB_DIR>(.*)</%s_LIB_DIR>' % (py, py),
                         '<%s_LIB_DIR>%s</%s_LIB_DIR>' % (py, libDir, py), line)
        include = distutils.sysconfig.get_config_var('INCLUDEPY')
        newLine = re.sub('<%s_INCLUDE_DIR>(.*)</%s_INCLUDE_DIR>' % (py, py),
                         '<%s_INCLUDE_DIR>%s</%s_INCLUDE_DIR>' % (py, include, py), newLine)
        if newLine != line:
            modified = True
            props.write(newLine)
        else:
            props.write(line)
if not modified:
    os.remove(propsFile)
    os.rename(propsBak, propsFile)
