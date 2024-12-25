import pytest
from flask import Flask, json
from flask_jwt_extended import JWTManager
from extensions import db, bcrypt
from routes.user_routes import user_bp
from models import User

@pytest.fixture
def app():
    """Configure l'application pour les tests."""
    app = Flask(__name__)
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'SECRET_KEY': 'test_secret',
        'JWT_SECRET_KEY': 'jwt_secret_for_test'  # Ajout de la clé JWT
    })

    # Initialiser les extensions
    db.init_app(app)
    bcrypt.init_app(app)
    JWTManager(app)  # Initialisation du JWT Manager
    
    # Enregistrer le blueprint
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
    """Test l'enregistrement réussi d'un utilisateur."""
    response = client.post('/register', json={
        'username': 'newuser',
        'email': 'new@test.com',
        'password': 'TestPass123'
    })
    assert response.status_code == 201
    assert 'message' in json.loads(response.data)

def test_register_duplicate_email(client, create_user):
    """Test l'enregistrement avec un email déjà utilisé."""
    # Créer un premier utilisateur
    create_user('existinguser', 'existing@test.com', 'TestPass123')
    
    # Tenter de créer un utilisateur avec le même email
    response = client.post('/register', json={
        'username': 'newuser',
        'email': 'existing@test.com',
        'password': 'TestPass123'
    })
    assert response.status_code == 400
    assert 'error' in json.loads(response.data)

def test_register_invalid_data(client):
    """Test l'enregistrement avec des données invalides."""
    # Test avec un email invalide
    response = client.post('/register', json={
        'username': 'newuser',
        'email': 'invalid-email',
        'password': 'TestPass123'
    })
    assert response.status_code == 400
    
    # Test avec un mot de passe trop court
    response = client.post('/register', json={
        'username': 'newuser',
        'email': 'new@test.com',
        'password': 'short'
    })
    assert response.status_code == 400

def test_login_success(client, create_user):
    """Test la connexion réussie."""
    create_user('loginuser', 'login@test.com', 'TestPass123')
    response = client.post('/login', json={
        'username': 'loginuser',
        'password': 'TestPass123'
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'access_token' in data
    assert 'user' in data

def test_login_invalid_credentials(client, create_user):
    """Test la connexion avec des identifiants invalides."""
    create_user('loginuser', 'login@test.com', 'TestPass123')
    
    # Test avec un mauvais mot de passe
    response = client.post('/login', json={
        'username': 'loginuser',
        'password': 'WrongPass123'
    })
    assert response.status_code == 401
    
    # Test avec un utilisateur inexistant
    response = client.post('/login', json={
        'username': 'nonexistent',
        'password': 'TestPass123'
    })
    assert response.status_code == 401

def test_protected_route(client, auth_headers):
    """Test l'accès à une route protégée avec authentification."""
    response = client.get('/profile', headers=auth_headers)
    assert response.status_code == 200
    
def test_protected_route_without_token(client):
    """Test l'accès à une route protégée sans authentification."""
    response = client.get('/profile')
    assert response.status_code == 401