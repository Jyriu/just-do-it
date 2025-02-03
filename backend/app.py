# entry point for the app, initialize the app, set up routes, connect database
import os
from flask import Flask
from config import DevelopmentConfig, ProductionConfig, TestingConfig
from extensions import db, bcrypt, migrate
from dotenv import load_dotenv
from flask_migrate import Migrate
from routes.user_routes import user_bp
from routes.post_routes import post_bp, topic_bp
from routes.like_routes import like_bp
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf.csrf import CSRFProtect
from datetime import timedelta

def create_app(config_class=DevelopmentConfig):
    # load environment variables
    load_dotenv()

    # initialize app and config
    app = Flask(__name__)
    
    # Chargement de la configuration
    app.config.from_object(config_class)
    
    # Initialisation des extensions
    CORS(app, resources={
        r"/*": {"origins": app.config['CORS_ORIGINS']}
    })
    JWTManager(app)
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    csrf = CSRFProtect(app)
    
    # Configuration du rate limiting
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        storage_uri=app.config['RATELIMIT_STORAGE_URL'],
        default_limits=["200 per day", "50 per hour"]
    )
    
    # Exemption CSRF pour les routes d'API
    csrf.exempt(user_bp)
    csrf.exempt(post_bp)
    csrf.exempt(like_bp)
    
    # Enregistrement des blueprints
    app.register_blueprint(user_bp)
    app.register_blueprint(post_bp)
    app.register_blueprint(like_bp)
    app.register_blueprint(topic_bp)
    
    # Route de test pour CSRF
    @app.route('/test_csrf', methods=['POST'])
    def test_csrf():
        return {'message': 'CSRF test route'}, 200
    
    return app

# This block will only run if the script is executed directly
if __name__ == '__main__':
    env = os.getenv('FLASK_ENV', 'development')
    config = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'testing': TestingConfig
    }.get(env, DevelopmentConfig)
    
    app = create_app(config)
    app.run()