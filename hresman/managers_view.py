#!/usr/bin/env python

from flask.ext.classy import FlaskView, route
from flask import request
from utils import json_request, json_reply, json_error
import json
import uuid

class ManagersView(FlaskView):
    base = 'managers'
    version='v3'    
    route_base='/'
    
    ###############################################  register manager ##############        
    @route('/registerManager', methods=["POST"])
    @route(version + '/' + base, methods=["POST"])      
    def register_manager(self):
        try:
           raise Exception("register manager method has not been implemented!")
        except Exception as e:
           return json_error(e)

    ###############################################  get all managers ##############    
    @route(version + '/' + base, methods=["GET"])   
    def get_managers(self): 
        try:
           raise Exception("get all managers method has not been implemented!")
        except Exception as e:
           return json_error(e)       
            
   ###############################################  get manager X ##############      
    @route(version + '/' + base + '/<id>', methods=["GET"])   
    def get_manager(self, id):
        try:
           raise Exception("get manager method has not been implemented!")
        except Exception as e:
           return json_error(e)     
      
    ###############################################  delete all managers ##############    
    @route(version + '/' + base, methods=["DELETE"])   
    def delete_managers(self):
        try:
           raise Exception("delete all managers method has not been implemented!")
        except Exception as e:
           return json_error(e)              
   ###############################################  delete manager X ##############      
    @route(version + '/' + base + '/<id>', methods=["DELETE"])   
    def delete_manager(self, id):
        try:
           raise Exception("delete manager method has not been implemented!")
        except Exception as e:
           return json_error(e)       

ManagersView._class = ManagersView 
