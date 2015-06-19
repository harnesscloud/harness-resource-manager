#!/usr/bin/env python

from flask import Flask
from flask.ext.classy import FlaskView, route
import managers_view, resources_view, reservations_view
import sys

class HarnessResourceManager:
   def __init__(self, host, port, views):
      self.app = Flask(__name__)
      self.host = host
      self.port = port
      self.views = views
            
      for v in views:
         v.register(self.app)

      self.app.run(host=self.host, port=self.port, debug=False)   
      

views=[managers_view.ManagersView, resources_view.ResourcesView, reservations_view.ReservationsView]
x=HarnessResourceManager('localhost', 5000, views) 
      
#ParaView.register(app)

#if __name__ == '__main__':
#   app.run()
           

#class ResourceManager:
#   
#   def __init__(self, host, port):
#      self.host = host
#      self.port = port
#      
#      self.webserver = Flask(__name__)      
#      self.webserver.run(host=self.host, port=self.port, debug=False)     

#print __name__

