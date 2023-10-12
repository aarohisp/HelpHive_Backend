# from flask import Flask, request, jsonify, flash
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import create_engine
# from sqlalchemy.orm import scoped_session, sessionmaker
# from passlib.hash import sha256_crypt

# app = Flask(__name__)
# app.secret_key = "H3lpH!v3"

# engine = create_engine("mysql+mysqldb://root:password123@localhost/temporary_user_db")
# db = scoped_session(sessionmaker(bind=engine))

# # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:password123@localhost/temporary_user_db'
# # db = SQLAlchemy(app)

# class UserModel(db.Model):
#     __tablename__ = 'UserModel'
#     user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     username = db.Column(db.String(50), unique=True)
#     uname = db.Column(db.String(50), unique=True)
#     password = db.Column(db.String(50))  # Ideally, this should be hashed
#     email = db.Column(db.String(100), unique=True)

#     def __repr__(self) -> str:
#         return f'<User: {self.email}>'

# @app.route('/api/register', methods=['POST'])
# def register():
#     data = request.get_json()

#     name = data.get("name")
#     username = data.get("username")
#     password = data.get("password")
#     confirm = data.get("confirm")
    
#     secure_password = sha256_crypt.encrypt(str(password))
    
#     usernamedata = db.execute("SELECT username FROM users WHERE username=:username", {"username": username}).fetchone()

#     if usernamedata == None:
#         if password == confirm:
#             db.execute("INSERT INTO users(name, username, password) VALUES(:name, :username, :password)",
#                        {"name": name, "username": username, "password": secure_password})
#             db.commit()
#             response = {"message": "You are registered and can now login", "status": "success"}
#         else:
#             response = {"message": "Password does not match", "status": "danger"}
#     else:
#         response = {"message": "User already exists, please login or contact admin", "status": "danger"}

#     return jsonify(response)

# @app.route('/api/login', methods=["GET"])
# def login():
#     data = request.get_json()

#     username = data.get("username")
#     password = data.get("password")

#     usernamedata = db.execute("SELECT username FROM users WHERE username=:username", {"username": username}).fetchone()
#     passworddata = db.execute("SELECT password FROM users WHERE username=:username", {"username": username}).fetchone()

#     if usernamedata is None:
#         response = {"message": "No username", "status": "danger"}
#     else:
#         for password_data in passworddata:
#             if sha256_crypt.verify(password, password_data):
#                 response = {"message": "You are now logged in!!", "status": "success"}
#             else:
#                 response = {"message": "Incorrect password", "status": "danger"}

#     return jsonify(response)

# @app.route('/api/add_user/<username>/<password>', methods=['POST'])
# def add_user(username, password):
#     user = UserModel(username=username, password=password)
#     db.session.add(user)
#     db.session.commit()

#     return jsonify({"message": "Added new user!", "status": "success"})

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
#from passlib.hash import sha256_crypt

app = Flask(__name__)
app.secret_key = "H3lpH!v3"  # Replace with a secure secret key

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

@app.route('/api/register', methods=['GET'])
def register():
    data = request.json

    name = data.get("uname")
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")
    
 #   secure_password = sha256_crypt.encrypt(str(password))
    
    usernamedata = UserModel.query.filter_by(username=username).first()

    if usernamedata is None:
        new_user = UserModel(uname=name, username=username, password=password, email = email)
        db.session.add(new_user)
        db.session.commit()
        response = {"message": "You are registered and can now login", "status": "success"}
        # else:
        #     response = {"message": "Password does not match", "status": "danger"}
    else:
        response = {"message": "User already exists, please login or contact admin", "status": "danger"}

    return jsonify(response)

@app.route('/api/login', methods=["GET"])
def login():
    data = request.json

    username = data.get("username")
    password = data.get("password")

    user = UserModel.query.filter_by(username=username).first()

    if user is None:
        response = {"message": "No username", "status": "danger"}
    elif password == user.password:
        response = {"message": "You are now logged in!!", "status": "success"}
    else:
        response = {"message": "Incorrect password", "status": "danger"}

    return jsonify(response)

@app.route('/api/add_user/<username>/<password>', methods=['POST'])
def add_user(username, password):
    user = UserModel(username=username, password=password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Added new user!", "status": "success"})

if __name__ == '__main__':
    app.run(debug=True)
