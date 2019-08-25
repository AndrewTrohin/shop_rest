import os


class Config:
    DEBUG = True
    CSRF_ENABLED = True
    JSON_SORT_KEYS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key'
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = "postgresql://{DB_USER}:{DB_PASS}@{DB_ADDR}/{DB_NAME}".format(DB_USER="postgres",
                                                                                            DB_PASS="postgres",
                                                                                            DB_ADDR="127.0.0.1",
                                                                                            DB_NAME="shop")
