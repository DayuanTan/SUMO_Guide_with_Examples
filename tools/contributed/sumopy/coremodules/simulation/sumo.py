# Eclipse SUMO, Simulation of Urban MObility; see https://eclipse.org/sumo
# Copyright (C) 2016-2017 German Aerospace Center (DLR) and others.
# SUMOPy module
# Copyright (C) 2012-2017 University of Bologna - DICAM
# This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v2.0
# which accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v20.html

# @file    sumo.py
# @author  Joerg Schweizer
# @date    
# @version $Id$

import os
import sys
import string
from xml.sax import saxutils, parse, handler
if __name__ == '__main__':
    try:
        APPDIR = os.path.dirname(os.path.abspath(__file__))
    except:
        APPDIR = os.path.dirname(os.path.abspath(sys.argv[0]))
    SUMOPYDIR = os.path.join(APPDIR, '..', '..')
    sys.path.append(SUMOPYDIR)

from coremodules.modules_common import *
import numpy as np
import agilepy.lib_base.classman as cm
import agilepy.lib_base.arrayman as am
import agilepy.lib_base.xmlman as xm
#from agilepy.lib_base.misc import get_inversemap
#from agilepy.lib_base.geometry import find_area
from agilepy.lib_base.processes import Process, CmlMixin, ff, call, P
from coremodules.network.network import SumoIdsConf


def write_netconfig(filename_netconfig, filename_net,
                    filename_routes='',
                    filename_poly=None,
                    dirname_output='',
                    starttime=None, stoptime=None,
                    time_step=1.0,
                    time_to_teleport=-1,
                    pedestrian_model='None',
                    width_sublanes=-1.0,
                    filename_ptstops=None,
                    filepath_output_vehroute=None,
                    filepath_output_tripinfo=None,
                    filepath_output_edgedata=None,
                    filepath_output_lanedata=None,
                    filepath_output_edgeemissions=None,
                    filepath_output_laneemissions=None,
                    filepath_output_edgenoise=None,
                    filepath_output_lanenoise=None,
                    freq=60,
                    is_exclude_emptyedges=False,
                    is_exclude_emptylanes=False,
                    is_ignore_route_errors=True,
                    seed=1025):
    """
    filename_netconfig = output filename of network config file without path 
    filename_net = input filename of network  file without path
    filename_rou = input filename of routes  file without path
    filename_poly = input filename of polygons file without path
    dirname_output = directory where config, network, route and poly file reside
    """
    print 'write_netconfig >>%s<<' % filename_netconfig
    print '  filename_poly=>>%s<<' % filename_poly
    if dirname_output:
        filepath_netconfig = os.path.join(dirname_output, filename_netconfig)
    else:
        filepath_netconfig = filename_netconfig

    if (filepath_output_edgedata != None)\
            | (filepath_output_lanedata != None)\
            | (filepath_output_edgeemissions != None)\
            | (filepath_output_laneemissions != None)\
            | (filepath_output_edgenoise != None)\
            | (filepath_output_lanenoise != None):
        # filename of additional files:
        filename_add = string.join(filename_netconfig.split('.')[
                                   :-2] + ['add.xml'], '.')
        filepath_add = os.path.join(dirname_output, filename_add)
        # print '  filepath_add',filepath_add
    else:
        filename_add = None

    simfile = open(filepath_netconfig, 'w')

    simfile.write(
        """<?xml version="1.0"?>
<configuration xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.sf.net/xsd/sumoConfiguration.xsd">
<input>\n""")

    simfile.write('  <net-file value="%s"/>\n' % filename_net)

    if filename_routes != "":
        simfile.write('  <route-files value="%s"/>\n' % filename_routes)

    # print '  filename_add',filename_add
    # print '  filepath_add',filepath_add
    simfile.write('  <additional-files value="')

    filenames_add = set([filename_poly, filename_add,
                         filename_add, filename_ptstops])
    filenames_add.discard(None)
    filenames_add = list(filenames_add)

    if len(filenames_add) > 0:
        for filename in filenames_add[:-1]:
            simfile.write('%s,' % filename)
        simfile.write('%s' % filenames_add[-1])

    simfile.write('" />\n')
    simfile.write('</input>\n')

    if (starttime != None) & (stoptime != None):
        simfile.write(
            """
<time>
    <begin value="%s"/>
    <end value="%s"/>
</time>
        """ % (starttime, stoptime))

    simfile.write('<time-to-teleport value="%s"/>\n' % time_to_teleport)
    simfile.write('<seed value="%s"/>\n' % seed)
    simfile.write('<step-length value="%s"/>\n' % time_step)

    simfile.write('<ignore-route-errors value="%s"/>\n' %
                  is_ignore_route_errors)

    if width_sublanes > 0:
        simfile.write('<lateral-resolution value="%s"/>\n' % width_sublanes)
    # not (yet) recogniced...move to cml
    if pedestrian_model != 'None':
        simfile.write('<pedestrian.model value="%s"/>\n' % pedestrian_model)

    simfile.write('<output>\n')
    #<output-file value="quickstart.net.xml"/>

    if filepath_output_vehroute != None:
        simfile.write('<vehroute-output value="%s"/>\n' %
                      filepath_output_vehroute)
    if filepath_output_tripinfo != None:
        simfile.write('<tripinfo-output value="%s"/>\n' %
                      filepath_output_tripinfo)

    simfile.write('</output>\n')

    #<report>
    #    <no-duration-log value="true"/>
    #    <no-step-log value="true"/>
    #</report>

    simfile.write('</configuration>\n')
    simfile.close()

    # add path to  additional files if necessary
    if filename_add != None:
        addfile = open(filepath_add, 'w')
        addfile.write('<add>\n')
        if filepath_output_edgedata != None:
            addfile.write('  <edgeData id="output_edgedata_%d" freq="%d" file="%s" excludeEmpty="%s"/>\n' %
                          (freq, freq, filepath_output_edgedata, str(is_exclude_emptyedges).lower()))

        if filepath_output_lanedata != None:
            addfile.write('  <laneData id="output_lanedata_%d" freq="%d" file="%s" excludeEmpty="%s"/>\n' %
                          (freq, freq, filepath_output_lanedata, str(is_exclude_emptylanes).lower()))

        if filepath_output_edgeemissions != None:
            addfile.write('  <edgeData id="output_edgeemissions_%d" type="emissions" freq="%d" file="%s" excludeEmpty="%s"/>\n' %
                          (freq, freq, filepath_output_edgeemissions, str(is_exclude_emptyedges).lower()))

        if filepath_output_laneemissions != None:
            addfile.write('  <laneData id="output_laneemissions_%d" type="emissions" freq="%d" file="%s" excludeEmpty="%s"/>\n' %
                          (freq, freq, filepath_output_laneemissions, str(is_exclude_emptylanes).lower()))

        if filepath_output_edgenoise != None:
            addfile.write('  <edgeData id="edgenoise_%d" type="harmonoise" freq="%d" file="%s" excludeEmpty="%s"/>\n' %
                          (freq, freq, filepath_output_edgenoise, str(is_exclude_emptyedges).lower()))

        if filepath_output_lanenoise != None:
            addfile.write('  <laneData id="lanenoise_%d" type="harmonoise" freq="%d" file="%s" excludeEmpty="%s"/>\n' %
                          (freq, freq, filepath_output_lanenoise, str(is_exclude_emptylanes).lower()))

        addfile.write('</add>\n')
        addfile.close()


class Sumo(CmlMixin, Process):

    def __init__(self, scenario,
                 results=None,
                 logger=None,
                 is_gui=False, is_runnow=False,
                 is_run_background=False, is_nohup=False,
                 workdirpath=None,
                 is_export_net=False,
                 is_export_poly=False,
                 is_export_rou=False,
                 method_routechoice=None,
                 **kwargs):
        self._init_common('sumo', name='SUMO',
                          logger=logger,
                          info='SUMO simulation of scenario.',
                          )
        self._results = results
        rootname = scenario.get_rootfilename()
        rootdirpath = scenario.get_workdirpath()
        self.configfilepath = os.path.join(rootdirpath, rootname + '.netc.xml')

        # if simresults == None:
        #    self.simresults = Simresults(scenario=scenario)

        self.init_cml('xxx', is_run_background=is_run_background,
                      is_nohup=is_nohup)  # pass main shell command
        attrsman = self.get_attrsman()

        # print '\nSumo.__init__',kwargs

        #self.scenario = scenario
        #self.settings = scenario.settings
        self.is_gui = attrsman.add(cm.AttrConf('is_gui', is_gui,
                                               groupnames=['options', 'misc'],
                                               name='run in gui mode',
                                               perm='rw',
                                               info='If selected show animation in window'
                                               ))

        if is_export_net:
            netfilepath = scenario.net.export_netxml()
            if netfilepath is not False:
                # export OK, network is not an option
                groupnames = ['input', '_private']
            else:
                # something went wrong with exporting
                netfilepath = os.path.join(rootdirpath, rootname + '.net.xml')
                groupnames = ['input', 'options']

        else:
            netfilepath = os.path.join(rootdirpath, rootname + '.net.xml')
            groupnames = ['input', '_private']

        self.netfilepath = attrsman.add(cm.AttrConf('netfilepath', netfilepath,
                                                    groupnames=groupnames,
                                                    perm='rw',
                                                    name='Netfile',
                                                    wildcards='SUMO net XML files (*.net.xml)|*.net.xml',
                                                    metatype='filepath',
                                                    info="""SUMO network xml file.""",
                                                    ))

        self.dirpath_results = attrsman.add(cm.AttrConf('dirpath_results', rootdirpath,
                                                        groupnames=['input'],
                                                        perm='rw',
                                                        name='Result directory',
                                                        metatype='dirpath',
                                                        info="""Directory where general SUMO simulation result files are placed.""",
                                                        ))

        if is_export_rou:
            routefilepaths = scenario.demand.trips.export_routes_xml(
                method_routechoice=method_routechoice)
            if routefilepaths is not False:
                # export OK, network is not an option
                groupnames = ['input', '_private']
            else:
                # something went wrong with exporting
                routefilepaths = kwargs.get(
                    'routefilepaths', scenario.demand.trips.get_routefilepath())
                groupnames = ['input', 'options']

        else:
            routefilepaths = kwargs.get(
                'routefilepaths', scenario.demand.trips.get_routefilepath())
            groupnames = ['input', 'options']

        self.routefilepaths = attrsman.add(cm.AttrConf('routefilepaths', routefilepaths,
                                                       groupnames=groupnames,
                                                       perm='rw',
                                                       name='Route file(s)',
                                                       wildcards='Typemap XML files (*.rou.xml)|*.rou.xml',
                                                       metatype='filepaths',
                                                       info='SUMO route xml file.\n'
                                                       +
                                                       'If multiple, comma separated files are given'
                                                       +
                                                       ' then make sure the start time of trips'
                                                       +
                                                       ' are in increasing chronological order.',
                                                       ))

        simtime_start_default = scenario.demand.trips.get_time_depart_first()
        # estimate end of simtime
        simtime_end_default = scenario.demand.trips.get_time_depart_last() + \
            600.0

        self.simtime_start = attrsman.add(cm.AttrConf('simtime_start', kwargs.get('simtime_start', simtime_start_default),
                                                      groupnames=[
                                                          'options', 'timing'],
                                                      name='Start time',
                                                      perm='rw',
                                                      info='Start time of simulation in seconds after midnight.',
                                                      unit='s',
                                                      ))

        self.simtime_end = attrsman.add(cm.AttrConf('simtime_end', kwargs.get('simtime_end', simtime_end_default),
                                                    groupnames=[
                                                        'options', 'timing'],
                                                    name='End time',
                                                    perm='rw',
                                                    info='End time of simulation in seconds after midnight.',
                                                    unit='s',
                                                    ))

        self.time_step = attrsman.add(cm.AttrConf('time_step', kwargs.get('time_step', 0.2),
                                                  groupnames=[
                                                      'options', 'timing'],
                                                  name='Time step',
                                                  perm='rw',
                                                  info='Basic simulation time step (1s by default).',
                                                  metatype='time',
                                                  unit='s',
                                                  ))

        self.time_to_teleport = attrsman.add(cm.AttrConf('time_to_teleport', kwargs.get('time_to_teleport', -1),
                                                         groupnames=[
                                                             'options', 'timing'],
                                                         name='teleport',
                                                         perm='rw',
                                                         info='Time to teleport in seconds, which is the time after'
                                                         +
                                                         'dedlocks get resolved by teleporting\n'
                                                         +
                                                         '-1 means no teleporting takes place',
                                                         metatype='time',
                                                         unit='s',
                                                         ))

        self.time_sample = attrsman.add(cm.AttrConf('time_sample', kwargs.get('time_sample', 60),
                                                    groupnames=[
                                                        'options', 'timing'],
                                                    name='Output sample time',
                                                    perm='rw',
                                                    info='Common sampling time of output data.',
                                                    metatype='time',
                                                    unit='s',
                                                    ))

        # print '  ',scenario.demand.vtypes.lanechangemodel.get_value()
        if scenario.demand.vtypes.lanechangemodel.get_value() in ['SL2015', ]:
            width_sublanes_default = 1.0
        else:
            width_sublanes_default = -1.0

        self.width_sublanes = attrsman.add(cm.AttrConf('width_sublanes', kwargs.get('width_sublanes', width_sublanes_default),
                                                       groupnames=[
                                                           'options', 'edges'],
                                                       #cml = '--lateral-resolution',
                                                       perm='rw',
                                                       name='Sublane width',
                                                       unit='m',
                                                       info='Width of sublanes. Should be less than lane width. If negative the sublanes are disabeled.',
                                                       is_enabled=lambda self: self.width_sublanes > 0,
                                                       ))

        self.pedestrian_model = attrsman.add(cm.AttrConf('pedestrian_model', kwargs.get('pedestrian_model', 'striping'),
                                                         groupnames=[
                                                             'options', 'parameters'],
                                                         name='Pedestrian Model',
                                                         choices=[
                                                             'striping', 'nonInteracting', 'None'],
                                                         perm='rw',
                                                         info='Type of Pedestrian model.',
                                                         ))

        self.is_edgedata = attrsman.add(cm.AttrConf('is_edgedata', kwargs.get('is_edgedata', False),
                                                    groupnames=[
                                                        'options', 'output'],
                                                    name='Output edge data',
                                                    perm='rw',
                                                    info='If set, generate detailed data for all edges.'
                                                    ))

        self.is_routedata = attrsman.add(cm.AttrConf('is_routedata', kwargs.get('is_routedata', False),
                                                     groupnames=[
                                                         'options', 'output'],
                                                     name='Output route data',
                                                     perm='rw',
                                                     info='If set, generate detailed data for all routes.'
                                                     ))

        self.is_tripdata = attrsman.add(cm.AttrConf('is_tripdata', kwargs.get('is_tripdata', False),
                                                    groupnames=[
                                                        'options', 'output'],
                                                    name='Output trip data',
                                                    perm='rw',
                                                    info='If set, generate detailed data for all trips.'
                                                    ))

        self.is_edgenoise = attrsman.add(cm.AttrConf('is_edgenoise', kwargs.get('is_edgenoise', False),
                                                     groupnames=[
                                                         'options', 'output'],
                                                     name='Output edge noise',
                                                     perm='rw',
                                                     info='If set, generate noise information for all edges.'
                                                     ))

        self.is_edgesemissions = attrsman.add(cm.AttrConf('is_edgesemissions', kwargs.get('is_edgesemissions', False),
                                                          groupnames=[
                                                              'options', 'output'],
                                                          name='Output edge emissions',
                                                          perm='rw',
                                                          info='If set, generate emission information for all edges.'
                                                          ))

        outfile_prefix = kwargs.get('outfile_prefix', 'out')
        self.routesdatapath = attrsman.add(cm.AttrConf('routesdatapath', os.path.join(rootdirpath, rootname + '.' + outfile_prefix + '.roudata.xml'),
                                                       groupnames=[
                                                           'outputfiles', '_private'],
                                                       perm='r',
                                                       name='Route data file',
                                                       wildcards='Route data XML files (*.roudata.xml)|*.roudata.xml',
                                                       metatype='filepath',
                                                       info="""SUMO xml file with route output info.""",
                                                       #attrnames_data = ['depart','arrival'],
                                                       #element = 'vehicle',
                                                       #id_type = 'trip',
                                                       #reader = 'plain',
                                                       ))

        self.tripdatapath = attrsman.add(cm.AttrConf('tripdatapath', os.path.join(rootdirpath, rootname + '.' + outfile_prefix + '.tripdata.xml'),
                                                     groupnames=[
                                                         'outputfiles', '_private'],
                                                     perm='r',
                                                     name='Edge data file',
                                                     wildcards='Trip data XML files (*.tripdata.xml)|*.tripdata.xml',
                                                     metatype='filepath',
                                                     info="""SUMO xml file with trip output data.""",
                                                     attrnames_data=[
                                                         'depart', 'arrival', 'duration'],
                                                     #element = 'tripinfo',
                                                     #id_type = 'trip',
                                                     #reader = 'plain',
                                                     ))

        self.edgedatapath = attrsman.add(cm.AttrConf('edgedatapath', os.path.join(rootdirpath, rootname + '.' + outfile_prefix + '.edgedata.xml'),
                                                     groupnames=[
                                                         'outputfiles', '_private'],
                                                     perm='r',
                                                     name='Edge data file',
                                                     wildcards='Edge data XML files (*.edgedata.xml)|*.edgedata.xml',
                                                     metatype='filepath',
                                                     info="""SUMO xml file with edge output data.""",
                                                     ))

        self.edgenoisepath = attrsman.add(cm.AttrConf('edgenoisepath', os.path.join(rootdirpath, rootname + '.' + outfile_prefix + '.edgenoise.xml'),
                                                      groupnames=[
                                                          'outputfiles', '_private'],
                                                      perm='r',
                                                      name='Edge noise file',
                                                      wildcards='Edge noise XML files (*.edgenoise.xml)|*.edgenoise.xml',
                                                      metatype='filepath',
                                                      info="""SUMO xml file with edge noise data.""",
                                                      #attrnames_averaged = ['noise'],
                                                      #element = 'edge',
                                                      #id_type = 'edge',
                                                      #reader = 'interval',
                                                      ))

        self.edgeemissionspath = attrsman.add(cm.AttrConf('edgeemissionspath', os.path.join(rootdirpath, rootname + '.' + outfile_prefix + '.edgeemissions.xml'),
                                                          groupnames=[
                                                              'outputfiles', '_private'],
                                                          perm='r',
                                                          name='Edge noise file',
                                                          wildcards='Edge noise XML files (*.edgeemissions.xml)|*.edgeemissions.xml',
                                                          metatype='filepath',
                                                          info="""SUMO xml file with edge emission data.""",
                                                          attrnames_data=[
                                                              'fuel_abs', 'CO_abs', 'CO2_abs', 'NOx_abs', 'PMx_abs'],
                                                          attrnames_averaged=[
                                                              'fuel_normed', 'CO_normed', 'CO2_normed', ],
                                                          element='edge',
                                                          id_type='edge',
                                                          reader='interval',
                                                          ))

        self.is_exclude_emptyedges = attrsman.add(cm.AttrConf('is_exclude_emptyedges', kwargs.get('is_exclude_emptyedges', True),
                                                              name='No empty edges',
                                                              perm='rw',
                                                              groupnames=[
                                                                  'options', 'misc'],
                                                              info='Excludes empty edges from being sampled.',
                                                              ))

        self.is_exclude_emptylanes = attrsman.add(cm.AttrConf('is_exclude_emptylanes', kwargs.get('is_exclude_emptylanes', True),
                                                              name='No empty lanes',
                                                              perm='rw',
                                                              groupnames=[
                                                                  'options', 'misc'],
                                                              info='Excludes empty edges from being sampled.',
                                                              ))

        self.seed = attrsman.add(cm.AttrConf('seed', kwargs.get('seed', 0),
                                             name='Seed',
                                             perm='rw',
                                             groupnames=['options', 'misc'],
                                             info='Ransdom seed.',
                                             ))

        self.is_include_poly = attrsman.add(cm.AttrConf('is_include_poly', kwargs.get('is_include_poly', True),
                                                        name='Include buildings',
                                                        perm='rw',
                                                        groupnames=[
                                                            'options', 'misc'],
                                                        info='Include building polynomials. Only for visualization purposes.',
                                                        ))

        # print '  is_export_poly',is_export_poly
        if is_export_poly:
            polyfilepath = scenario.landuse.export_polyxml()
            # print '  export_polyxml',polyfilepath
            if polyfilepath is not False:
                # export OK,  not an option
                groupnames = ['input', '_private']
            else:
                # something went wrong with exporting
                polyfilepath = os.path.join(
                    rootdirpath, rootname + '.poly.xml')
                groupnames = ['input', 'options']

        else:
            polyfilepath = os.path.join(rootdirpath, rootname + '.poly.xml')
            groupnames = ['input', 'options']

        self.polyfilepath = attrsman.add(cm.AttrConf('polyfilepath', polyfilepath,
                                                     groupnames=groupnames,
                                                     perm='rw',
                                                     name='Poly file',
                                                     wildcards='Poly XML files (*.poly.xml)|*.poly.xml',
                                                     metatype='filepath',
                                                     info='SUMO polynomial xml file',
                                                     ))

        # print '  is_export_poly,is_include_poly,
        # filepath_poly',is_export_poly, self.is_include_poly,
        # self.polyfilepath

        if is_runnow:
            self.run()

    def is_ready(self):
        """
        Returns True if process is ready to run.

        """
        # here we can check existance of files
        return True

    def do(self):
        """
        Called by run after is_ready verification
        """

        print 'do... '
        if self.is_routedata:
            routesdatapath = self.routesdatapath
        else:
            routesdatapath = None

        if self.is_tripdata:
            tripdatapath = self.tripdatapath
        else:
            tripdatapath = None

        if self.is_edgedata:
            edgedatapath = self.edgedatapath
        else:
            edgedatapath = None

        if self.is_edgenoise:
            edgenoisepath = self.edgenoisepath
        else:
            edgenoisepath = None

        if self.is_edgesemissions:
            edgeemissionspath = self.edgeemissionspath
        else:
            edgeemissionspath = None

        # print '  is_include_poly, filepath_poly', self.is_include_poly,
        # self.polyfilepath
        if self.is_include_poly:
            if os.path.isfile(self.polyfilepath):
                filename_poly = os.path.basename(self.polyfilepath)
            else:
                filename_poly = None
        else:
            filename_poly = None

        # if self.files_input.filepath.get('ptstops')=='':
        #    filepath_ptstops = None
        #    filename_ptstops = None
        # else:
        #    filepath_ptstops = self.files_input.filepath.get('ptstops')
        #    filename_ptstops = os.path.basename(filepath_ptstops)

        # print '  >>%s<<'%self.configfilepath
        #filename_netconfig = os.path.basename(self.filepath_netconfig)

        # print '  filepath_poly =',filepath_poly
        # print '  filename_poly =',filename_poly
        # write configuration file

        write_netconfig(
            self.configfilepath,
            self.netfilepath,
            self.routefilepaths,
            starttime=self.simtime_start,
            stoptime=self.simtime_end,
            time_step=self.time_step,
            #filename_ptstops = filename_ptstops,
            pedestrian_model=self.pedestrian_model,
            width_sublanes=self.width_sublanes,
            filename_poly=filename_poly,
            dirname_output=self.dirpath_results,
            time_to_teleport=self.time_to_teleport,
            filepath_output_vehroute=routesdatapath,
            filepath_output_tripinfo=tripdatapath,
            filepath_output_edgedata=edgedatapath,
            #filepath_output_lanedata = self._get_filepath_output('lanedata'),
            filepath_output_edgeemissions=edgeemissionspath,
            #filepath_output_laneemissions = self._get_filepath_output('laneemissions'),
            filepath_output_edgenoise=edgenoisepath,
            #filepath_output_lanenoise = self._get_filepath_output('lanenoise'),
            freq=self.time_sample,
            is_exclude_emptyedges=self.is_exclude_emptyedges,
            is_exclude_emptylanes=self.is_exclude_emptylanes,
            seed=self.seed,
        )

        self.run_cml(cml=self.get_cml())

        self.import_results()

    def import_results(self, results=None):
        """
        Imports simulation resuts into results object. 
        """
        if results == None:
            results = self._results

        if results != None:
            if self.is_edgedata:
                results.edgeresults.import_edgedata(self.edgedatapath)

            if self.is_edgenoise:
                results.edgeresults.import_edgenoise(self.edgenoisepath)

            if self.is_edgesemissions:
                results.edgeresults.import_edgeemissions(
                    self.edgeemissionspath)

            if self.is_routedata:
                results.tripresults.import_routesdata(self.routesdatapath)

            if self.is_tripdata:
                results.tripresults.import_tripdata(self.tripdatapath)

    def get_cml(self):
        """
        TODO: This sould be rather automatic
        Returns commandline with all options.
        To be overridden by costum class.
        """
        if self.is_gui:
            command = 'sumo-gui'
        else:
            command = 'sumo'

        # went into config...
        # if self.pedestrian_model=='None':
        #    pedmodeloptions = ''
        # else:
        #    pedmodeloptions = '--pedestrian.model %s'%self.pedestrian_model
        # return command + ' ' +pedmodeloptions+' -c '+P+self.configfilepath+P
        return command + ' -c ' + P + self.configfilepath + P
