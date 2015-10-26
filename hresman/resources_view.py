#!/usr/bin/env python

from flask.ext.classy import FlaskView, route
from flask import request
from utils import json_request, json_reply, json_error, get
from managers_tree_view import ManagersTreeView
import requests
import copy
import json
import threading

class ResourcesView(FlaskView):
    base = 'resources'
    version='v3'    
    route_base='/'
    
    resources = {}    
    resource_constraints = {}
        
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
    def _calculate_capacity(self, resource, allocation, release):
       raise Exception("compute capacity method has not been implemented!")
      
    @route('/calculateCapacity', methods=["POST"])
    @route(version + '/' + base + "/calc-capacity", methods=["POST"])   
    def calculate_capacity(self):
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
              allocation = {}
           
           if "Release" in in_data:
              release = in_data["Release"]
              if not isinstance(release, list):
                 raise Exception("Release field is not an array!")              
           else:
              release = {} 
                      
           return json_reply(self._calculate_capacity(resource, allocation, release))
                        
        except Exception as e:           
           return json_error(e)   

    ################################ request resources from a resource manager ##############
    ### This needs to leave!
    @route(version + '/' + base + '/<id>/request', methods=["GET"])
    def request_resources_id(self, id):
       try:
          if not id in ManagersTreeView.managers:
             raise Exception("cannot find manager: " + id)
          data = ManagersTreeView.managers[id]

          try:  
             print "Trying out getting resources!"
             out = get("getResources", data["Port"], data["Address"])
             print "Done!"

             if "result" in out:
                 ResourcesView.resources[data["ManagerID"]] = out["result"]["Resources"]
                 if "Constraints" in out["result"]:
                    ResourcesView.resource_constraints[data["ManagerID"]] = out["result"]["Constraints"]   
          except requests.exceptions.ConnectionError:
             ManagersTreeView._class().delete_manager(data["ManagerID"])
             return json_error(Exception)   
                                  
          except Exception as e:
             return json_error(e)
          return json_reply({})
       except Exception as e:
          return json_error(e)

    ################################ request resources from all IRMs ############
    @route(version + '/' + base + '/request', methods=["GET"])
    def request_resources(self):
       try:
          managers = copy.copy(ManagersTreeView.managers)
          for id in managers:          
             self.request_resources_id(id)
          return json_reply({})
       except Exception as e:
          return json_error(e)
          
ResourcesView._class = ResourcesView               
