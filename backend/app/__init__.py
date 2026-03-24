from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from .config import Config
from .models import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app, resources={r'/api/*': {'origins': '*'}})
    JWTManager(app)
    db.init_app(app)
    Migrate(app, db)

    from .routes.auth import auth_bp
    from .routes.candidates import candidates_bp
    from .routes.logs import logs_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(candidates_bp, url_prefix='/api')
    app.register_blueprint(logs_bp, url_prefix='/api')

    @app.route('/api/health')
    def health():
        return {'status': 'ok'}

    return app
