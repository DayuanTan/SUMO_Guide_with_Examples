#!/usr/bin/env python
# -*- coding: Latin-1 -*-
# Eclipse SUMO, Simulation of Urban MObility; see https://eclipse.org/sumo
# Copyright (C) 2008-2017 German Aerospace Center (DLR) and others.
# This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v2.0
# which accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v20.html

# @file    CalcTime.py
# @author  Sascha Krieg
# @author  Daniel Krajzewicz
# @author  Michael Behrisch
# @date    2008-04-17
# @version $Id$

from __future__ import absolute_import
from __future__ import print_function

from time import gmtime
from time import strftime
from time import strptime
from time import mktime
from time import localtime

format = "%Y-%m-%d %H:%M:%S"
formatTime = "%H:%M:%S"
# used simulation date in seconds
simDate = mktime((2007, 7, 18, 0, 0, 0, 2, 199, 1))


def getSecsInTime(time=85460):
    """calculates the Hour:Minutes:Seconds of the given time in seconds."""
    print(strftime(formatTime, gmtime(time)))


def getDateFromDepart(time):
    """calculates the Date from the departtime"""
    return strftime(format, localtime(simDate + int(time)))


def getTimeInSecs(date):
    """calculates the depart time in seconds of the given date (date should be same as simDate)"""
    result = (int)(mktime(strptime(date, format)) - simDate)
    if result < 0:
        print("WARNING: calculated time is negative")
    return result


def getNiceTimeLabel(label='20070718000020'):
    # returns 2007-07-18 00:00:20
    return label[:4] + "-" + label[4:6] + "-" + label[6:8] + " " + label[8:10] + ":" + label[10:12] + ":" + label[12:]
