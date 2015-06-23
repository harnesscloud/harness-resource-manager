#!/usr/bin/env python

import sys
from optparse import OptionParser
import utils
import json
from random import randint

import manager, managers_view, resources_view, reservations_view, metrics_view

###################################################################### options
parser = OptionParser()
parser.add_option("-p", "--port", dest="PORT", default=55555,
                  help="IRM port", type="int")
                  
parser.add_option("-n", "--name", dest="NAME", default="IRM-DUMMY",
                  help="IRM name")

parser.add_option("-r", "--resources", dest="NRESOURCES", default=3, 
                  help="number of resources", type="int")
                  
parser.add_option("-t", "--type", dest="TYPE", default="Device",
                  help="resource type")
                  
parser.add_option("-f", "--fields", dest="NFIELDS", default=2,
                  help="number of fields", type="int")

parser.add_option("-m", "--minvalue", dest="MINVAL", default=0,
                  help="minimum value for field", type="int")
                  
parser.add_option("-M", "--maxvalue", dest="MAXVAL", default=10,
                  help="maximum value for field", type="int")
                                                      
                                                      
(options, _) = parser.parse_args()

######################################################### Resource View ####
class ResourcesView(resources_view.ResourcesView):
   def get_resources(self):
       resources = {}
       for i in range(0, options.NRESOURCES):
          fields = {}
          for j in range(0, options.NFIELDS):
             fields[chr(97+j)]= randint(options.MINVAL, options.MAXVAL)
          resources["ID"+str(i+1)] = { "Type":  options.TYPE, "Attributes": fields}
       return resources           
       
   def get_alloc_spec(self):
       spec = {"Types": {options.TYPE:{}}}
       
       for j in range(0, options.NFIELDS):
          spec["Types"][options.TYPE][chr(97+j)] = { "Description": "Something related to " + chr(97+j) + ".", "DataType": "int" }
       
       return spec
################################################################ class IRM-Dummy    
irm_dummy_views=[ResourcesView, \
                 reservations_view.ReservationsView, \
                 metrics_view.MetricsView]

class IRMDummy(manager.HarnessResourceManager):
    pass
    
if __name__ == "__main__":    
    mgr = IRMDummy(irm_dummy_views)
    data = json.dumps(\
		    {\
		    "Port":options.PORT,\
		    "Name":options.NAME\
		    })  
    
    out=utils.post(data, 'registerManager') 
    if not isinstance(out, dict) or "result" not in out:
       print "Error: " + str(out) 
       exit(-1)
       
    mgr.run(options.PORT)    
    app = mgr.app()
