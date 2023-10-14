from flask import request, jsonify, current_app
from app import db
from database.models import UserModel, ItemModel

def init_routes(app):
    @app.route('/api/register', methods=['GET'])
    def register():
        data = request.json

        name = data.get("uname")
        username = data.get("username")
        password = data.get("password")
        email = data.get("email")

        with current_app.app_context():  # Ensure you're within the application context
            # Check if the username already exists
            user_exists = UserModel.query.filter_by(username=username).first()

            if user_exists is None:
                new_user = UserModel(uname=name, username=username, password=password, email=email)
                db.session.add(new_user)
                db.session.commit()
                response = {"message": "You are registered and can now login", "status": "success"}
            else:
                response = {"message": "User already exists, please login or contact admin", "status": "danger"}

        return jsonify(response)

    @app.route('/api/login', methods=["POST"])
    def login():
        data = request.json

        username = data.get("username")
        password = data.get("password")

        user = UserModel.query.filter_by(username=username).first()

        if user is None:
            response = {"message": "No username", "status": "danger"}
        elif password == user.password:
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

        response = {
            "message": "Item is registered in the database",
            "status": "success",
            "product id": new_item.item_id,
            "product name": new_item.item_name
            }

        return jsonify(response)

    @app.route('/api/get_product/<int:item_id>', methods=['GET'])    
    def get_product(item_id):
        try:
            item = ItemModel.query.get(item_id)

            if item:
                item_data = {
                    "item_id": item.item_id,  # Use item_id instead of id
                    "item_name": item.item_name,
                    "descriptions": item.descriptions,
                    "time_used": item.time_used,
                    "donor_id": item.donor_id,
                    "category_id": item.category_id,
                    "item_address": item.item_address,
                    "image_info": item.image_info,
                    "specification": item.specification,
                    "org_id": item.org_id
                }

                return jsonify({"item": item_data, "status": "success"})
            else:
                return jsonify({"message": "Item not found", "status": "error"}), 404

        except Exception as e:
            return jsonify({"message": "An error occurred", "error": str(e), "status": "error"}), 500
  
    @app.route('/api/add_user/<username>/<password>', methods=['GET'])
    def add_user(username, password):
        with current_app.app_context():  # Ensure you're within the application context
            user = UserModel(username=username, password=password)
            db.session.add(user)
            db.session.commit()

        return jsonify({
            "message": "Added new user!",
             "status": "success"})
