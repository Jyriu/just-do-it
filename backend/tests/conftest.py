import os
import sys
import pytest

# Ajouter le répertoire 'backend' au path Python pour permettre l'importation correcte des modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importer la fonction de création d'application et les extensions
from app import create_app
from extensions import db
from models.user import User
from models.topic import Topic

@pytest.fixture
def app():
    """
    Configure l'application pour les tests.
    """
    # Créez une nouvelle instance de l'application pour chaque test
    app = create_app()

    # Configurer l'application pour le test
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "postgresql://postgres:password@localhost/test_db",  # Utiliser une base de données de test
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "JWT_SECRET_KEY": "test_secret_key"  # Clé secrète pour JWT dans l'environnement de test
    })

    with app.app_context():
        db.create_all()  # Crée les tables pour chaque test run

        # Générer des données de test
        user = User(username="testuser", email="testuser@example.com", password_hash="hashed_password")
        db.session.add(user)

        topic = Topic(name="General", description="A general discussion topic.")
        db.session.add(topic)

        db.session.commit()  # Sauvegarder les changements

        yield app

        # Nettoyage après les tests
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """
    Fournit un client de test Flask pour simuler des requêtes HTTP.
    """
    return app.test_client()

@pytest.fixture
def create_user():
    """
    Fonction utilitaire pour créer un utilisateur facilement.
    """
    def _create_user(username, email, password):
        user = User(username=username, email=email, password_hash=password)
        db.session.add(user)
        db.session.commit()
        return user

    return _create_user