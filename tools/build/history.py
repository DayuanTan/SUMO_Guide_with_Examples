#!/usr/bin/env python
# Eclipse SUMO, Simulation of Urban MObility; see https://eclipse.org/sumo
# Copyright (C) 2011-2017 German Aerospace Center (DLR) and others.
# This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v2.0
# which accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v20.html

# @file    history.py
# @author  Michael Behrisch
# @date    2014-06-21
# @version $Id$

"""
This script builds all sumo versions in a certain revision range
and tries to eliminate duplicates afterwards.
"""
from __future__ import absolute_import

import subprocess
import optparse
import shutil
import os
import sys
import traceback

import version


optParser = optparse.OptionParser()
optParser.add_option("-b", "--begin", default="51bb151", help="first revision to build")
optParser.add_option("-e", "--end", default="HEAD", help="last revision to build")
options, args = optParser.parse_args()

LOCK = "../history.lock"
if os.path.exists(LOCK):
    sys.exit("History building is still locked!")
open(LOCK, 'w').close()
try:
    subprocess.call(["git", "checkout", "-q", "master"])
    subprocess.call(["git", "pull"])
    commits = {}
    for line in subprocess.check_output(["git", "log", "%s..%s" % (options.begin, options.end)]).splitlines():
        if line.startswith("commit "):
            h = line.split()[1]
            commits[h] = version.gitDescribe(h)
    for h, desc in sorted(commits.items(), key=lambda x: x[1]):
        if not os.path.exists('../bin%s' % desc):
            ret = subprocess.call(["git", "checkout", "-q", h])
            if ret != 0:
                continue
            subprocess.call('make clean; make -j 16', shell=True)
            shutil.copytree('bin', '../bin%s' % desc,
                            ignore=shutil.ignore_patterns('Makefile*', '*.bat', '*.jar'))
            subprocess.call('strip -R .note.gnu.build-id ../bin%s/*' % desc, shell=True)
            subprocess.call("sed -i 's/%s/%s/' ../bin%s/*" % (desc, len(desc) * "0", desc), shell=True)
    for line in subprocess.check_output('fdupes -1 -q ../binv*', shell=True).splitlines():
        dups = line.split()
        for d in dups[1:]:
            subprocess.call('ln -sf %s %s' % (dups[0], d), shell=True)
    subprocess.call(["git", "checkout", "-q", "master"])
except:
    traceback.print_exc()
os.remove(LOCK)
