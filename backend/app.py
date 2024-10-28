# entry point for the app, initialize the app, set up routes, connect database
from flask import Flask
from config import Config
from extensions import db, bcrypt

# initialize app and config
app = Flask(__name__)
app.config.from_object(Config)

# initialize extensions
db.init_app(app)
bcrypt = Bcrypt(app)

# blueprints
from routes.user_routes import user_bp
app.register_blueprint(user_bp)

if __name__ == '__main__':
    app.run(debug=True)