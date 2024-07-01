from flask import Flask
from flask_login import LoginManager
import os

db_path = os.path.join(os.path.dirname(__file__), 'database.db')

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'asldfj_slkdf_sefwe_sdfvvw'
    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import create_database, User
    from .db_utils import populate_database
    if not os.path.exists(db_path):
        create_database()
        populate_database()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.get(user_id)

    return app