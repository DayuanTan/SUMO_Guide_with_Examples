#!/usr/bin/env python
# Eclipse SUMO, Simulation of Urban MObility; see https://eclipse.org/sumo
# Copyright (C) 2008-2017 German Aerospace Center (DLR) and others.
# This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v2.0
# which accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v20.html

# @file    route2sel.py
# @author  Jakob Erdmann
# @date    2015-08-05
# @version $Id$

from __future__ import print_function
from __future__ import absolute_import
import sys
from optparse import OptionParser
from sumolib.output import parse, parse_fast


def parse_args():
    USAGE = "Usage: " + sys.argv[0] + " <routefile> [options]"
    optParser = OptionParser()
    optParser.add_option("-o", "--outfile", help="name of output file")
    options, args = optParser.parse_args()
    try:
        options.routefiles = args
    except:
        sys.exit(USAGE)
    if options.outfile is None:
        options.outfile = options.routefiles[0] + ".sel.txt"
    return options


def main():
    options = parse_args()
    edges = set()

    for routefile in options.routefiles:
        for route in parse_fast(routefile, 'route', ['edges']):
            edges.update(route.edges.split())
        for walk in parse_fast(routefile, 'walk', ['edges']):
            edges.update(walk.edges.split())

        # warn about potentially missing edges
        for trip in parse(routefile, ['trip', 'flow'], heterogeneous=True):
            edges.update([trip.attr_from, trip.to])
            if trip.via is not None:
                edges.update(trip.via.split())
            print(
                "Warning: Trip %s is not guaranteed to be connected within the extracted edges." % trip.id)
        for walk in parse_fast(routefile, 'walk', ['from', 'to']):
            edges.update([walk.attr_from, walk.to])
            print("Warning: Walk from %s to %s is not guaranteed to be connected within the extracted edges." % (
                walk.attr_from, walk.to))

    with open(options.outfile, 'w') as outf:
        for e in sorted(list(edges)):
            outf.write('edge:%s\n' % e)

if __name__ == "__main__":
    main()
