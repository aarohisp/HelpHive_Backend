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

from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
# from .webpages import login_result
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

class ItemModel(db.Model):
    __tablename__ = 'Item'
    item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_name = db.Column(db.String(25), nullable=False)
    descriptions = db.Column(db.String(100), nullable=False)
    time_used = db.Column(db.Integer, nullable=False)
    donor_id = db.Column(db.Integer, db.ForeignKey('UserModel.user_id'), nullable=False)
    category_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    item_address = db.Column(db.String(100), nullable=False)
    image_info = db.Column(db.String(100), nullable=False)
    specification = db.Column(db.String(50), nullable=False)
    item_check = db.Column(db.Boolean, default=False)
    status_item = db.Column(db.Enum('open', 'closed', 'expired', name='status_item_enum'), nullable=False, default='open')
    org_id = db.Column(db.Integer, nullable=False)

    # Define a relationship to the UserModel
    donor = db.relationship('UserModel', backref='donated_items', foreign_keys=[donor_id])


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

# @app.route('/api/login', methods=["GET"])
# def login():
#     data = request.json

#     username = data.get("username")
#     password = data.get("password")

#     user = UserModel.query.filter_by(username=username).first()

#     if user is None:
#         response = {"message": "No username", "status": "danger"}
#     elif password == user.password:
#         # Successful login
#         response = {
#             "message": "You are now logged in!!",
#             "status": "success",
#             "uname": user.uname,
#             "username": user.username,
#             "email": user.email
#         }
#     else:
#         response = {"message": "Incorrect password", "status": "danger"}

#     return jsonify(response)

from flask import request, jsonify

@app.route('/api/login', methods=["POST"])
def login():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    user = UserModel.query.filter_by(username=username).first()

    if user is None:
        response = {"message": "No username", "status": "danger"}
    elif password == user.password:
        # Successful login
        response = {
            "message": "You are now logged in!!",
            "status": "success",
            "uname": user.uname,
            "username": user.username,
            "email": user.email
        }
    else:
        response = {"message": "Incorrect password", "status": "danger"}

    return jsonify(response)

@app.route('/api/add_user/<username>/<password>', methods=['POST'])
def add_user(username, password):
    user = UserModel(username=username, password=password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Added new user!", "status": "success"})

@app.route('/api/get_user_info', methods=['GET'])
def get_user_info():
    data = request.json

    username = data.get("username")

    user = UserModel.query.filter_by(username=username).first()

    if user:
        user_info = {
            "username": user.username,
            "uname": user.uname,
            "email": user.email
        }
        return jsonify(user_info)
    else:
        return jsonify({"message": "User not found"}, 404)

@app.route('/api/add_product', methods=['GET'])
def add_product():
    data = request.json

    item_name = data.get("item_name")
    descriptions = data.get("descriptions")
    time_used = data.get("time_used")
    donor_id = data.get("donor_id")
    category_id = data.get("category_id")
    item_address = data.get("item_address")
    image_info = data.get("image_info")
    specification = data.get("specification")
    org_id = data.get("org_id")

    new_item = ItemModel(
        item_name=item_name,
        descriptions=descriptions,
        time_used=time_used,
        donor_id=donor_id,
        category_id=category_id,
        item_address=item_address,
        image_info=image_info,
        specification=specification,
        org_id=org_id
    )

    db.session.add(new_item)
    db.session.commit()

    response = {"message": "Item is registered in the database", "status": "success"}

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
