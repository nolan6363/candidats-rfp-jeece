import os
from datetime import timedelta


class Config:
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', 'dev-secret')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'dev-jwt-secret')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{os.environ.get('DB_USER', 'jeece')}:"
        f"{os.environ.get('DB_PASSWORD', 'devpassword')}@"
        f"{os.environ.get('DB_HOST', 'localhost')}:"
        f"{os.environ.get('DB_PORT', '3306')}/"
        f"{os.environ.get('DB_NAME', 'jeece_rfp')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FRONTEND_URL = os.environ.get('FRONTEND_URL', '*')

    ADMIN_EMAIL = 'admin@jeece.fr'
    ADMIN_PASSWORD = 'Admin1234'
