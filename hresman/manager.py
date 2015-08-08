#!/usr/bin/env python

from flask import Flask
from flask.ext.classy import FlaskView, route
import sys
import os

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
      


