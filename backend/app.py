# entry point for the app, initialize the app, set up routes, connect database
from flask import Flask
from config import Config
from extensions import db, bcrypt, jwt
from dotenv import load_dotenv
from routes.user_routes import user_bp

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

# blueprints
app.register_blueprint(user_bp)

if __name__ == '__main__':
    app.run(debug=True)