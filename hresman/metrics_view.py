#!/usr/bin/env python

from flask.ext.classy import FlaskView, route
from flask import request
from utils import json_request, json_reply, json_error
import json

class MetricsView(FlaskView):
    base = 'metrics'
    version='v3'    
    route_base='/'
    
    ###############################################  create reservation ############ 
    def get_metrics(self, address, entry):       
       raise Exception("get metrics method has not been implemented!")
           
    @route('/getMetrics', methods=["POST"])         
    def get_metrics_post__(self):
       try:
           in_data = json_request()
        
           addrs = in_data['Address']
           entries = in_data['Entry']
           
           if not isinstance(addrs,list):
              raise Exception("Address field is not an array!")

           if not isinstance(entries, list):
              raise Exception("Entry field is not an array!")

           if len(addrs) <> len(entries):
              raise Exception("Address and Entry fields must have the same size!")
 
           if len(addrs) == 0:
              raise Exception("Address field cannot be empty!")
              
           return json_reply(map(self.get_metrics, addrs, entries)) 
                            
       except Exception as e:           
          return json_error(e)
          

    @route(version + '/' + base, methods=["GET"])         
    def get_metrics__(self):
       try:
          addr=request.args.get('addr')
          if addr is None:
             raise Exception("no address specified!")
          entry=request.args.get('entry')
          if entry is None:
             entry = 0  
          entry_int = int(entry)         
          return json_reply(self.get_metrics(addr, entry_int))    
               
       except Exception as e:           
          return json_error(e)

          
                            
