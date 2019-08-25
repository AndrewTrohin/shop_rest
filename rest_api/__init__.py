from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
ma = Marshmallow(app)


from rest_api import views


def init_bd():
    db.create_all()