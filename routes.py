from flask import Blueprint, request, jsonify
from models import db, Customer, Vehicle, Employee, Repair, User
from datetime import datetime
from flask_login import login_user, logout_user, login_required, current_user
from flask_bcrypt import generate_password_hash
from flask_jwt_extended import create_access_token

bp = Blueprint('api', __name__)

@bp.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password required.'}), 400
    
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered.'}), 400
    
    hashed_password = generate_password_hash(password).decode('utf-8')

    new_user = User(email=email, password_hash=hashed_password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully.'}), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not data or not all(key in data for key in ('email', 'password')):
        return jsonify({'error': 'Missing email or password.'})
    
    user = User.query.filter_by(email=data['email']).first()
 
    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id)
        login_user(user)
        return jsonify({'access_token': access_token, 'user': user.to_dict()}), 200
    else:
        return jsonify({'error': 'Invalid Credentials.'}), 401

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logut successful.'})

@bp.route('/protected')
@login_required
def protected():
    return jsonify({'message': 'You are logged in as{}'.format(current_user.email)})

@bp.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200


@bp.route('/customers', methods=['POST'])
def create_customer():
    data = request.json
    if not data or not all(key in data for key in('first_name', 'last_name', 'phone', 'email')):
        return jsonify({'error': 'Missing data'}, 400)
    
    # Check if the email already exisists in the database
    existing_customer = Customer.query.filter_by(email=data['email']).first()
    if existing_customer:
        return jsonify({'error': 'Email already exists'}), 400
    
    customer = Customer.from_dict(data)
    db.session.add(customer)
    db.session.commit()

    return jsonify(customer.to_dict()), 201

@bp.route('/customers', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    return jsonify([customer.to_dict() for customer in customers]), 200

@bp.route('/vehicles', methods=['POST'])
def create_vehicle():
    data = request.json
    if not data or not all(key in data for key in ('make', 'model', 'year', 'color', 'customer_email')):
        return jsonify({'error': 'Missing data'}, 400)
    
    customer = Customer.query.filter_by(email=data['customer_email']).first()
    if not customer:
        return jsonify({'error': 'Customer Email Not Found.'}, 404)
    
    vehicle = Vehicle.from_dict(data)
    vehicle.customer_id = customer.id
    db.session.add(vehicle)
    db.session.commit()

    return jsonify(vehicle.to_dict()), 201

@bp.route('/vehicles', methods=['GET'])
def get_vehicles():
    vehicles = Vehicle.query.all()
    return jsonify([vehicle.to_dict() for vehicle in vehicles]), 200

@bp.route('/vehicles/<customer_email>', methods=['GET'])
def get_customer_vehiclces(customer_email):
    customer = Customer.query.filter_by(email=customer_email).first()
    if not customer:
        return jsonify({'error': 'Customer not found.'}), 404
    
    vehicles = Vehicle.query.filter_by(customer_id=customer.id).all()
    return jsonify([vehicle.to_dict() for vehicle in vehicles]), 200

@bp.route('/employees', methods=['POST'])
def create_employee():
    data = request.json
    if not data or not all(key in data for key in ('first_name', 'last_name', 'email', 'phone', 'hourly_wage', 'employee_type')):
        return jsonify({'error': 'Missing data'}), 400
    
    # check if email already exists in the database
    existing_employee = Employee.query.filter_by(email=data['email']).first()
    if existing_employee:
        return jsonify({'error': 'Email already exisists.'}), 400
    
    employeee = Employee.from_dict(data)
    db.session.add(employeee)
    db.session.commit()

    return jsonify(employeee.to_dict()), 201

@bp.route('/employees', methods=['GET'])
def get_all_employees():
    employees = Employee.query.all()
    return jsonify([employee.to_dict() for employee in employees]), 200

@bp.route('/employees/<string:email>', methods=['GET'])
def get_employee_by_email(email):
    employee = Employee.query.filter_by(email=email).first()
    if employee:
        return jsonify(employee.to_dict()), 200
    else:
        return jsonify({'error': 'Employee nof found.'}), 404

@bp.route('/repairs', methods=['POST'])
def create_repair():
    data = request.json
    if not data or not all(key in data for key in ('description', 'date', 'vehicle_id')):
        return jsonify({'error': 'Missing data'}), 400
    
    # Convert the date from string to date object
    try:
        data['date'] = datetime.strptime(data['date'], '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date formate. Use YYYY-MM-DD'}), 400
    
    repair = Repair.from_dict(data)
    db.session.add(repair)
    db.session.commit()

    return jsonify(repair.to_dict()), 201

@bp.route('/repairs', methods=['GET'])
def get_repairs():
    repairs = Repair.query.all()
    return jsonify([repair.to_dict() for repair in repairs]), 200

@bp.route('/repairs/<string:repair_id>/status', methods=['PATCH'])
def update_repair_status(repair_id):
    data = request.json
    if not data or 'status' not in data:
        return jsonify({'error': 'Missing status field.'}), 400
    
    repair = Repair.query.get(repair_id)
    if not repair:
        return jsonify({'error': 'Repair not found'}), 404
    
    repair.status = data['status']
    db.session.commit()

    return jsonify(repair.to_dict()), 200

@bp.route('/repairs/vehicle/<string:vehicle_id>', methods=['GET'])
def get_repairs_by_vehicle(vehicle_id):
    repairs = Repair.query.filter_by(vehicle_id=vehicle_id).all()
    if not repairs:
        return jsonify({'error': 'No repairs found for this vehicle'}), 404
    
    return jsonify([repair.to_dict() for repair in repairs]), 200

@bp.route('/repairs/in-shop/count', methods=['GET'])
def count_in_shop_repairs():
    in_shop_repairs_count = Repair.query.filter_by(status='in-shop').count()
    return jsonify({'in_shop_repairs_count': in_shop_repairs_count}), 200