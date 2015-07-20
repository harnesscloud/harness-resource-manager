#!/usr/bin/env python

import sys
from optparse import OptionParser
import utils
import json
import random
import copy

import managers_view, resources_view, reservations_view, metrics_view
import uuid

from manager import HarnessResourceManager

try:
   with open("animals.txt") as f:
      default_name = "IRM-" + random.choice(f.readlines()).upper().replace(' ', '-')
except:
   default_name = "IRM-DUMMY"   
   

###################################################################### options
parser = OptionParser()
parser.add_option("-p", "--port", dest="PORT", default=50000+random.randint(100,10000),
                  help="IRM port", type="int")
                  
parser.add_option("-n", "--name", dest="NAME", default=default_name,
                  help="IRM name")

parser.add_option("-r", "--resources", dest="NRESOURCES", default=3, 
                  help="number of resources", type="int")
                  
parser.add_option("-t", "--type", dest="TYPE", default="Device",
                  help="resource type")
                  
parser.add_option("-f", "--fields", dest="NFIELDS", default=3,
                  help="number of fields", type="int")

parser.add_option("-m", "--minvalue", dest="MINVAL", default=2,
                  help="minimum value for field", type="int")
                  
parser.add_option("-M", "--maxvalue", dest="MAXVAL", default=10,
                  help="maximum value for field", type="int")
                                                      
                                                      
(options, _) = parser.parse_args()

######################################################### Resource View ####
resources = {}

class ResourcesView(resources_view.ResourcesView):
   def _get_resources(self):
       if resources == {}:
          for i in range(0, options.NRESOURCES):
             fields = {}
             for j in range(0, options.NFIELDS):
                fields[chr(97+j)]= random.randint(options.MINVAL, options.MAXVAL)
             resources["ID"+str(i+1)] = { "Type":  options.TYPE, "Attributes": fields}
       return { "Resources" : resources }          
       
   def _get_alloc_spec(self):
       spec = {"Types": {options.TYPE:{}}}
       
       for j in range(0, options.NFIELDS):
          spec["Types"][options.TYPE][chr(97+j)] = { "Description": "Something related to " + chr(97+j) + ".", "DataType": "int" }
       
       return spec
       
   def _calculate_capacity(self, resource, allocation, release):  
      fields = resource["Attributes"]
      for rel in release:
          for fld in rel["Attributes"]:
             if fld in fields:
                fields[fld] = fields[fld] + rel["Attributes"][fld]  
      
      feasible = True              
      for alloc in allocation:
          for fld in alloc["Attributes"]:
             if fld in fields:
                fields[fld] = fields[fld] - alloc["Attributes"][fld]
                if feasible and fields[fld] < 0:
                   feasible = False
      if feasible:
         return {'Resource': resource }
      else:
         return {}


######################################################### Reservation View #####
class ReservationsView(reservations_view.ReservationsView):
    def _create_reservation(self, alloc_req, constraints, monitor):
       '''
       resources= {'ID2': {'Attributes': {'a': 2, 'c': 2, 'b': 8}, 'Type': 'Device'}, 'ID3': {'Attributes': {'a': 8, 'c': 9, 'b': 8}, 'Type': 'Device'}, 'ID1': {'Attributes': {'a': 10, 'c': 7, 'b': 3}, 'Type': 'Device'}}
       
 
       alloc_req= [{u'Group': u'g0', u'Type': u'Machine', u'ID': u'resource ID', u'Attributes': {u'Cores': 8, u'Disk': 8192, u'Memory': 1024}}, {u'Group': u'g0', u'Type': u'Machine', u'ID': u'resource ID', u'Attributes': {u'Cores': 8, u'Disk': 8192, u'Memory': 1024}}, {u'Group': u'g0', u'Type': u'Machine', u'ID': u'resource ID', u'Attributes': {u'Cores': 8, u'Disk': 8192, u'Memory': 1024}}, {u'Group': u'g1', u'Type': u'Storage', u'ID': u'resource ID', u'Attributes': {u'Throughput': 8192, u'Capacity': 8192, u'AccessType': u'RANDOM'}}, {u'Group': u'g1', u'Type': u'Storage', u'ID': u'resource ID', u'Attributes': {u'Throughput': 8192, u'Capacity': 8192, u'AccessType': u'RANDOM'}}]      
       '''
       global resources
       cresources = copy.deepcopy(resources)
       uid = str(uuid.uuid1())
       res_info = []
       n = 0
       for req in alloc_req:
          if "ID" not in req:
             raise Exception("ID field missing!")
          if req["ID"] not in cresources:
             raise Exception("cannot find resource ID: " + req["ID"])
          id = req["ID"]
          resource = cresources[id]
          req_attrib = {"Attributes":req["Attributes"]}
          ret = ResourcesView()._calculate_capacity(resource, [req_attrib], [])
          if ret == {}:
             raise Exception("Cannot reserve request!")
          n = n + 1   
          res_info.append({"addr": "dmy://" + uid + "/" + str(n), "alloc": req_attrib, "ID": id})
       resources = cresources 
       
       reservations_view.ReservationsView.reservations[uid] = res_info

       return { "ReservationID": [uid] }  
       
    def _check_reservation(self, reservations):
       existing_reservations = reservations_view.ReservationsView.reservations
       instances = {}
       
       for res in reservations:          
          if res not in existing_reservations:
             raise Exception("cannot find reservation: " + res)
          addrs = map(lambda x: x['addr'], existing_reservations[res])
          instances[res] = { "Ready": "True", "Address": addrs } 
       
       return { "Instances" : instances }    
       
    def _release_reservation(self, reservations):
       global resources
       existing_reservations = reservations_view.ReservationsView.reservations
           
       cresources = copy.deepcopy(resources)
       for res in reservations:          
          if res not in existing_reservations:
             raise Exception("cannot find reservation: " + res)
          for inst in existing_reservations[res]:
             
             resource = cresources[inst["ID"]]
             ret = ResourcesView()._calculate_capacity(resource, [], [inst["alloc"]])
             if ret == {}:
                raise Exception("Cannot reserve request!")                   
          
       resources = cresources
       return { }               
              
             
################################################################ class IRM-Dummy    
irm_dummy_views=[ResourcesView, \
                 ReservationsView, \
                 metrics_view.MetricsView]
    
if __name__ == "__main__":    
    mgr = HarnessResourceManager(irm_dummy_views)
 
    
    out=utils.post({"Port":options.PORT, "Name":options.NAME} , 'registerManager', 56789) 
    if not isinstance(out, dict) or "result" not in out:
       print "Error: " + str(out) 
       exit(-1)
       
    mgr.run(options.PORT)    
    app = mgr.app()
