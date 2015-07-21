#!/usr/bin/env python

from flask import Flask
from flask.ext.classy import FlaskView, route
import managers_tree_view, resources_view, reservations_view, metrics_view, managers_view
import sys
import os

default_views=[managers_view.ManagersView,  \
               resources_view.ResourcesView, \
               reservations_view.ReservationsView, \
               metrics_view.MetricsView]

default_views_tree=[managers_tree_view.ManagersTreeView,  \
               resources_view.ResourcesView, \
               reservations_view.ReservationsView, \
               metrics_view.MetricsView]
               
class HarnessResourceManager:
   def __init__(self, views):
      self.app = Flask(__name__, \
                       template_folder=os.path.dirname(os.path.realpath(__name__))+'/templates', \
                       static_folder=os.path.dirname(os.path.realpath(__name__))+'/static')
      self.views = views
            
      for v in views:
         v.register(self.app)
       
      self.init()
      
   def init(self):
      pass
      
   def run(self, port, dbg=False):
      self.host = "0.0.0.0"
      self.port = port  
      
      print  
      self.app.run(host=self.host, port=self.port, debug=dbg)   
      

if __name__ == '__main__':
   mgr = HarnessResourceManager(default_views_tree) 
   mgr.run(56781)

