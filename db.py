from os import getenv
from flask_sqlalchemy import SQLAlchemy
from app import app

uri = getenv("DATABASE_URL")
SECRET_KEY = getenv('SECRET_KEY', 'Optional default value')
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
