from flask import Blueprint, request, jsonify
from extensions import db, bcrypt
from models import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from utils.return_error import error_response

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/register', methods=['POST'])
def register():
    # get data send by user
    data = request.get_json()

    # check email or username duplicate exists
    if User.query.filter_by(email=data['email']).first():
        return error_response(400, 'Email already exists')
    if User.query.filter_by(username=data['username']).first():
        return error_response(400, 'Username already exists')
    
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
    user = User.query.filter_by(username=data['username']).first()
    if not user:
        return error_response(401, 'Invalid email')
    if not bcrypt.check_password_hash(user.password_hash, data['password']):
        return error_response(401, 'Invalid password')
    
    # create jwt token
    token = create_access_token(identity=user.id)

    return jsonify({'access_token': token}), 200

@user_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():

    # get user from token
    user_id = get_jwt_identity()
    
    # get user from db
    user = User.query.get(user_id)

    if not user:
        return error_response(404, 'User not found')
    
    return jsonify({'username': user.username, 'email': user.email}), 200

@user_bp.route('/change_password', methods=['POST'])
@jwt_required()
def change_password():
    data = request.get_json()
    user_id = get_jwt_identity()

    # get user from db
    user = User.query.get(user_id)

    # check old password
    if not bcrypt.check_password_hash(user.password_hash, data['old_password']):
        return error_response(401, 'Invalid old password')
    
    # hash the new password
    hashed_password = bcrypt.generate_password_hash(data['new_password']).decode('utf-8')

    # update user password
    user.password_hash = hashed_password
    db.session.commit()

    return jsonify({'message': 'Password successfully updated'}), 200