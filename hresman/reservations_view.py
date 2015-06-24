#!/usr/bin/env python

from flask.ext.classy import FlaskView, route
from flask import request
from utils import json_request, json_reply, json_error
import json

class ReservationsView(FlaskView):
    base = 'reservations'
    version='v3'    
    route_base='/'
    reservations = {}
    
    ###############################################  create reservation ############ 
    def _create_reservation(self, allocation, constraints, monitor):
       raise Exception("create reservation method has not been implemented!")
       
    @route('/createReservation', methods=["POST"])
    @route(version + '/' + base + "/create", methods=["POST"])     
    def create_reservation(self):
        try:
           in_data = json_request()
           allocation = in_data["Allocation"]
           
           if not isinstance(allocation, list):
              raise Exception("Allocation field is not an array!")
              
           if "Constraints" in in_data:
              constraints = in_data["Constraints"]
              if not isinstance(constraints, list):
                 raise Exception("Constraints field is not an array!")
           else:
              constraints = None
           
           if "Monitor" in in_data:
              monitor = in_data["Monitor"]
              if not isinstance(release, list):
                 raise Exception("Monitor field is not an array!")              
           else:
              monitor = None 

           self._create_reservation(allocation, constraints, monitor)
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

           self._check_reservation(reservations)
        except Exception as e:           
           return json_error(e)    
           
           
    ###############################################  release reservation ############   
    def _release_reservation(self, reservations):
       raise Exception("release reservation method has not been implemented!")
       
    @route('/releaseReservation', methods=["DELETE"])
    @route(version + '/' + base + "/release", methods=["DELETE"])     
    def release_reservation(self):
        try:
           in_data = json_request()
           reservations = in_data["ReservationID"]
           
           if not isinstance(reservations, list):
              raise Exception("ReservationID field is not an array!")
              
           if len(reservations) == 0:
               raise Exception("ReservationID field cannot be empty!")          

           self._release_reservation(reservations)
        except Exception as e:           
           return json_error(e)             
                      
    ###############################################  release all reservations ############   
    def _release_all_reservations(self):
       ReservationsView.reservations={}
       
    @route('/releaseAllReservations', methods=["DELETE"])
    @route(version + '/' + base + "/release-all", methods=["DELETE"])     
    def release_all_reservations(self):
        try:
           self._release_all_reservations()
        except Exception as e:           
           return json_error(e)             
                            
