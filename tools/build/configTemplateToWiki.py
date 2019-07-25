#!/usr/bin/env python
# Eclipse SUMO, Simulation of Urban MObility; see https://eclipse.org/sumo
# Copyright (C) 2008-2017 German Aerospace Center (DLR) and others.
# This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v2.0
# which accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v20.html

# @file    configTemplateToWiki.py
# @author  Michael Behrisch
# @date    2012-01-26
# @version $Id$

from __future__ import absolute_import
from __future__ import print_function
import os
import sys
from xml.sax import parse, handler

from mirrorWiki import readParseEditPage


class ConfigReader(handler.ContentHandler):

    def __init__(self, mergeWikiTxt):
        self._level = 0
        self._mergeWiki = mergeWikiTxt
        self._intro = {}
        self._end = len(mergeWikiTxt)
        active = False
        currSect = ""
        for idx, line in enumerate(mergeWikiTxt):
            line = line.strip('\n\r')
            if line == "==Options==":
                active = True
            if active:
                if line[:3] == "===":
                    start = idx
                    currSect = line
                elif line[:2] == "{|":
                    self._intro[currSect] = (start, idx)
                elif line[:4] == "----" or (len(line) > 2 and line[0] == "=" and line[1] != "="):
                    self._end = idx
                    break
            if currSect == "":
                print(line)

    def startElement(self, name, attrs):
        if self._level == 1:
            # subtopic
            title = "===%s===" % name.replace("_", " ").title()
            if title in self._intro:
                begin, end = self._intro[title]
                title = ("".join(self._mergeWiki[begin:end]))
            else:
                title += "\n"
            print("""%s{| class="wikitable" style="width:90%%"
|-
! style="background:#ddffdd; vertical-align:top; width:350px" | Option
! style="background:#ddffdd; vertical-align:top" | Description""" % title)
        if self._level == 2:
            # entry
            print('|-\n| style="vertical-align:top" |', end=' ')
            a = ""
            for s in attrs.get('synonymes', '').split():
                if len(s) == 1:
                    a = s
            if a != "":
                print('{{Option|-%s {{DT_%s}}}}<br/>' %
                      (a, attrs['type']), end=' ')
            print('{{Option|--%s {{DT_%s}}}}' % (name, attrs['type']))
            suffix = ""
            if attrs['value']:
                suffix = "; ''default: '''%s'''''" % attrs['value']
            print('| style="vertical-align:top" | %s%s' %
                  (attrs['help'], suffix))
        self._level += 1

    def endElement(self, name):
        self._level -= 1
        if self._level == 1:
            # subtopic end
            print("|-\n|}\n")

    def endDocument(self):
        print(("".join(self._mergeWiki[self._end:])).strip())

if __name__ == "__main__":
    if len(sys.argv) == 2:
        app = sys.argv[1].lower()
        if app == "netgenerate":
            app = "netgen"
        cfg = os.path.join(os.path.dirname(
            __file__), "..", "..", "tests", app, "meta", "write_template_full", "cfg." + app)
        parse(
            cfg, ConfigReader(readParseEditPage(sys.argv[1].upper()).splitlines(True)))
    elif len(sys.argv) == 3:
        parse(sys.argv[1], ConfigReader(open(sys.argv[2]).readlines()))
    else:
        print("Usage: %s <template> <wikisrc>\n   or: %s <app>" % (
            os.path.basename(__file__), os.path.basename(__file__)), file=sys.stderr)
