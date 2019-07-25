# Eclipse SUMO, Simulation of Urban MObility; see https://eclipse.org/sumo
# Copyright (C) 2012-2018 German Aerospace Center (DLR) and others.
# This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v2.0
# which accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v20.html
# SPDX-License-Identifier: EPL-2.0

# @file    polygon.py
# @author  Daniel Krajzewicz
# @author  Melanie Knocke
# @author  Michael Behrisch
# @date    2012-12-04
# @version $Id$

from __future__ import absolute_import

from xml.sax import handler, parse
from .. import color


class Polygon:

    def __init__(self, id, type=None, color=None, layer=None, fill=None, shape=None):
        self.id = id
        self.type = type
        self.color = color
        self.layer = layer
        self.fill = fill
        self.shape = shape
        self.attributes = {}

    def getBoundingBox(self):
        xmin = self.shape[0][0]
        xmax = self.shape[0][0]
        ymin = self.shape[0][1]
        ymax = self.shape[0][1]
        for p in self.shape[1:]:
            xmin = min(xmin, p[0])
            xmax = max(xmax, p[0])
            ymin = min(ymin, p[1])
            ymax = max(ymax, p[1])
        assert(xmin != xmax or ymin != ymax)
        return xmin, ymin, xmax, ymax

    def getShapeString(self):
        return " ".join([",".join(map(str, e)) for e in self.shape])

    def toXML(self):
        ret = '<poly id="%s"' % self.id
        if self.type is not None:
            ret += ' type="%s"' % self.type
        if self.color is not None:
            ret += ' color="%s"' % self.color.toXML()
        if self.layer is not None:
            ret += ' layer="%s"' % self.layer
        if self.fill is not None:
            ret += ' fill="%s"' % self.fill
        if self.shape is not None:
            ret += ' shape="%s"' % self.getShapeString()
        if len(self.attributes) == 0:
            ret += '/>'
        else:
            ret += '>'
            for a in self.attributes:
                ret += '<param key="%s" value="%s"/>' % (a, self.attributes[a])
            ret += '</poly>'
        return ret

    def __lt__(self, other):
        return self.id < other.id

    def __repr__(self):
        return self.toXML()


class PolygonReader(handler.ContentHandler):

    def __init__(self, includeTaz=False):
        self._includeTaz = includeTaz
        self._id2poly = {}
        self._polys = []
        self._lastPoly = None

    def startElement(self, name, attrs):
        if name == 'poly' or (self._includeTaz and name == 'taz'):
            cshape = []
            for e in attrs['shape'].split():
                p = e.split(",")
                cshape.append((float(p[0]), float(p[1])))
            if name == 'poly' and not self._includeTaz:
                c = color.decodeXML(attrs['color'])
                poly = Polygon(attrs['id'], attrs['type'], c, float(
                               attrs['layer']), attrs['fill'], cshape)
            else:
                poly = Polygon(attrs['id'], shape=cshape)
            self._id2poly[poly.id] = poly
            self._polys.append(poly)
            self._lastPoly = poly
        if name == 'param' and self._lastPoly is not None:
            self._lastPoly.attributes[attrs['key']] = attrs['value']

    def endElement(self, name):
        if name == 'poly':
            self._lastPoly = None

    def getPolygons(self):
        return self._polys


def read(filename, includeTaz=False):
    polys = PolygonReader(includeTaz)
    parse(filename, polys)
    return polys.getPolygons()
