#!/usr/bin/env python
# Eclipse SUMO, Simulation of Urban MObility; see https://eclipse.org/sumo
# Copyright (C) 2009-2017 German Aerospace Center (DLR) and others.
# This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v2.0
# which accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v20.html

# @file    route.py
# @author  Michael Behrisch
# @date    2013-10-23
# @version $Id$

from __future__ import print_function
import os
import sys
SUMO_HOME = os.environ.get('SUMO_HOME',
                           os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
sys.path.append(os.path.join(SUMO_HOME, 'tools'))
from sumolib.miscutils import euclidean
from sumolib.geomhelper import polygonOffsetWithMinimumDistanceToPoint


def _getMinPath(paths):
    minDist = 1e400
    minPath = None
    for path, (dist, _) in paths.items():
        if dist < minDist:
            minPath = path
            minDist = dist
    return minPath


def mapTrace(trace, net, delta, verbose=False):
    """
    matching a list of 2D positions to consecutive edges in a network
    """
    result = ()
    paths = {}
    if verbose:
        print("mapping trace with %s points" % len(trace))
    for pos in trace:
        newPaths = {}
        candidates = net.getNeighboringEdges(pos[0], pos[1], delta)
        if len(candidates) == 0 and verbose:
            print("Found no candidate edges for %s" % pos)
        for edge, d in candidates:
            base = polygonOffsetWithMinimumDistanceToPoint(pos, edge.getShape())
            if paths:
                advance = euclidean(lastPos, pos)
                minDist = 1e400
                minPath = None
                for path, (dist, lastBase) in paths.items():
                    if dist < minDist:
                        if edge == path[-1]:
                            baseDiff = lastBase + advance - base
                        elif edge in path[-1].getOutgoing():
                            baseDiff = lastBase + advance - path[-1].getLength() - base
                        else:
                            airLineDist = euclidean(
                                path[-1].getToNode().getCoord(),
                                edge.getFromNode().getCoord())
                            baseDiff = lastBase + advance - path[-1].getLength() - base - airLineDist
                        if dist + baseDiff * baseDiff < minDist:
                            minDist = dist + baseDiff * baseDiff
                            minPath = path if edge == path[-1] else path + (edge,)
                if minPath:
                    newPaths[minPath] = (minDist, base)
            else:
                newPaths[(edge,)] = (d * d, base)
        if not newPaths:
            if paths:
                result += _getMinPath(paths)
        paths = newPaths
        lastPos = pos
    if paths:
        return result + _getMinPath(paths)
    return result
