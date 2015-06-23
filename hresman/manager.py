#!/usr/bin/env python

from flask import Flask
from flask.ext.classy import FlaskView, route
import managers_view, resources_view, reservations_view, metrics_view
import sys

default_views=[managers_view.ManagersView,  \
               resources_view.ResourcesView, \
               reservations_view.ReservationsView, \
               metrics_view.MetricsView]
               
leaf_views=[resources_view.ResourcesView, \
            reservations_view.ReservationsView, \
            metrics_view.MetricsView]                            

class HarnessResourceManager:
   def __init__(self, views=default_views):
      self.app = Flask(__name__)
      self.views = views
            
      for v in views:
         v.register(self.app)
   
   def run(self, host, port, dbg=False):
      self.host = host
      self.port = port   
      self.app.run(host=self.host, port=self.port, debug=dbg)   
      

if __name__ == '__main__':
   mgr = HarnessResourceManager() 
   mgr.run('localhost', 5000)

