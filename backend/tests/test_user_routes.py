import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app
from extensions import db
import pytest


@pytest.fixture
def client():
    # configure the app in test mode
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['JWT_SECRET_KEY'] = 'test-secret-key'

    # create test app
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_register(client):
    response = client.post('/register', json={
        'username': 'test_user',
        'email': 'test_user@test.com',
        'password': 'password'
    })
    assert response.status_code == 201
    assert response.json == {'message': 'User successfully registered'}

def test_login(client):
    client.post('/register', json={
        'username': 'test_user',
        'email': 'test_user@test.com',
        'password': 'password'
    })

    response = client.post('/login', json={
        'username': 'test_user',
        'password': 'password'
    })
    assert response.status_code == 200
    assert 'access_token' in response.json