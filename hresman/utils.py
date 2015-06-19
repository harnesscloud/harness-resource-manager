from flask import request
import json
import traceback
import sys


def json_request():
   return json.loads(request.data) 
   
def json_reply(reply):   
   return json.dumps({"result": reply})  
   
def json_error(error, error_id=-1): 
   exc_type, exc_value, exc_traceback = sys.exc_info() # most recent (if any) by default
   traceback_details = {
                         'filename': exc_traceback.tb_frame.f_code.co_filename,
                         'lineno'  : exc_traceback.tb_lineno,
                         'name'    : exc_traceback.tb_frame.f_code.co_name,
                         'type'    : exc_type.__name__,
                         'message' : exc_value.message, # or see traceback._some_str()
                        }
   
 
   del(exc_type, exc_value, exc_traceback) # So we don't leave our local labels/objects dangling


   return json.dumps({"error": { "message": traceback_details["message"], "code": traceback_details["type"], "function":traceback_details["name"], "filename": traceback_details["filename"], "lineno":  traceback_details["lineno"] }})  
