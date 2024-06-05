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
app.config.from_object(Config)
app.config.from_envvar('TICKETY_SETTINGS', silent=True)

CORS(app)

login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    session = Session()
    user = session.query(User).get(user_id)
    session.close()
    return user


app.register_blueprint(bp)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
