# -*- coding: utf-8 -*-
# Eclipse SUMO, Simulation of Urban MObility; see https://eclipse.org/sumo
# Copyright (C) 2008-2018 German Aerospace Center (DLR) and others.
# This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v2.0
# which accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v20.html
# SPDX-License-Identifier: EPL-2.0

# @file    __init__.py
# @author  Michael Behrisch
# @author  Lena Kalleske
# @author  Mario Krumnow
# @author  Daniel Krajzewicz
# @author  Jakob Erdmann
# @date    2008-10-09
# @version $Id$

from __future__ import print_function
from __future__ import absolute_import
import socket
import time
import subprocess
import warnings
import abc
import sys
import os

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

import sumolib  # noqa
from sumolib.miscutils import getFreeSocketPort  # noqa

from .domain import _defaultDomains  # noqa
from .connection import Connection, _embedded  # noqa
from .exceptions import FatalTraCIError, TraCIException  # noqa
from . import _inductionloop, _lanearea, _multientryexit, _trafficlight  # noqa
from . import _lane, _person, _route, _vehicle, _vehicletype  # noqa
from . import _edge, _gui, _junction, _poi, _polygon, _simulation  # noqa

_connections = {}
_stepListeners = {}
_nextStepListenerID = 0
# cannot use immutable type as global variable
_currentLabel = [""]


def _STEPS2TIME(step):
    """Conversion from time steps in milliseconds to seconds as float"""
    return step / 1000.


def connect(port=8813, numRetries=10, host="localhost", proc=None):
    """
    Establish a connection to a TraCI-Server and return the
    connection object. The connection is not saved in the pool and not
    accessible via traci.switch. It should be safe to use different
    connections established by this method in different threads.
    """
    for wait in range(1, numRetries + 2):
        try:
            return Connection(host, port, proc)
        except socket.error as e:
            if wait > 1:
                print("Could not connect to TraCI server at %s:%s" % (host, port), e)
            if wait < numRetries + 1:
                print(" Retrying in %s seconds" % wait)
                time.sleep(wait)
    raise FatalTraCIError("Could not connect in %s tries" % (numRetries + 1))


def init(port=8813, numRetries=10, host="localhost", label="default"):
    """
    Establish a connection to a TraCI-Server and store it under the given
    label. This method is not thread-safe. It accesses the connection
    pool concurrently.
    """
    _connections[label] = connect(port, numRetries, host)
    switch(label)
    return getVersion()


def start(cmd, port=None, numRetries=10, label="default"):
    """
    Start a sumo server using cmd, establish a connection to it and
    store it under the given label. This method is not thread-safe.
    """
    if port is None:
        port = sumolib.miscutils.getFreeSocketPort()
    sumoProcess = subprocess.Popen(cmd + ["--remote-port", str(port)])
    _connections[label] = connect(port, numRetries, "localhost", sumoProcess)
    switch(label)
    return getVersion()


def isLibsumo():
    return False


def isEmbedded():
    return _embedded


def load(args):
    """load([optionOrParam, ...])
    Let sumo load a simulation using the given command line like options
    Example:
      load(['-c', 'run.sumocfg'])
      load(['-n', 'net.net.xml', '-r', 'routes.rou.xml'])
    """
    return _connections[""].load(args)


def simulationStep(step=0):
    """
    Make a simulation step and simulate up to the given millisecond in sim time.
    If the given value is 0 or absent, exactly one step is performed.
    Values smaller than or equal to the current sim time result in no action.
    """
    global _stepListeners
    responses = _connections[""].simulationStep(step)

    # manage stepListeners
    listenersToRemove = []
    for (listenerID, listener) in _stepListeners.items():
        keep = listener.step(step)
        if not keep:
            listenersToRemove.append(listenerID)
    for listenerID in listenersToRemove:
        removeStepListener(listenerID)

    return responses


class StepListener(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def step(self, s=0):
        """step(int) -> bool

        After adding a StepListener 'listener' with traci.addStepListener(listener),
        TraCI will call listener.step(s) after each call to traci.simulationStep(s)
        The return value indicates whether the stepListener wants to stay active.
        """
        return True

    def cleanUp(self):
        """cleanUp() -> None

        This method is called at removal of the stepListener, allowing to schedule some final actions
        """
        pass

    def setID(self, ID):
        self._ID = ID

    def getID(self):
        return self._ID


def addStepListener(listener):
    """addStepListener(traci.StepListener) -> int

    Append the step listener (its step function is called at the end of every call to traci.simulationStep())
    Returns the ID assigned to the listener if it was added successfully, None otherwise.
    """
    global _nextStepListenerID, _stepListeners
    if issubclass(type(listener), StepListener):
        listener.setID(_nextStepListenerID)
        _stepListeners[_nextStepListenerID] = listener
        _nextStepListenerID += 1
        # print ("traci: Added stepListener %s\nlisteners: %s"%(_nextStepListenerID - 1, _stepListeners))
        return _nextStepListenerID - 1
    warnings.warn(
        "Proposed listener's type must inherit from traci.StepListener. Not adding object of type '%s'" %
        type(listener))
    return None


def removeStepListener(listenerID):
    """removeStepListener(traci.StepListener) -> bool

    Remove the step listener from traci's step listener container.
    Returns True if the listener was removed successfully, False if it wasn't registered.
    """
    global _stepListeners
    # print ("traci: removeStepListener %s\nlisteners: %s"%(listenerID, _stepListeners))
    if listenerID in _stepListeners.keys():
        _stepListeners[listenerID].cleanUp()
        del _stepListeners[listenerID]
        # print ("traci: Removed stepListener %s"%(listenerID))
        return True
    msg = "removeStepListener(listener): listener %s not registered as step listener.\nlisteners:%s" % (
        listenerID, _stepListeners)
    # print ("traci: "+msg)
    warnings.warn(msg)
    return False


def getVersion():
    return _connections[""].getVersion()


def setOrder(order):
    return _connections[""].setOrder(order)


def close(wait=True):
    _connections[""].close(wait)


def switch(label):
    _currentLabel[0] = label
    _connections[""] = _connections[label]
    for domain in _defaultDomains:
        domain._setConnection(_connections[""])


def getLabel():
    return _currentLabel[0]


def getConnection(label="default"):
    if label not in _connections:
        raise TraCIException("connection with label '%s' is not known")
    return _connections[label]


if _embedded:
    # create the default dummy connection
    init()
