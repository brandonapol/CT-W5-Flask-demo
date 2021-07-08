# imports 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid 
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_login import LoginManager
from flask_marshmallow import Marshmallow 
import secrets

# set variables for class instantiation
login_manager = LoginManager()
ma = Marshmallow()
db = SQLAlchemy()



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# Creating a database for users
class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String(150), nullable=True, default='')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = True, default = '')
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default = '', unique = True )
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __init__(self, email, first_name='', last_name='', password='', token='', g_auth_verify=False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_token(self, length):
        return secrets.token_hex()

    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f'User {self.email} has been added to the database'

# A database for cars
class Car(db.Model):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(200), nullable = True)
    price = db.Column(db.Numeric(precision=10,scale=2))
    engine_size = db.Column(db.String(150), nullable = True)
    transmission = db.Column(db.String(100), nullable = True)
    max_speed = db.Column(db.String(100))
    dimensions = db.Column(db.String(100))
    weight = db.Column(db.String(50))
    cost_of_prod = db.Column(db.Numeric(precision=10, scale=2))
    gas_mileage = db.Column(db.String(150))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self,name,description,price, engine_size,transmission,max_speed,dimensions, weight,cost_of_prod,gas_mileage,user_token, id = ''):
        self.id = self.set_id()
        self.name = name
        self.description = description
        self.price = price
        self.engine_size = engine_size
        self.transmission = transmission
        self.max_speed = max_speed
        self.dimensions = dimensions
        self.weight = weight
        self.cost_of_prod = cost_of_prod
        self.gas_mileage = gas_mileage
        self.user_token = user_token


    def __repr__(self):
        return f'The following vehicle has been added to the collection: {self.name}'

    def set_id(self):
        return (secrets.token_urlsafe())

class Instrument(db.Model):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(200), nullable = True)
    price = db.Column(db.Numeric(precision=10,scale=2))
    instrumentname = db.Column(db.String(150), nullable = True)
    instrumentbrand = db.Column(db.String(150), nullable = True)
    instrumentmodel = db.Column(db.String(150), nullable = True)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, name, description, price, instrumentname, instrumentbrand, instrumentmodel, user_token, id=''):
        self.id = self.set_id()
        self.name = name
        self.description = description
        self.price = price
        self.instrumentname = instrumentname
        self.instrumentbrand = instrumentbrand
        self.instrumentmodel = instrumentmodel
        self.user_token = user_token
    
    def __repr__(self):
        return f'The following instrument has been added to the collection: {self.name}'

    def set_id(self):
        return (secrets.token_urlsafe())

# Creation of API Schema via the Marshmallow object 
class CarSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name','description', 'price', 'engine_size', 'transmission', 'max_speed', 'dimensions', 'weight', 'cost_of_prod', 'gas_mileage']

car_schema = CarSchema()
cars_schema = CarSchema(many=True)

class InstrumentSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name','description', 'price', 'instrumentname', 'instrumentbrand', 'instrumentmodel']

instrument_schema = InstrumentSchema()
instruments_schema = InstrumentSchema(many=True)
