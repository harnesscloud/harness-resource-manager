#!/usr/bin/env python

from flask.ext.classy import FlaskView, route
from flask import request
from utils import json_request, json_reply, json_error
import json
import uuid
from managers_view import ManagersView

class ManagersTreeView(ManagersView): 
    managers = {} # idx -> item
    managers_idx = {} # key -> idx  
    
    @staticmethod
    def gen_key(name, addr, port):
       return name + ':' + addr + ':' + str(port)
    
    ###############################################  register manager ##############        
    @route('/registerManager', methods=["POST"])
    @route(ManagersView.version + '/' + ManagersView.base, methods=["POST"])      
    def register_manager(self):
        try:
           in_data = json_request()
           
           if 'Address' in in_data:               
              addr = in_data['Address']
           else:
              addr = request.remote_addr
           
           # when testing (no requests), addr is None. We assume localhost   
           if addr is None:
              addr = "127.0.0.1"
              
           port = in_data['Port']
           name = in_data['Name']
           
           key = ManagersTreeView.gen_key(name, addr, port)
           
           if key in ManagersTreeView.managers_idx:
              idx = ManagersTreeView.managers_idx[key]
           else:
              idx = uuid.uuid1()
              ManagersTreeView.managers_idx[key] = idx
                   
           ManagersTreeView.managers[idx] = { 'Address': addr, 'Port': port, 'Name': name, 'ManagerID': str(idx) } 
           
           return json_reply(ManagersTreeView.managers[idx])    
               
        except Exception as e:           
           return json_error(e)

    ###############################################  get all managers ##############    
    @route(ManagersView.version + '/' + ManagersView.base, methods=["GET"])   
    def get_managers(self):
        try:
           mgrs = []
           
           for i in ManagersTreeView.managers:
              mgrs.append(ManagersTreeView.managers[i])
              
           return json_reply(mgrs)    
               
        except Exception as e:           
           return json_error(e)      
            
   ###############################################  get manager X ##############      
    @route(ManagersView.version + '/' + ManagersView.base + '/<id>', methods=["GET"])   
    def get_manager(self, id):
        try:
           i = uuid.UUID(id)
           if i in  ManagersTreeView.managers:
              return json_reply(ManagersTreeView.managers[i]) 
           
           raise Exception("invalid manager id: " + id)
               
        except Exception as e:           
           return json_error(e)       
    ###############################################  delete all managers ##############    
    @route(ManagersView.version + '/' + ManagersView.base, methods=["DELETE"])   
    def delete_managers(self):
        try:
           ManagersTreeView.managers = {} 
           ManagersTreeView.managers_idx = {}   
              
           return json_reply({})    
               
        except Exception as e:           
           return json_error(e)      
            
   ###############################################  delete manager X ##############      
    @route(ManagersView.version + '/' + ManagersView.base + '/<id>', methods=["DELETE"])   
    def delete_manager(self, id):
        try:
           i = uuid.UUID(id)
           if i in  ManagersTreeView.managers:
              item = ManagersTreeView.managers[i]
              key = ManagersTreeView.gen_key(item['Name'], item['Address'], item['Port'])
              ManagersTreeView.managers.pop(i)
              ManagersTreeView.managers_idx.pop(key)
              return json_reply({}) 
           
           raise Exception("invalid manager index: " + id)
               
        except Exception as e:           
           return json_error(e)       
      
  
