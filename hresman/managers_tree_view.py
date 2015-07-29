#!/usr/bin/env python

from flask.ext.classy import FlaskView, route
from flask import request
from utils import json_request, json_reply, json_error
import json
import uuid
from managers_view import ManagersView
import sqlite3

############ initialise database for managers ######
conn = sqlite3.connect('crs.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS managers
             (key text unique, uuid text)''')
conn.commit()
conn.close()
###################################################

class ManagersTreeView(ManagersView): 
    managers = {} # idx -> item
    
    @staticmethod
    def gen_key(name, addr, port):
       return name + ':' + addr + ':' + str(port)
   
    ###############################################  register manager ##############
    def _registerManager(self, data):
        pass
   
    @route('/registerManager', methods=["POST"])
    @route(ManagersView.version + '/' + ManagersView.base, methods=["POST"])      
    def register_manager(self):
        try:
           in_data = json_request()
           print ":::>", in_data
           
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
           
           ################### check the database ####
           conn = sqlite3.connect('crs.db')
           c = conn.cursor()
           c.execute("SELECT * from managers where key = '%s'" % key)
           r = c.fetchone()

           if r == None:
              idx = str(uuid.uuid1())
              c.execute("INSERT INTO managers VALUES  ('%s', '%s')" % (key, idx))
              conn.commit()
           else:
              idx = r[1]            
           conn.close()             
           
           data = { 'Address': addr, 'Port': port, 'Name': name, 'ManagerID': idx }   
                
           ManagersTreeView.managers[idx] = data
           
           self._registerManager(data)
           
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
           if id in  ManagersTreeView.managers:
              return json_reply(ManagersTreeView.managers[id]) 
           
           raise Exception("invalid manager id: " + id)
               
        except Exception as e:           
           return json_error(e)       
    ###############################################  delete all managers ##############    
    @route(ManagersView.version + '/' + ManagersView.base, methods=["DELETE"])   
    def delete_managers(self):
        try:
           ManagersTreeView.managers = {}   
              
           return json_reply({})    
               
        except Exception as e:           
           return json_error(e)      
            
   ###############################################  delete manager X ##############     
    @route(ManagersView.version + '/' + ManagersView.base + '/<id>', methods=["DELETE"]) 
    def delete_manager(self, id):
        try:
           if id in  ManagersTreeView.managers:
              item = ManagersTreeView.managers[id]
              key = ManagersTreeView.gen_key(item['Name'], item['Address'], item['Port'])
              ManagersTreeView.managers.pop(id)
              return json_reply({}) 
           
           raise Exception("invalid manager index: " + id)
               
        except Exception as e:           
           return json_error(e)       
      
  
