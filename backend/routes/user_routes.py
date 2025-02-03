from flask import Blueprint, request, jsonify
from models import User
from extensions import db, bcrypt
from flask_jwt_extended import create_access_token
from utils.return_error import error_response
from models.schemas import UserSchema, LoginSchema
from marshmallow import ValidationError
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

user_bp = Blueprint('user_bp', __name__)

user_schema = UserSchema()
login_schema = LoginSchema()

limiter = Limiter(key_func=get_remote_address)

@user_bp.route('/register', methods=['POST'])
@limiter.limit("5/minute")
def register():
    try:
        # Récupérer les données brutes avant validation
        data = request.get_json()
        
        # Vérifier d'abord si l'email existe
        if User.query.filter_by(email=data['email']).first():
            return error_response('Email already exists', 400)
            
        # Vérifier si le nom d'utilisateur existe
        if User.query.filter_by(username=data['username']).first():
            return error_response('Username already exists', 400)
            
        # Ensuite seulement, valider les données avec Marshmallow
        validated_data = user_schema.load(data)
        
        # Créer un nouvel utilisateur
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            password_hash=bcrypt.generate_password_hash(validated_data['password']).decode('utf-8')
        )
        
        db.session.add(user)
        db.session.commit()

        return jsonify({
            'message': 'User successfully registered',
            'user': user_schema.dump(user)
        }), 201

    except ValidationError as err:
        return error_response(err.messages, 400)
    except Exception as e:
        db.session.rollback()
        return error_response(str(e), 400)

@user_bp.route('/login', methods=['POST'])
@limiter.limit("5/minute")
def login():
    try:
        data = request.get_json()
        user = User.query.filter_by(username=data['username']).first()

        if not user:
            return error_response('Invalid username or password', 401)

        if not bcrypt.check_password_hash(user.password_hash, data['password']):
            return error_response('Invalid username or password', 401)

        access_token = create_access_token(identity=str(user.id))
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token
        }), 200

    except Exception as e:
        return error_response(str(e), 401)