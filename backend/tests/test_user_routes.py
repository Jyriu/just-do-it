import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import create_access_token
import sys
import os
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from routes.user_routes import user_bp  # importe le blueprint des routes utilisateur
from extensions import db, bcrypt
from models import User

# Configurer une application Flask pour les tests
@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Utiliser une DB en mémoire pour les tests
    app.config['SECRET_KEY'] = 'test_secret'
    app.config['JWT_SECRET_KEY'] = 'jwt_secret'
    db.init_app(app)
    bcrypt.init_app(app)
    app.register_blueprint(user_bp)

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture

def client(app):
    return app.test_client()

@pytest.fixture
def create_user():
    def _create_user(username, email, password):
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, email=email, password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()
        return user
    return _create_user

def test_register_success(client):
    response = client.post('/register', json={
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'password123'
    })
    assert response.status_code == 201
    assert response.get_json()['message'] == 'User successfully registered'

def test_register_duplicate_email(client, create_user):
    create_user('testuser', 'testuser@example.com', 'password123')
    response = client.post('/register', json={
        'username': 'testuser2',
        'email': 'testuser@example.com',
        'password': 'password123'
    })
    assert response.status_code == 400
    assert response.get_json()['error'] == 'Email already exists'

def test_register_duplicate_username(client, create_user):
    create_user('testuser', 'testuser@example.com', 'password123')
    response = client.post('/register', json={
        'username': 'testuser',
        'email': 'newemail@example.com',
        'password': 'password123'
    })
    assert response.status_code == 400
    assert response.get_json()['error'] == 'Username already exists'

def test_login_success(client, create_user):
    create_user('testuser', 'testuser@example.com', 'password123')
    response = client.post('/login', json={
        'username': 'testuser',
        'password': 'password123'
    })
    assert response.status_code == 200
    assert 'access_token' in response.get_json()

def test_login_invalid_username(client):
    response = client.post('/login', json={
        'username': 'unknownuser',
        'password': 'password123'
    })
    assert response.status_code == 401
    assert response.get_json()['error'] == 'Invalid email'

def test_login_invalid_password(client, create_user):
    create_user('testuser', 'testuser@example.com', 'password123')
    response = client.post('/login', json={
        'username': 'testuser',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401
    assert response.get_json()['error'] == 'Invalid password'

def test_profile_success(client, create_user):
    user = create_user('testuser', 'testuser@example.com', 'password123')
    access_token = create_access_token(identity=user.id)
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = client.get('/profile', headers=headers)
    assert response.status_code == 200
    assert response.get_json() == {
        'username': 'testuser',
        'email': 'testuser@example.com'
    }

def test_profile_user_not_found(client):
    access_token = create_access_token(identity=999)  # ID utilisateur qui n'existe pas
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = client.get('/profile', headers=headers)
    assert response.status_code == 404
    assert response.get_json()['error'] == 'User not found'

def test_change_password_success(client, create_user):
    user = create_user('testuser', 'testuser@example.com', 'password123')
    access_token = create_access_token(identity=user.id)
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = client.post('/change_password', headers=headers, json={
        'old_password': 'password123',
        'new_password': 'newpassword123'
    })
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Password successfully updated'

def test_change_password_invalid_old_password(client, create_user):
    user = create_user('testuser', 'testuser@example.com', 'password123')
    access_token = create_access_token(identity=user.id)
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = client.post('/change_password', headers=headers, json={
        'old_password': 'wrongpassword',
        'new_password': 'newpassword123'
    })
    assert response.status_code == 401
    assert response.get_json()['error'] == 'Invalid old password'