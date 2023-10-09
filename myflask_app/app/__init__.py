# app/__init__.py
from flask import Flask
from ..database.models import db
from ..config import SECRET_KEY, SQLALCHEMY_DATABASE_URI

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

# Initialize the database
db.init_app(app)
