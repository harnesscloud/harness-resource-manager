#!/usr/bin/env python

from flask.ext.classy import FlaskView, route
from flask import request
from utils import json_request, json_reply, json_error
import json

class ResourcesView(FlaskView):
    base = 'resources'
    version='v3'    
    route_base='/'
        
    ###############################################  get all resources ############## 
    def _get_resources(self):
       raise Exception("GET resources method has not been implemented!") 
       
    @route('/getResources', methods=["GET"])
    @route(version + '/' + base, methods=["GET"])   
    def get_resources(self):
        try:
           return json_reply(self._get_resources())   
        except Exception as e:           
           return json_error(e) 

    ################################  get allocation specification ##############  
    def _get_alloc_spec(self):
       raise Exception("GET allocation specification method has not been implemented!")
    
     
    @route('/getAllocSpec', methods=["GET"])
    @route(version + '/' + base + "/alloc-spec", methods=["GET"])   
    def get_alloc_spec(self):
        try:
           return json_reply(self._get_alloc_spec())
        except Exception as e:           
           return json_error(e)   
           
    ################################  compute capacity ##############  
    def _compute_capacity(self, resource, allocation, release):
       raise Exception("compute capacity method has not been implemented!")
      
    @route('/computeCapacity', methods=["POST"])
    @route(version + '/' + base + "/capacity", methods=["POST"])   
    def compute_capacity(self):
        try:
           in_data = json_request()
           resource = in_data["Resource"]
           if not isinstance(resource, dict):
              raise Exception("Resource field is not an object!")
           
           if "Allocation" in in_data:
              allocation = in_data["Allocation"]
              if not isinstance(allocation,list):
                 raise Exception("Allocation field is not an array!")
           else:
              allocation = None
           
           if "Release" in in_data:
              release = in_data["Release"]
              if not isinstance(release, list):
                 raise Exception("Release field is not an array!")              
           else:
              release = None 
           
           if allocation is None and release is None:
              raise Exception("missing Allocation or Release fields!")
           
           return json_reply(self._compute_capacity(resource, allocation, release))
                        
        except Exception as e:           
           return json_error(e)   

                  
