#   store configuration variables like databse connection details and secret keys here

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Charger la clé secrète depuis l'environnement, sinon utiliser une valeur par défaut
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    # Définir `SQLALCHEMY_DATABASE_URI` pour que SQLAlchemy puisse s'y connecter
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Clé JWT pour l'authentification
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'default_jwt_secret_key')

    # Imprimer la valeur pour vérifier
    # print("Config - SQLALCHEMY_DATABASE_URI:", SQLALCHEMY_DATABASE_URI)

