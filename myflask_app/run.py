from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:password123@localhost/temporary_user_db'
db = SQLAlchemy(app)

class UserModel(db.Model):
    __tablename__ = 'UserModel'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True)
    uname = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))  # Ideally, this should be hashed
    email = db.Column(db.String(100), unique=True)

    def __repr__(self) -> str:
        return f'<User: {self.email}>'
    
@app.route('/add_user/<username>/<password>')
def add_user(username, password):
    user = UserModel(username=username, password=password)
    db.session.add(user)
    db.session.commit()

    return '<h1>Added new user!</h1>'

if __name__ == '__main__':
    app.run(debug=True)
