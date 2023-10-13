from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Load configuration settings from config.py
    config_file_path = os.path.abspath('./config.py')
    app.config.from_pyfile(config_file_path)

    # Initialize the database
    db.init_app(app)

    # Import your routes
    from apis import routes

    return app