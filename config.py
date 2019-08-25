import os


class Config:
    DEBUG = False
    CSRF_ENABLED = True
    JSON_SORT_KEYS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key'
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = "postgresql://{DB_USER}:{DB_PASS}@{DB_ADDR}/{DB_NAME}".format(DB_USER="shop_r",
                                                                                            DB_PASS="shop_r",
                                                                                            DB_ADDR="127.0.0.1",
                                                                                            DB_NAME="shop")
