# entry point for the app, initialize the app, set up routes, connect database
import os
from flask import Flask
from config import Config
from extensions import db, bcrypt, jwt
from dotenv import load_dotenv
from flask_migrate import Migrate
from routes.user_routes import user_bp
from routes.post_routes import post_bp

# load environment variables
# load_dotenv()

# print("DATABASE_URL: ", os.getenv('DATABASE_URL'))

# initialize app and config
app = Flask(__name__)
app.config.from_object(Config)

# add secret key for jwt
app.config['JWT_SECRET_KEY'] = 'test-secret-key'

# initialize extensions
db.init_app(app)
bcrypt.init_app(app)
jwt.init_app(app)
migrate = Migrate(app, db)

# blueprints
app.register_blueprint(user_bp)
app.register_blueprint(post_bp)

if __name__ == '__main__':
    app.run(debug=True)