#!/usr/bin/python3
from flask import Flask
from flask_login import LoginManager
from .config import Config
from .auth import login_manager
from .models.storage import Session
from .models import *
from flask_cors import CORS
from flask_mail import Mail
from .routes import bp

app = Flask(__name__)
"""Create a Flask application instance"""

app.config.from_object(Config)
app.config.from_envvar('TICKETY_SETTINGS', silent=True)
CORS(app)

login_manager.init_app(app)
login_manager.login_view = 'login'
@login_manager.user_loader
def load_user(user_id):
    """Load a user by ID"""
    session = Session()
    """Create a new database session"""
    user = session.query(User).get(user_id)
    """Query the user by ID"""
    session.close()
    """Close the database session"""
    return user

mail = Mail(app)

app.register_blueprint(bp)
if __name__ == "__main__":
    app.run()