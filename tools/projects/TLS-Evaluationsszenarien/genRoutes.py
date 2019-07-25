#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Eclipse SUMO, Simulation of Urban MObility; see https://eclipse.org/sumo
# Copyright (C) 2009-2017 German Aerospace Center (DLR) and others.
# This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v2.0
# which accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v20.html

# @file    genRoutes.py
# @author  Lena Kalleske
# @author  Daniel Krajzewicz
# @author  Michael Behrisch
# @date    2009-06-30
# @version $Id$

from __future__ import absolute_import
from __future__ import print_function

import random
import optparse
import sys


def genRoutes(N, dR, fR, dL, fL, dD, fD, dU, fU):

    routes = open("cross.rou.xml", "w")
    print('''\
<routes>
    <vType id="carRight" accel="2.6" decel="4.5" sigma="0.5" length="5" minGap="2.5" maxSpeed="16.67"/>
    <vType id="carLeft" accel="2.6" decel="4.5" sigma="0.5" length="5" minGap="2.5" maxSpeed="16.67"/>
    <vType id="carDown" accel="2.6" decel="4.5" sigma="0.5" length="5" minGap="2.5" maxSpeed="16.67"/>
    <vType id="carUp" accel="2.6" decel="4.5" sigma="0.5" length="5" minGap="2.5" maxSpeed="16.67"/>

    <route id="right" edges="51o 1i 2o 52i" />
    <route id="left" edges="52o 2i 1o 51i" />
    <route id="down" edges="54o 4i 3o 53i" />
    <route id="up" edges="53o 3i 4o 54i" />
''', file=routes)
    lastVeh = 0
    vehNr = 0

    nbVehR = 0
    nbVehL = 0
    nbVehD = 0
    nbVehU = 0

    if fR == 0:
        tR = N
        nextTR = N
    else:
        tR = (1.0 / fR) * 3600
        nextTR = 0

    if fL == 0:
        tL = N
        nextTL = N
    else:
        tL = (1.0 / fL) * 3600
        nextTL = 0

    if fD == 0:
        tD = N
        nextTD = N
    else:
        tD = (1.0 / fD) * 3600
        nextTD = 0

    if fU == 0:
        tU = N
        nextTU = N
    else:
        tU = (1.0 / fU) * 3600
        nextTU = 0

    pR = fR / 3600.0
    pL = fL / 3600.0
    pD = fD / 3600.0
    pU = fU / 3600.0

    vehNr = 0
    for T in range(N):
        if (dR == 'u' and nextTR <= T) or (dR == 'p' and random.uniform(0, 1) < pR):
            print('    <vehicle id="%i" type="carRight" route="right" depart="%i" />' % (
                vehNr, T), file=routes)
            vehNr += 1
            nbVehR += 1
            nextTR = nextTR + tR

        if (dL == 'u' and nextTL <= T) or (dL == 'p' and random.uniform(0, 1) < pL):
            print('    <vehicle id="%i" type="carLeft" route="left" depart="%i" />' % (
                vehNr, T), file=routes)
            vehNr += 1
            nbVehL += 1
            nextTL = nextTL + tL

        if (dD == 'u' and nextTD <= T) or (dD == 'p' and random.uniform(0, 1) < pD):
            print('    <vehicle id="%i" type="carDown" route="down" depart="%i" />' % (
                vehNr, T), file=routes)
            vehNr += 1
            nbVehD += 1
            nextTD = nextTD + tD

        if (dU == 'u' and nextTU <= T) or (dU == 'p' and random.uniform(0, 1) < pU):
            print('    <vehicle id="%i" type="carUp" route="up" depart="%i" />' % (
                vehNr, T), file=routes)
            vehNr += 1
            nbVehU += 1
            nextTU = nextTU + tU

    print("</routes>", file=routes)
    routes.close()


#    print "Right: " + str(nbVehR*3600.0/N) + " veh/h"
#    print "Left: " + str(nbVehL*3600.0/N) + " veh/h"
#    print "Down: " + str(nbVehD*3600.0/N) + " veh/h"
#    print "Up: " + str(nbVehU*3600.0/N) + " veh/h"
    # print "%i vehicles were generated" % (vehNr)

if __name__ == "__main__":

    parser = optparse.OptionParser()
    parser.add_option(
        "-d",
        "--distribution",
        dest="distr",
        default="('u','u','u','u')",
        help="Distribution (Uniform (u), Poisson (p))"
    )

    parser.add_option(
        "-f",
        "--flow",
        dest="flow",
        default="(360, 360, 360, 360)",
        help="Traffic flow (vehicles/hour)"
    )

    parser.add_option(
        "-N",
        "--SimulationTime",
        dest="N",
        default="1000",
        help="Simulation Time"
    )

    (options, args) = parser.parse_args()

    flows = eval(options.flow)
    if type(flows) == int:
        fR = flows
        fL = flows
        fD = flows
        fU = flows
    elif len(flows) == 4:
        (fR, fL, fD, fU) = flows
    elif len(flows) == 2:
        (fR, fD) = flows
        (fL, fU) = flows
    else:
        print("Flow - wrong format")
        sys.exit()

    distrs = eval(options.distr)
    if len(distrs) == 4:
        (dR, dL, dD, dU) = distrs
    elif len(distrs) == 1:
        dR = distrs
        dL = distrs
        dD = distrs
        dU = distrs
    elif len(distrs) == 2:
        (dR, dD) = distrs
        (dL, dU) = distrs
    else:
        print("Distribution - wrong format")
        sys.exit()

    N = int(options.N)

    genRoutes(N, dR, fR, dL, fL, dD, fD, dU, fU)
