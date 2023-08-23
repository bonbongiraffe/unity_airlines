#!/usr/bin/env python3
from models import User, Reservation, Flight
from flask_restful import Api, Resource
from flask import request, make_response, session, send_from_directory
import os
import ipdb
import string, random

from config import app, api, db

# helper functions
def id_query(class_name, id): # <-- queries db by id given class_name
    try:
        result = class_name.query.filter_by(id=id).first()
        if not result:
            return make_response({'error':'Instance not found'},404)
        return result
    except ValueError as v_error:
        return make_response({'error':[v_error]})

def conf_generator(): # <-- generates random string of characters of length 5, among uppercase letters and digits
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for i in range(5))

@app.route('/')
def index():
    return '<h1>Welcome to Unity Airlines!<h1>'

# restful routes
class Flights(Resource):
    def get(self):
        flightDicts = []
        for f in Flight.query.all():
            flightDicts.append({**f.to_dict(),'open_seats':f.open_seats})
        return make_response( flightDicts, 200)

class FlightsById(Resource):
    def get(self,id):
        flight = id_query(Flight,id)
        if hasattr(flight,'error'):
            return flight
        return make_response({**flight.to_dict(),'open_seats':flight.open_seats},200)

class Reservations(Resource):
    def post(self):
        data = request.get_json()
        flight = Flight.query.filter_by(origin=data['origin'], destination=data['destination']).first()
        if not flight:
            return make_response({'error':'Flight not found'},404)  
        if data["seat"] not in flight.open_seats:
            return make_response({'error':'Seat is already taken'},400)     
        try:
            new_reservation = Reservation(
                user_id = data["user_id"],
                flight_id = flight.id,
                seat = data["seat"],
                conf_number = conf_generator()
            )
            db.session.add(new_reservation)
            db.session.commit()
            return make_response(new_reservation.to_dict(),201)
        except ValueError as v_error:
            return make_response({'error':[v_error]},400)

class ReservationsById(Resource):
    def get(self,id):
        reservation = id_query(Reservation,id)
        if hasattr(reservation,'error'):
            return reservation
        print(reservation)
        return make_response(reservation.to_dict(),200)
    
    def delete(self,id):
        reservation = id_query(Reservation,id)
        if hasattr(reservation,'error'):
            return reservation
        db.session.delete(reservation)
        db.session.commit()
        return make_response({'message':'Reservation deleted'},204)
    
    def patch(self,id):
        # print(id)
        reservation = id_query(Reservation,id)
        if hasattr(reservation,'error'):
            return reservation
        try:
            data = request.get_json()
            # print(data,"from form")
            for attr in data:
                if attr not in ['origin','destination','id']:
                    # print(attr)
                    setattr(reservation, attr, data[attr])
            if 'origin' in data.keys():
                # print("about to search for flights")
                flight = Flight.query.filter_by(origin=data['origin'], destination=data['destination']).first()
                if not flight:
                    return make_response({'error':'Flight not found'},404) 
                # print(flight,"flight print")
                reservation.flight_id = flight.id 
            # print(reservation,"reservation print") 
            db.session.add(reservation)
            db.session.commit()
            return make_response(reservation.to_dict(),200)
        except ValueError as v_error:
            return make_response({'error':[v_error]},400)

api.add_resource(Flights,'/flights')
api.add_resource(FlightsById,'/flights/<int:id>')
api.add_resource(Reservations,'/reservations')
api.add_resource(ReservationsById,'/reservations/<int:id>')

# auth routes
@app.route('/login',methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        return make_response({'error':'Incorrect email or password'},400)
    if user.authenticate(data['password']):
        session['user_id'] = user.id
        return make_response(user.to_dict(),200)
    return make_response({'error':'Incorrect email or password'},400)

@app.route('/signup',methods=['POST'])
def signup():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user:
        return make_response({'error':'User with email exists already'},400)
    try:
        new_user = User(
            first_name = data['firstName'],
            last_name = data['lastName'],
            email = data['email'],
            password_hash = data['password']
        )
        db.session.add(new_user)
        db.session.commit()
        session['user_id'] = new_user.id
        return make_response(new_user.to_dict(),201)
    except ValueError as v_error:
        return make_response({'error':[v_error]},400)

@app.route('/authorized',methods=['GET'])
def authorized():
    try:
        user = User.query.filter_by(id=session.get('user_id')).first()
        return make_response(user.to_dict(),200)
    except:
        return make_response({'message':'Please login or signup'},404)

@app.route('/logout',methods=['DELETE'])
def logout():
    del session['user_id']
    return make_response({'message':'Logout successful'},204)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
    