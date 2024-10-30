from flask import Blueprint, request, jsonify
from extensions import db, bcrypt
from models import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/register', methods=['POST'])
def register():
    # get data send by user
    data = request.get_json()

    # check email or username duplicate exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    # hash the password with bcrypt
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    # add user to db
    user = User(username=data['username'], email=data['email'], password_hash=hashed_password)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User successfully registered'}), 201

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    # check email then password
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        return jsonify({'error': 'Invalid email'}), 401
    if not bcrypt.check_password_hash(user.password_hash, data['password']):
        return jsonify({'error': 'Invalid password'}), 401
    
    # create jwt token
    token = create_access_token(identity=user.id)

    return jsonify({'token': token}), 200

@user_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():

    # get user from token
    user_id = get_jwt_identity()
    
    # get user from db
    user = User.query.get(user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({'username': user.username, 'email': user.email}), 200