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
    
    managers = {} # idx -> item
    managers_idx = {} # key -> idx  
    
    @staticmethod
    def gen_key(name, addr, port):
       return name + ':' + addr + ':' + str(port)
    
    ###############################################  register manager ##############        
    @route('/registerManager', methods=["POST"])
    @route(version + '/' + base, methods=["POST"])      
    def register_manager(self):
        try:
           in_data = json_request()
           
           if 'Address' in in_data:               
              addr = in_data['Address']
           else:
              addr = request.remote_addr
              
           port = in_data['Port']
           name = in_data['Name']
           
           key = ManagersView.gen_key(name, addr, port)
           
           if key in ManagersView.managers_idx:
              idx = ManagersView.managers_idx[key]
           else:
              idx = uuid.uuid1()
              ManagersView.managers_idx[key] = idx
                   
           ManagersView.managers[idx] = { 'Address': addr, 'Port': port, 'Name': name, 'ManagerID': str(idx) } 
           
           return json_reply(ManagersView.managers[idx])    
               
        except Exception as e:           
           return json_error(e)

    ###############################################  get all managers ##############    
    @route(version + '/' + base, methods=["GET"])   
    def get_managers(self):
        try:
           mgrs = []
           
           for i in ManagersView.managers:
              mgrs.append(ManagersView.managers[i])
              
           return json_reply(mgrs)    
               
        except Exception as e:           
           return json_error(e)      
            
   ###############################################  get manager X ##############      
    @route(version + '/' + base + '/<id>', methods=["GET"])   
    def get_manager(self, id):
        try:
           i = uuid.UUID(id)
           if i in  ManagersView.managers:
              return json_reply(ManagersView.managers[i]) 
           
           raise Exception("invalid manager id: " + id)
               
        except Exception as e:           
           return json_error(e)       
    ###############################################  delete all managers ##############    
    @route(version + '/' + base, methods=["DELETE"])   
    def delete_managers(self):
        try:
           ManagersView.managers = {} 
           ManagersView.managers_idx = {}   
              
           return json_reply({})    
               
        except Exception as e:           
           return json_error(e)      
            
   ###############################################  delete manager X ##############      
    @route(version + '/' + base + '/<id>', methods=["DELETE"])   
    def delete_manager(self, id):
        try:
           i = uuid.UUID(id)
           if i in  ManagersView.managers:
              item = ManagersView.managers[i]
              key = ManagersView.gen_key(item['Name'], item['Address'], item['Port'])
              ManagersView.managers.pop(i)
              ManagersView.managers_idx.pop(key)
              return json_reply({}) 
           
           raise Exception("invalid manager index: " + id)
               
        except Exception as e:           
           return json_error(e)       
      
  
