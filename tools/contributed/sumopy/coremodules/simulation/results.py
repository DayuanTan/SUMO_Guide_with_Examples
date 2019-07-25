# Eclipse SUMO, Simulation of Urban MObility; see https://eclipse.org/sumo
# Copyright (C) 2016-2017 German Aerospace Center (DLR) and others.
# SUMOPy module
# Copyright (C) 2012-2017 University of Bologna - DICAM
# This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v2.0
# which accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v20.html

# @file    results.py
# @author  Joerg Schweizer
# @date    
# @version $Id$


import os
import sys
import string
import types
from xml.sax import saxutils, parse, handler  # , make_parser
from collections import OrderedDict
import numpy as np


from coremodules.modules_common import *

import agilepy.lib_base.classman as cm
import agilepy.lib_base.arrayman as am
import agilepy.lib_base.xmlman as xm
from agilepy.lib_base.geometry import *

from agilepy.lib_base.processes import Process, CmlMixin, ff, call, P
from coremodules.network.network import SumoIdsConf


def load_results(filepath, parent=None, logger=None):
    # typically parent is the scenario
    results = cm.load_obj(filepath, parent=parent)
    if logger != None:
        results.set_logger(logger)
    return results


class Tripresults(am.ArrayObjman):

    def __init__(self, parent, trips, edges, is_add_default=True, **kwargs):

        self._init_objman(ident='tripresults',
                          parent=parent,  # main results object
                          name='Trip results',
                          info='Table with simulation results for each trip made.',
                          **kwargs)

        self.add_col(am.IdsArrayConf('ids_trip', trips,
                                     groupnames=['state'],
                                     is_index=True,
                                     name='ID trip',
                                     info='ID of trip.',
                                     ))
        attrinfos = OrderedDict([
            ('duration', {'name': 'Duration', 'xmltag': 'duration',    'unit': 's',
                          'default': 0, 'info': 'Trip duration', 'groupnames': ['tripdata']}),
            ('depart',   {'name': 'Dep. time', 'xmltag': 'depart',   'unit': 's',
                          'default': 0, 'info': 'Departure time', 'groupnames': ['tripdata']}),
            ('arrival',   {'name': 'Arr. time', 'xmltag': 'arrival',   'unit': 's',
                           'default': 0, 'info': 'Departure time', 'groupnames': ['tripdata']}),
            ('departPos',   {'name': 'depart pos', 'xmltag': 'departPos',   'unit': 'm',
                             'default': 0.0, 'info': 'depart position', 'groupnames': ['tripdata']}),
            ('arrivalPos',   {'name': 'arrival pos', 'xmltag': 'arrivalPos',    'unit': 'm',
                              'default': 0.0, 'info': 'arrival position', 'groupnames': ['tripdata']}),
            ('routeLength',   {'name': 'Length', 'xmltag': 'routeLength',    'unit': 'm',
                               'default': 0.0, 'info': 'Route length', 'groupnames': ['tripdata']}),
            ('waitSteps',   {'name': 'wait steps', 'xmltag': 'waitSteps',   'unit': None,    'default': 0,
                             'info': 'Time steps, the vehicle has been waiting during its trip', 'groupnames': ['tripdata']}),
            ('rerouteNo',   {'name': 'reroute No', 'xmltag': 'rerouteNo',   'unit': None,
                             'default': 0, 'info': 'Number of re-routes', 'groupnames': ['tripdata']}),
        ])

        for attrname, kwargs in attrinfos.iteritems():
            self.add_resultattr(attrname, **kwargs)

        # this is special for route info
        self.add_col(am.IdlistsArrayConf('ids_edges', edges,
                                         name='Edge IDs',
                                         groupnames=['routeinfo'],
                                         info='List of edge IDs constituting the actually taken route.',
                                         xmltag='edges',
                                         ))

    def add_resultattr(self, attrname, **kwargs):

        # default cannot be kwarg
        default = kwargs['default']
        del kwargs['default']
        if kwargs.has_key('groupnames'):
            kwargs['groupnames'].append('results')
        else:
            kwargs['groupnames'] = ['results']

        self.add_col(am.ArrayConf(attrname, default, **kwargs))

    def import_routesdata(self, filepath):
        # TODO
        pass

    def import_tripdata(self, filepath):
        # print 'import_tripdata',filepath,self.get_group('tripdata')
        self.import_sumoxml(filepath, self.get_group('tripdata'))

    def import_sumoxml(self, filepath, attrconfigs):
        element = 'tripinfo'
        # print 'import_sumoxml',element
        #id_type = 'edge',
        #reader = 'interval',

        ids_raw, results, interval = read_interval2(
            filepath, element, attrconfigs)

        # this procedure is necessary to create new result ids only
        # for trips that are not yet in the database
        n = len(ids_raw)
        # print '  n',n
        ind_range = np.arange(n, dtype=np.int32)
        ids = np.zeros(n, dtype=np.int32)
        for i in ind_range:
            id_trip = int(ids_raw[i])
            if self.ids_trip.has_index(id_trip):
                ids[i] = self.ids_trip.get_id_from_index(id_trip)
            else:
                ids[i] = self.add_row(ids_trip=id_trip)

        for attrconfig in attrconfigs:
            attrname = attrconfig.attrname
            default = attrconfig.get_default()
            if type(default) in (types.IntType, types.LongType):
                conversion = 'i'  # int
                values_attr = np.zeros(n, int)
            elif type(default) in (types.FloatType, types.ComplexType):
                conversion = 'f'  # float
                values_attr = np.zeros(n, float)
            else:
                conversion = 's'  # str
                values_attr = np.zeros(n, obj)

            # this is a tricky way to read the data stored in
            # dictionarie into array tructures as used in results
            # problem is that not all dictionaries have all ids
            for i in ind_range:
                val = results[attrname].get(ids_raw[i], default)

                if conversion == 'i':
                    val = int(val)
                else:
                    values_attr[i] = val
                # print '   attrname',attrname,conversion,val,type(val)
                values_attr[i] = val

            # print '  attrname',attrname
            # print '  ids',type(ids),ids
            # print '  values_attr',type(values_attr),values_attr
            attrconfig.set(ids, values_attr)


class Edgeresults(am.ArrayObjman):

    def __init__(self, parent, edges, is_add_default=True, **kwargs):

        self._init_objman(ident='edgeresults',
                          parent=parent,  # main results object
                          name='Edge results',
                          info='Table with simulation results for each network edge.',
                          #xmltag = ('vtypes','vtype','ids_sumo'),
                          **kwargs)

        self.add_col(am.IdsArrayConf('ids_edge', edges,
                                     groupnames=['state'],
                                     is_index=True,
                                     name='ID edge',
                                     info='ID of edge.',
                                     ))

        attrinfos = OrderedDict([
            ('entered',  {'name': 'Entered',      'unit': None,    'default': 0,
                          'info': 'Entered number of vehicles', 'xmltag': 'entered', 'groupnames': ['edgedata']}),
            ('left',     {'name': 'Left',         'unit': None,    'default': 0,
                          'info': 'Left number of vehicles', 'xmltag': 'left', 'groupnames': ['edgedata']}),
            ('arrived',  {'name': 'Arrived',      'unit': None,    'default': 0,
                          'info': 'Arrived number of vehicles', 'xmltag': 'arrived', 'groupnames': ['edgedata']}),
            ('departed', {'name': 'Departed',     'unit': None,    'default': 0,
                          'info': 'Departed number of vehicles', 'xmltag': 'departed', 'groupnames': ['edgedata']}),
            ('traveltime', {'name': 'Av. times',   'unit': 's',     'default': 0.0, 'info': 'Av. Travel times',
                            'xmltag': 'traveltime', 'groupnames': ['edgedata'], 'is_average': True}),
            ('density',  {'name': 'Av. Densities', 'unit': 'veh/km', 'default': 0.0,
                          'info': 'Av. Density in vehicles of vehicles on this Edge/Lane', 'xmltag': 'density', 'groupnames': ['edgedata'], 'is_average': True}),
            ('waitingTime', {'name': 'Av. waits',  'unit': 's',     'default': 0.0, 'info': 'Av. Waiting times of vehicles on this Edge/Lane',
                             'xmltag': 'waitingTime', 'groupnames': ['edgedata'], 'is_average': True}),
            ('speed',    {'name': 'Av. speeds',   'unit': 'm/s',   'default': 0.0,
                          'info': 'Av. velocity of vehicles on this Edge/Lane', 'xmltag': 'speed', 'groupnames': ['edgedata'], 'is_average': True}),
            ('fuel_abs', {'name': 'Abs. Fuel',    'unit': 'ml',    'default': 0.0,
                          'info': 'Absolute fuel consumption of vehicles on this Edge/Lane', 'xmltag': 'fuel_abs', 'groupnames': ['edgeemissions']}),
            ('CO_abs',   {'name': 'Abs. CO',      'unit': 'mg',    'default': 0.0,
                          'info': 'Absolute CO emission of vehicles on this Edge/Lane', 'xmltag': 'CO_abs', 'groupnames': ['edgeemissions']}),
            ('CO2_abs',  {'name': 'Abs. CO2',     'unit': 'mg',    'default': 0.0,
                          'info': 'Absolute CO2 emission of vehicles on this Edge/Lane', 'xmltag': 'CO2_abs', 'groupnames': ['edgeemissions']}),
            ('NOx_abs',  {'name': 'Abs. NOx',     'unit': 'mg',    'default': 0.0,
                          'info': 'Absolute NOx emission of vehicles on this Edge/Lane', 'xmltag': 'NOx_abs', 'groupnames': ['edgeemissions']}),
            ('PMx_abs',  {'name': 'Abs. PMx',     'unit': 'mg',    'default': 0.0,
                          'info': 'Absolute PMx  emission (Particle matter, all sizes) of vehicles on this Edge/Lane', 'xmltag': 'PMx_abs', 'groupnames': ['edgeemissions']}),
            ('fuel_normed', {'name': 'Specific fuel',       'unit': 'l/km/h', 'default': 0.0,
                             'info': 'Absolute fuel consumption of vehicles on this Edge/Lane', 'xmltag': 'fuel_normed', 'groupnames': ['edgeemissions'], 'is_average': True}),
            ('CO_normed', {'name': 'Specific CO',           'unit': 'g/km/h', 'default': 0.0,
                           'info': 'Normalized CO emission of vehicles on this Edge/Lane', 'xmltag': 'CO_normed', 'groupnames': ['edgeemissions'], 'is_average': True}),
            ('CO2_normed', {'name': 'Specific CO2',         'unit': 'g/km/h', 'default': 0.0,
                            'info': 'Normalized CO2 emission of vehicles on this Edge/Lane', 'xmltag': 'CO2_normed', 'groupnames': ['edgeemissions'], 'is_average': True}),
            ('NOx_normed', {'name': 'Specific NOx',         'unit': 'g/km/h', 'default': 0.0,
                            'info': 'Normalized NOx emission of vehicles on this Edge/Lane', 'xmltag': 'NOx_normed', 'groupnames': ['edgeemissions'], 'is_average': True}),
            ('PMx_normed', {'name': 'Specific PMx',         'unit': 'g/km/h', 'default': 0.0,
                            'info': 'Normalized PMx emission of vehicles on this Edge/Lane', 'xmltag': 'PMx_normed', 'groupnames': ['edgeemissions'], 'is_average': True}),
            ('fuel_perVeh', {'name': 'Fuel per veh.',       'unit': 'ml/veh', 'default': 0.0,
                             'info': 'Absolute fuel consumption of vehicles on this Edge/Lane', 'xmltag': 'fuel_perVeh', 'groupnames': ['edgeemissions'], 'is_average': True}),
            ('CO_perVeh', {'name': 'CO per veh.',           'unit': 'mg/veh', 'default': 0.0,
                           'info': 'CO emission per vehicle on this Edge/Lane', 'xmltag': 'CO_perVeh', 'groupnames': ['edgeemissions'], 'is_average': True}),
            ('CO2_perVeh', {'name': 'CO2 per veh.',         'unit': 'mg/veh', 'default': 0.0,
                            'info': 'CO2 emission per vehicle on this Edge/Lane', 'xmltag': 'CO2_perVeh', 'groupnames': ['edgeemissions'], 'is_average': True}),
            ('NOx_perVeh', {'name': 'NOx per veh.',         'unit': 'mg/veh', 'default': 0.0,
                            'info': 'NOx emission per vehicle on this Edge/Lane', 'xmltag': 'NOx_perVeh', 'groupnames': ['edgeemissions'], 'is_average': True}),
            ('PMx_perVeh', {'name': 'PMx per veh.',         'unit': 'mg/veh', 'default': 0.0,
                            'info': 'PMx emission per vehicle on this Edge/Lane', 'xmltag': 'PMx_perVeh', 'groupnames': ['edgeemissions'], 'is_average': True}),
            ('noise',    {'name': 'Noise',         'unit': 'dB',   'default': 0.0,
                          'info': 'Noise of vehicles on this Edge/Lane', 'xmltag': 'noise', 'groupnames': ['edgenoise'], 'is_average': True}),
        ])

        for attrname, kwargs in attrinfos.iteritems():
            self.add_resultattr(attrname, **kwargs)

    def add_resultattr(self, attrname, **kwargs):

        # default cannot be kwarg
        default = kwargs['default']
        del kwargs['default']
        if kwargs.has_key('groupnames'):
            kwargs['groupnames'].append('results')
        else:
            kwargs['groupnames'] = ['results']

        self.add_col(am.ArrayConf(attrname, default, **kwargs))

    def import_edgedata(self, filepath):
        # print 'import_edgedata',filepath
        # print '  group',self.get_group('edgedata')
        #attrnames_data = ['entered','left','arrived','departed']
        #attrnames_averaged = ['traveltime','density','waitingTime','speed',]
        self.import_sumoxml(filepath, self.get_group('edgedata'))

    def import_edgenoise(self, filepath):
        # print 'import_edgedata',filepath
        self.import_sumoxml(filepath, self.get_group('edgenoise'))

    def import_edgeemissions(self, filepath):
        # print 'import_edgedata',filepath
        #attrnames_data = ['fuel_abs','CO_abs','CO2_abs','NOx_abs','PMx_abs']
        #attrnames_averaged = ['fuel_normed','CO_normed','CO2_normed',]
        self.import_sumoxml(filepath, self.get_group('edgeemissions'))

    def import_sumoxml(self, filepath, attrconfigs):
        element = 'edge'
        # print 'import_sumoxml',element
        #id_type = 'edge',
        #reader = 'interval',
        ids_sumo, results, interval = read_interval2(
            filepath, element, attrconfigs)
        # print '  ids_sumo',ids_sumo
        # print '  results.keys()',results.keys()
        # print '  results',results
        # create ids for all colums
        # if fileinfo['id_type']=='edge':

        # this procedure is necessary to create new result ids only
        # for edges that are not yet in the database
        ids_sumoedge = self.ids_edge.get_linktab().ids_sumo
        n = len(ids_sumo)
        # print '  n',n
        ind_range = np.arange(n, dtype=np.int32)
        ids = np.zeros(n, dtype=np.int32)
        for i in ind_range:
            id_edge = ids_sumoedge.get_id_from_index(ids_sumo[i])
            if self.ids_edge.has_index(id_edge):
                ids[i] = self.ids_edge.get_id_from_index(id_edge)
            else:
                ids[i] = self.add_row(ids_edge=id_edge)

        # ids = self.add_row()# here the ids_sumo can be strings too
        # elif fileinfo['id_type']=='trip':
        #    ids = self.tripresults.add_rows_keyrecycle(keys = ids_sumo)#
        # print '  ids=',ids

        for attrconfig in attrconfigs:

            attrname = attrconfig.attrname
            # print ' copy',attrname
            default = attrconfig.get_default()
            if type(default) in (types.IntType, types.LongType):
                conversion = 'i'  # int
                values_attr = np.zeros(n, int)
            elif type(default) in (types.FloatType, types.ComplexType):
                conversion = 'f'  # float
                values_attr = np.zeros(n, float)
            else:
                conversion = 's'  # str
                values_attr = np.zeros(n, obj)

            # this is a tricky way to read the data stored in
            # dictionarie into array tructures as used in results
            # problem is that not all dictionaries have all ids
            for i in ind_range:
                val = results[attrname].get(ids_sumo[i], default)

                if conversion == 'i':
                    val = int(val)
                else:
                    values_attr[i] = val
                # print '   attrname',attrname,conversion,val,type(val)
                values_attr[i] = val

            # print '  attrname',attrname
            # print '  ids',type(ids),ids
            # print '  values_attr',type(values_attr),values_attr
            attrconfig.set(ids, values_attr)


class Simresults(cm.BaseObjman):

    def __init__(self, ident='simresults', scenario=None,
                 name='Simulation results',
                 info='Results of SUMO simulation run.',
                 outfile_prefix='out',
                 **kwargs):

            # print 'Network.__init__',name,kwargs
        rootname = scenario.get_rootfilename()
        rootdirpath = scenario.get_workdirpath()

        self._init_objman(ident=ident, parent=scenario, name=name,
                          info=info, **kwargs)
        attrsman = self.set_attrsman(cm.Attrsman(self))

        self.edgeresults = attrsman.add(cm.ObjConf(
            Edgeresults(self, scenario.net.edges)))
        self.tripresults = attrsman.add(cm.ObjConf(Tripresults(
            self, scenario.demand.trips, scenario.net.edges)))

    def save(self, filepath=None, is_not_save_parent=True):
        if filepath == None:
            self.get_scenario().get_rootfilepath() + '.res.obj'
        cm.save_obj(self, filepath, is_not_save_parent=is_not_save_parent)

    def get_scenario(self):
        return self.parent


class IntervalAvReader2(handler.ContentHandler):

    """
    Reads edge or lane based intervals
    and returns time averaged values for each attribute name.

    """

    def __init__(self, element, attrsconfigs_cumulative, attrsconfigs_average):
        """
        element is "lane" or "edge" or "tripinfo"
        attrnames is a list of attribute names to read.
        """
        # print 'IntervalAvReader2'
        self._element = element
        self._attrsconfigs_cumulative = attrsconfigs_cumulative
        self._attrsconfigs_average = attrsconfigs_average
        self._time_begin = None
        self._time_end = None
        self._values = {}
        self._ids = []
        #self._n_values= {}
        self.n_inter = 0
        self.n_test = 0
        self.n_test2 = 0
        # TODO: if we knew here all ids then we
        # could create a numeric array per attribute
        # idea: pass ids as input arg
        for attrsconfig in attrsconfigs_cumulative + attrsconfigs_average:
            self._values[attrsconfig.attrname] = {}
            # print '  init',attrsconfig.attrname
            #self._n_values= {}

    def startElement(self, name, attrs):
        # if attrs.has_key('id'):
        # print '  parse',name,self._element,name == self._element, attrs['id']

        if name == 'interval':
            self._time_inter = int(
                float(attrs['end'])) - int(float(attrs['begin']))
            # here we just take the start and end time ofthe whole
            # measurement period
            if self._time_begin == None:  # take very first time only
                self._time_begin = int(float(attrs['begin']))
            self._time_end = int(float(attrs['end']))
            self.n_inter += 1

        if name == self._element:
            id = attrs['id']
            # print '--'
            if id not in self._ids:
                self._ids.append(id)

            # no arrival data availlable if trip has not been finished!!
            for attrsconfig in self._attrsconfigs_cumulative:
                xmltag = attrsconfig.xmltag
                attrname = attrsconfig.attrname

                if attrs.has_key(xmltag):
                    # print '
                    # attrname',attrname,attrs.has_key(attrname),'*'+attrs[attrname]+'*'
                    a = attrs[xmltag]

                    if a.strip() != '':
                        if self._values[attrname].has_key(id):
                            self._values[attrname][id] += float(a)
                        else:
                            self._values[attrname][id] = float(a)

                    # if (id in ('1/0to1/1','1/0to2/0')) & (attrname == 'entered'):
                    #    self.n_test+=int(attrs[attrname])
                    #    print '  -read ',id,attrname,attrs[attrname],self.n_test,self._values[attrname][id]
                    #
                    # if (id in ('0/0to1/0')) & (attrname == 'left'):
                    #    self.n_test2+=int(attrs[attrname])
                    # print '  +read
                    # ',id,attrname,attrs[attrname],self.n_test2,self._values[attrname][id]

            for attrsconfig in self._attrsconfigs_average:
                xmltag = attrsconfig.xmltag
                attrname = attrsconfig.attrname
                if attrs.has_key(xmltag):
                    n = float(self.n_inter)
                    a = attrs[xmltag]
                    if a.strip() != '':
                        if self._values[attrname].has_key(id):
                            self._values[attrname][id] = (
                                (n - 1) * self._values[attrname][id] + float(a)) / n
                            #self._values[attrname][id] += float(a)/self._time_inter
                            #self._n_values[attrname][id] += 1
                        else:
                            self._values[attrname][id] = float(a)
                            #self._values[attrname][id] = float(a)/self._time_inter
                            #self._n_values[attrname][id] = 1

    def get_data(self):
        return self._values

    def get_interval(self):
        return (self._time_begin, self._time_end)

    def get_ids(self):
        return self._ids


def read_interval2(filepath, element, attrsconfigs):
    # print 'read_interval2'
    attrsconfigs_cumulative = []
    attrsconfigs_average = []
    for attrsconfig in attrsconfigs:
        # print '  check',attrsconfig.attrname
        if hasattr(attrsconfig, 'is_average'):
            if attrsconfig.is_average:
                attrsconfigs_average.append(attrsconfig)
            else:
                attrsconfigs_cumulative.append(attrsconfig)
        else:
            attrsconfigs_cumulative.append(attrsconfig)

    reader = IntervalAvReader2(
        element, attrsconfigs_cumulative, attrsconfigs_average)
    #parser = make_parser()
    # parser.setContentHandler(reader)
    #fn = '"'+filepath+'"'
    # print 'read_interval >'+fn+'<'
    # print '     >'+filepath+'<'
    # parser.parse(filepath)
    parse(filepath, reader)
    return reader.get_ids(), reader.get_data(), reader.get_interval()
