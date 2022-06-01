import os
from datetime import timedelta


class Development:
    DEBUG = True
    DEVELOPMENT = True
    JSON_SORT_KEYS = False
    SQLALCHEMY_DATABASE_URI = \
        f'mysql+pymysql://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWD")}@{os.getenv("DB_HOST")}/{os.getenv("DB_NAME")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('APP_SECRET_KEY')
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
    SESSION_COOKIE_NAME = 'google-login-session'
    SESSION_COOKIE_SECURE = True
    SESSION_LIFETIME = timedelta(minutes=5)
    SESSION_REFRESH_EACH_REQUEST = False
    FRONTEND_URL = os.getenv('FRONTEND_URL')


class Production(Development):
    DEBUG = False
    DEVELOPMENT = True
