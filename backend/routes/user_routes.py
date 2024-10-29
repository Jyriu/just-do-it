from flask import Blueprint, request, jsonify
from extensions import db, bcrypt
from models import User

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