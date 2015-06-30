#!/usr/bin/env python

from flask.ext.classy import FlaskView, route
from flask import request
from utils import json_request, json_reply, json_error
import json
from resources_view import ResourcesView

class ReservationsView(FlaskView):
    base = 'reservations'
    version='v3'    
    route_base='/'
    reservations = {}
    
    ###############################################  create reservation ############ 
    def _create_reservation(self, alloc_req, constraints, monitor):
       raise Exception("create reservation method has not been implemented!")
       
    @route('/createReservation', methods=["POST"])
    @route(version + '/' + base, methods=["POST"])     
    def create_reservation(self):
        try:
           in_data = json_request()
           alloc_req = in_data["Allocation"]
           
           if not isinstance(alloc_req, list):
              raise Exception("Allocation field is not an array!")
              
           if "Constraints" in in_data:
              constraints = in_data["Constraints"]
              if not isinstance(constraints, list):
                 raise Exception("Constraints field is not an array!")
           else:
              constraints = []
           
           if "Monitor" in in_data:
              monitor = in_data["Monitor"]
              if not isinstance(monitor, dict):
                 raise Exception("Monitor field is not an object!")              
           else:
              monitor = {} 
           
           ResourcesView().request_resources()
           return json_reply(self._create_reservation(alloc_req, constraints, monitor))
        except Exception as e:           
           return json_error(e)               
    
    ###############################################  check reservation ############   
    def _check_reservation(self, reservations):
       raise Exception("check reservation method has not been implemented!")
       
    @route('/checkReservation', methods=["POST"])
    @route(version + '/' + base + "/check", methods=["POST"])     
    def check_reservation(self):
        try:
           in_data = json_request()
           reservations = in_data["ReservationID"]
           
           if not isinstance(reservations, list):
              raise Exception("ReservationID field is not an array!")
              
           if len(reservations) == 0:
               raise Exception("ReservationID field cannot be empty!")          

           return json_reply(self._check_reservation(reservations))
        except Exception as e:           
           return json_error(e)    
           
           
    ###############################################  release reservation ############   
    def _release_reservation(self, reservations):
       raise Exception("release reservation method has not been implemented!")
       
    @route('/releaseReservation', methods=["DELETE"])
    @route(version + '/' + base, methods=["DELETE"])     
    def release_reservation(self):
        try:
           in_data = json_request()
           reservations = in_data["ReservationID"]
           
           if not isinstance(reservations, list):
              raise Exception("ReservationID field is not an array!")
              
           if len(reservations) == 0:
               raise Exception("ReservationID field cannot be empty!")          

           return json_reply(self._release_reservation(reservations))
        except Exception as e:           
           return json_error(e)             
                      
    ###############################################  release all reservations ############   
    def _release_all_reservations(self):
       ReservationsView.reservations={}
       return {}
       
    @route('/releaseAllReservations', methods=["DELETE"])
    @route(version + '/' + base + "/all", methods=["DELETE"])     
    def release_all_reservations(self):
        try:
           return json_reply(self._release_all_reservations())
        except Exception as e:           
           return json_error(e)             
                            
