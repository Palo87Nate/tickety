from flask import Flask
from flask_login import LoginManager
from .config import Config
from .auth import login_manager
from .models.storage import Session
from .models import *
from flask_cors import CORS
from . import routes
from .routes import bp

app = Flask(__name__)
"""Create a Flask application instance"""

app.config.from_object(Config)
"""Load configuration from the Config class"""

app.config.from_envvar('TICKETY_SETTINGS', silent=True)
"""Load configuration from the TICKETY_SETTINGS environment variable"""

CORS(app)
"""Enable CORS support for the application"""

login_manager.init_app(app)
"""Initialize the login manager for the application"""

login_manager.login_view = 'login'
"""Set the login view for the login manager"""

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

app.register_blueprint(bp)
"""Register the routes blueprint with the application"""

if __name__ == "__main__":
    """Entry point for the application"""
    app.run(host='0.0.0.0', port=5000, debug=True)
    """Run the application in debug mode"""