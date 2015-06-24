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
    def _get_metrics(self, reservID, address, entry):       
       raise Exception("get metrics method has not been implemented!")
    
           
    @route('/getMetrics', methods=["POST"])         
    def get_metrics_post(self):
       try:
          in_data = json_request()
          
          reservID = in_data['ReservationID']           
          addr = in_data['Address']
          if 'Entry' not in in_data:
             entry = 0
          else:
             entry = in_data['Entry']
            
          return json_reply(self._get_metrics(reservID, addr, entry)) 
                            
       except Exception as e:           
          return json_error(e)
          

    @route(version + '/' + base, methods=["GET"])         
    def get_metrics_get(self):
       try:
          reservID=request.args.get('id')
          if reservID is None:
             raise Exception("no id specified!")          
          addr=request.args.get('addr')
          if addr is None:
             raise Exception("no address specified!")
          entry=request.args.get('entry')
          if entry is None:
             entry = 0  
          entry_int = int(entry)         
          return json_reply(self._get_metrics(reservID, addr, entry_int))    
               
       except Exception as e:           
          return json_error(e)

          
                            
