from flask import Blueprint, request, jsonify
from helpers import token_required
from models import db, User, Car, Instrument, car_schema, cars_schema, instrument_schema, instruments_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'yee': 'haw'}

@api.route('/cars', methods = ['POST'])
@token_required
def create_car(current_user_token):
    instrumentid = request.form.get('instrumentid')
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    instrumentname = request.json['instrumentname']
    instrumentmodel = request.json['instrumentmodel']
    instrumentbrand = request.json['instrumentbrand']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')
    print(user_token)
    print(current_user_token)

    instrument = Instrument(instrumentid, name, description, price, instrumentname, instrumentmodel, instrumentbrand, user_token = user_token)

    db.session.add(instrument)
    db.session.commit()

    response = instrument_schema.dump(instrument)
    return jsonify(response)

@api.route('/cars', methods = ['GET'])
@token_required
def get_instrument(current_user_token):
    owner = current_user_token.token
    instruments = Instrument.query.filter_by(user_token = owner).all()
    response = instruments_schema.dump(instruments)
    return jsonify(response)

@api.route('/cars/<id>', methods = ['GET'])
@token_required
def get_instruments_two(current_user_token, id):
    owner = current_user_token.token
    if owner == current_user_token.token:
        instrument = Instrument.query.get(id)
        response = instrument_schema.dump(instrument)
        return jsonify(response)
    else:
        return jsonify({"message": "Valid Token Required"}),401

# UPDATE endpoint
# @api.route('/cars/<id>', methods = ['POST','PUT'])
# @token_required
# def update_car(current_user_token,id):
#     car = Car.query.get(id) 
#     car.name = request.json['name']
#     car.description = request.json['description']
#     car.price = request.json['price']
#     car.engine_size = request.json['engine_size']
#     car.transmission = request.json['transmission']
#     car.max_speed = request.json['max_speed']
#     car.dimensions = request.json['dimensions']
#     car.weight = request.json['weight']
#     car.cost_of_prod = request.json['cost_of_prod']
#     car.gas_mileage = request.json['gas_mileage']
#     car.user_token = current_user_token.token

#     db.session.commit()
#     response = car_schema.dump(car)
#     return jsonify(response)


# DELETE car ENDPOINT
@api.route('/cars/<id>', methods = ['DELETE'])
@token_required
def delete_car(current_user_token, id):
    car = Car.query.get(id)
    db.session.delete(car)
    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)