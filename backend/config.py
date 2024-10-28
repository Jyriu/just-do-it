#   store configuration variables like databse connection details and secret keys here

import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'defaut_secret_key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:8a08ad81@localhost/just_do_it_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False