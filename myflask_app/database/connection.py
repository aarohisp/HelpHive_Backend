#For establishing and handling a MySQL connection.

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password123@localhost/temporary_user_db'
db = SQLAlchemy(app)
