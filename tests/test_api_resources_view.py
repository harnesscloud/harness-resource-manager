from flask import json
import unittest
from hresman.manager import HarnessResourceManager,default_views

class TestApiResourcesView(unittest.TestCase):
  
    def create_app(self):
        app = HarnessResourceManager(default_views).app 
        app.config['TESTING'] = True
        return app.test_client()   
               
                
    # should fail getResources (using formal API)
    def test1(self):
        app = self.create_app()
        outdata = json.loads(app.get('/v3/resources').data)             
        assert "error" in outdata and "implemented" in outdata["error"]["message"]            
        
    # should fail getResources
    def test2(self):
        app = self.create_app()
        outdata = json.loads(app.get('/getResources').data)             
        assert "error" in outdata and "implemented" in outdata["error"]["message"]          
        
    # should fail getResources
    def test3(self):
        app = self.create_app()
        outdata = json.loads(app.get('/getResources').data)             
        assert "error" in outdata and "implemented" in outdata["error"]["message"]            
