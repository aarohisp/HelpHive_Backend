# Where you'll initialize and add all the routes for your resources.

# apis/routes.py
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from ..database.models import db, UserModel

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data['username']
    password = data['password']
    email = data['email']

    if UserModel.query.filter_by(username=username).first() or UserModel.query.filter_by(email=email).first():
        return jsonify({"message": "Username or email already exists"}), 400

    password_hash = generate_password_hash(password, method='sha256')

    new_user = UserModel(username=username, password_hash=password_hash, email=email)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']

    user = UserModel.query.filter_by(username=username).first()

    if user and check_password_hash(user.password_hash, password):
        # Implement JWT token generation here
        return jsonify({"token": "your_generated_token"}), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401
