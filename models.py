from flask_sqlalchemy import SQLAlchemy
import uuid
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin): 
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='customer')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'role': self.role
        }

class Customer(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone': self.phone,
            'email': self.email
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(first_name=data['first_name'], last_name=data['last_name'], phone=data['phone'], email=data['email'])
    

class Vehicle(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(50), nullable=False)
    customer_id = db.Column(db.String(36), db.ForeignKey('customer.id'), nullable=False)

    customer = db.relationship('Customer', backref='vehicles')

    def to_dict(self):
        return {
            'id': self.id,
            'make': self.make,
            'model': self.model,
            'year': self.year,
            'color': self.color,
            'customer': self.customer.to_dict()
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(make=data['make'], model=data['model'], year=data['year'], color=data['color'])
    
class Employee(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    hourly_wage = db.Column(db.Float, nullable=False)
    employee_type = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'hourly_wage': self.hourly_wage,
            'employee_type': self.employee_type
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(first_name=data['first_name'], last_name=data['last_name'], email=data['email'], phone=data['phone'], hourly_wage=data['hourly_wage'], employee_type=data['employee_type'])
    
class Repair(db.Model):
    id = db.Column(db.String(30), primary_key=True, default=lambda: str(uuid.uuid4()))
    description = db.Column(db.String(255), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    vehicle_id = db.Column(db.String(36), db.ForeignKey('vehicle.id'), nullable=False)

    vehhicle = db.relationship('Vehicle', backref='repairs')

    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description,
            'date': self.date,
            'status': self.status,
            'vehicle': self.vehhicle.to_dict()
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(description=data['description'], date=data['date'], status=data.get('status', 'scheduled'), vehicle_id=data['vehicle_id'])