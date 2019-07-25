#!/usr/bin/env python
# Eclipse SUMO, Simulation of Urban MObility; see https://eclipse.org/sumo
# Copyright (C) 2009-2017 German Aerospace Center (DLR) and others.
# This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v2.0
# which accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v20.html

# @file    generateTLSE1Detectors.py
# @author  Daniel Krajzewicz
# @author  Karol Stosiek
# @author  Michael Behrisch
# @date    2011-10-07
# @version $Id$

from __future__ import absolute_import
from __future__ import print_function

import logging
import optparse
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import sumolib  # noqa


def get_net_file_directory(net_file):
    """ Returns the directory containing the net file given. """

    dirname = os.path.split(net_file)[0]
    return dirname


def open_detector_file(destination_dir, detector_file_name):
    """ Opens a new detector file in given directory. """

    return open(os.path.join(destination_dir, detector_file_name), "w")


def adjust_detector_length(requested_detector_length,
                           requested_distance_to_tls,
                           lane_length):
    """ Adjusts requested detector's length according to
        the lane length and requested distance to TLS.

        If requested detector length is negative, the resulting detector length
        will match the distance between requested distance to TLS and lane
        beginning.


        If the requested detector length is positive, it will be adjusted
        according to the end of lane ending with TLS: the resulting length
        will be either the requested detector length or, if it's too long
        to be placed in requested distance from TLS, it will be shortened to
        match the distance between requested distance to TLS
        and lane beginning. """

    if requested_detector_length == -1:
        return lane_length - requested_distance_to_tls

    return min(lane_length - requested_distance_to_tls,
               requested_detector_length)


def adjust_detector_position(final_detector_length,
                             requested_distance_to_tls,
                             lane_length):
    """ Adjusts the detector's position. If the detector's length
        and the requested distance to TLS together are longer than
        the lane itself, the position will be 0; it will be
        the maximum distance from lane end otherwise (taking detector's length
        and requested distance to TLS into accout). """

    return max(0,
               lane_length - final_detector_length - requested_distance_to_tls)

if __name__ == "__main__":
    # pylint: disable-msg=C0103

    logging.basicConfig(level="INFO")

    option_parser = optparse.OptionParser()
    option_parser.add_option("-n", "--net-file",
                             dest="net_file",
                             help="Network file to work with. Mandatory.",
                             type="string")
    option_parser.add_option("-l", "--detector-length",
                             dest="requested_detector_length",
                             help="Length of the detector in meters "
                             "(-1 for maximal length).",
                             type="int",
                             default=250)
    option_parser.add_option("-d", "--distance-to-TLS",
                             dest="requested_distance_to_tls",
                             help="Distance of the detector to the traffic "
                             "light in meters. Defaults to 0.1m.",
                             type="float",
                             default=.1)
    option_parser.add_option("-f", "--frequency",
                             dest="frequency",
                             help="Detector's frequency. Defaults to 60.",
                             type="int",
                             default=60)
    option_parser.add_option("-o", "--output",
                             dest="output",
                             help="The name of the file to write the detector "
                             "definitions into. Defaults to e1.add.xml.",
                             type="string",
                             default="e1.add.xml")
    option_parser.add_option("-r", "--results-file",
                             dest="results",
                             help="The name of the file the detectors write "
                             "their output into. Defaults to e1output.xml.",
                             type="string",
                             default="e1output.xml")
    option_parser.set_usage("generateTLSE1Detectors.py -n example.net.xml "
                            "-l 250 -d .1 -f 60")

    (options, args) = option_parser.parse_args()
    if not options.net_file:
        print("Missing arguments")
        option_parser.print_help()
        exit()

    logging.info("Reading net...")
    net = sumolib.net.readNet(options.net_file)

    logging.info("Generating detectors...")
    detectors_xml = sumolib.xml.create_document("additional")
    lanes_with_detectors = set()
    for tls in net._tlss:
        for connection in tls._connections:
            lane = connection[0]
            lane_length = lane.getLength()
            lane_id = lane.getID()

            logging.debug("Creating detector for lane %s" % (str(lane_id)))

            if lane_id in lanes_with_detectors:
                logging.warn("Detector for lane %s already generated" %
                             (str(lane_id)))
                continue

            lanes_with_detectors.add(lane_id)

            final_detector_length = adjust_detector_length(
                options.requested_detector_length,
                options.requested_distance_to_tls,
                lane_length)
            final_detector_position = adjust_detector_position(
                final_detector_length,
                options.requested_distance_to_tls,
                lane_length)

            detector_xml = detectors_xml.addChild("e1Detector")
            detector_xml.setAttribute("file", options.results)
            detector_xml.setAttribute("freq", str(options.frequency))
            detector_xml.setAttribute("friendlyPos", "x")
            detector_xml.setAttribute("id", "e1det_" + str(lane_id))
            detector_xml.setAttribute("lane", str(lane_id))
            detector_xml.setAttribute("length", str(final_detector_length))
            detector_xml.setAttribute("pos", str(final_detector_position))

    detector_file = open_detector_file(
        get_net_file_directory(options.net_file),
        options.output)
    detector_file.write(detectors_xml.toXML())
    detector_file.close()

    logging.info("%d e1 detectors generated!" % len(lanes_with_detectors))
