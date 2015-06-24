from flask import json
import unittest
from hresman.manager import HarnessResourceManager, default_views_tree

class TestApiManagersView(unittest.TestCase):
  
    def create_app(self):
        app = HarnessResourceManager(default_views_tree).app 
        app.config['TESTING'] = True
        return app.test_client()   
        
    def register_manager(self, app, method, indata):    
        return json.loads(app.post(method, data=json.dumps(indata)).data)           
                
    # registering one manager    
    def test1(self):
        app = self.create_app()
        outdata = self.register_manager(app, '/registerManager', {'Address': '192.168.1.1', 'Port': '123', 'Name': 'IRM-DUMMY'})               
        assert "ManagerID" in outdata["result"]
    
    # registering one manager (using formal API) 
    def test2(self):
        app = self.create_app()
        outdata = self.register_manager(app, '/v3/managers', {'Address': '192.168.1.1', 'Port': '123', 'Name': 'IRM-DUMMY'})               
        assert "ManagerID" in outdata["result"]
            
        
    # testing idempotency
    def test3(self):
        app = self.create_app()
        outdata1 = self.register_manager(app, '/registerManager', {'Address': '192.168.1.1', 'Port': '123', 'Name': 'IRM-DUMMY'})   
        outdata2 = self.register_manager(app, '/registerManager', {'Address': '192.168.1.1', 'Port': '123', 'Name': 'IRM-DUMMY'})                     
        assert outdata1["result"]["ManagerID"] ==  outdata2["result"]["ManagerID"]   
   
    # registering two managers, deleting the first manager, deleting all managers
    def test4(self):
        app = self.create_app()
        outdata1 = self.register_manager(app, '/registerManager', {'Address': '192.168.1.1', 'Port': '123', 'Name': 'IRM-DUMMY'})   
        self.register_manager(app, '/registerManager', {'Address': '192.168.1.2', 'Port': '123', 'Name': 'IRM-DUMMY'})                     
        
        outdata2 = json.loads(app.get('/v3/managers').data)
        assert "result" in outdata2 and len(outdata2["result"]) == 2
        
        # remove the first manager
        app.delete('/v3/managers/'+outdata1["result"]["ManagerID"])
        
        # we should now have just one manager
        outdata3 = json.loads(app.get('/v3/managers').data)
        assert "result" in outdata3 and len(outdata3["result"]) == 1        
      
        # remove all managers
        app.delete('/v3/managers') 
        
        # we should not have any managers!
        outdata4 = json.loads(app.get('/v3/managers').data)
        assert "result" in outdata4 and len(outdata4["result"]) == 0         
 
    # should issue an error if we don't specify either Port or Name fields when registering the manager
    def test5(self):
        app = self.create_app()
        assert "error" in self.register_manager(app, '/registerManager', { 'Name': 'IRM-DUMMY'}) 
        assert "error" in self.register_manager(app, '/registerManager', { 'Port': 123})             
        assert not "error" in self.register_manager(app, '/registerManager', {'Port': 123, 'Name': 'IRM-DUMMY'})                      
        assert "error" in self.register_manager(app, '/registerManager', {})                         
        
                 
