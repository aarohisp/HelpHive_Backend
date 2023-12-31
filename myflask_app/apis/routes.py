import base64
from flask import request, jsonify, current_app, send_file
from app import db
from sqlalchemy import or_
from database.models import UserModel, ItemModel, OrgModel, ImageModel
import bcrypt
from io import BytesIO
from PIL import Image


def init_routes(app):
    @app.route("/api/upload", methods=["POST"])
    def upload_image():
        try:
            org_id = request.form.get("org_id")
            image_category = request.form.get("image_category")

            image_file = request.files["image"]
            if image_file:
                image_data = image_file.read()

                try:
                    image = Image.open(BytesIO(image_data))
                except:
                    return jsonify({"message": "Invalid image format", "status": "error"})
                
                new_image = ImageModel(
                    image_data=image_data,
                    image_category=image_category, 
                    org=OrgModel.query.get(org_id))
                db.session.add(new_image)
                db.session.commit()
                return jsonify({"message": "Image uploaded successfully", "status": "success"})
            else:
                return jsonify({"message": "No image provided", "status": "error"})
        except Exception as e:
            return jsonify({"message": "An error occurred", "error": str(e), "status": "error"})
        
    @app.route("/api/images/category/<int:image_category_id>", methods=["GET"])
    def get_images_by_category(image_category_id):
        try:
            # Query the database for images with the specified image_category
            images = ImageModel.query.filter_by(image_category=image_category_id).all()
            
            if images:
                image_list = []
                
                for image in images:
                    # Convert image data to base64
                    image_data_base64 = base64.b64encode(image.image_data).decode('utf-8')
                    
                    image_list.append({
                        "image_id": image.image_id,
                        "image_data": image_data_base64,
                    })
                
                return jsonify({"images": image_list, "status": "success"})
            else:
                return jsonify({"message": "No images found for the specified category", "status": "error"}), 404
        except Exception as e:
            return jsonify({"message": "An error occurred", "error": str(e), "status": "error"})

    @app.route("/api/images/<int:image_id>", methods=["GET"])
    def get_image(image_id):
        try:
            image = ImageModel.query.get(image_id)
            if image:
                image_data = image.image_data

                # Create an Image object from the image data
                image = Image.open(BytesIO(image_data))

                # Convert the image to JPEG format
                image_io = BytesIO()
                image.save(image_io, format="JPEG")
                image_io.seek(0)

                # Send the image as a response with the correct MIME type
                return send_file(image_io, mimetype="image/jpeg")
            else:
                return jsonify({"message": "Image not found", "status": "error"}), 404
        except Exception as e:
            return jsonify({"message": "An error occurred", "error": str(e), "status": "error"})

    @app.route('/api/register', methods=['POST'])
    def register():
        data = request.json

        name = data.get("uname")
        username = data.get("username")
        password = data.get("password")
        email = data.get("email")
        role_id = data.get("role_id")
        org_id = data.get("org_id")
        phoneno = data.get("phoneno")
        city = data.get("city")

        # Input validation
        if not (name and username and password and email and role_id and org_id and phoneno and city):
            return jsonify({"message": "Missing required fields", "status": "error"})

        with app.app_context():  
            user_exists = UserModel.query.filter_by(username=username).first()

            if user_exists is None:
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

                new_user = UserModel(uname=name, username=username, password=hashed_password, email=email, role_id=role_id, org_id=org_id, phoneno=phoneno, city=city, is_deleted=False)
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
        else:
            if bcrypt.checkpw(password.encode('utf-8'), user.password):
                response = {
                    "message": "You are now logged in!!",
                    "status": "success",
                    "name": user.uname,
                    "username": user.username,
                    "email": user.email
                }
            else:
                response = {"message": "Incorrect password", "status": "danger"}

        return jsonify(response)
    
    @app.route('/api/update_password/<int:user_id>', methods=['PUT'])
    def update_password(user_id):
        try:
            data = request.json
            new_password = data.get("new_password")

            user = UserModel.query.get(user_id)

            if user:
                # Hash the new password before updating
                hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                
                # Update the user's password with the new password
                user.password = hashed_password
                db.session.commit()
                
                response = {"message": "Password updated successfully", "status": "success"}
            else:
                response = {"message": "User not found", "status": "error"}, 404

            return jsonify(response)

        except Exception as e:
            return jsonify({"message": "An error occurred", "error": str(e), "status": "error"}), 500

    @app.route('/api/add_product', methods=['GET'])
    def add_product():
        data = request.json

        item_name = data.get("item_name")
        descriptions = data.get("descriptions")
        time_used = data.get("time_used")
        donor_id = data.get("donor_id")
        category = data.get("category_id")
        item_address = data.get("item_address")
        image_info = data.get("image_info")
        specification = data.get("specification")
        org_id = data.get("org_id")

        with current_app.app_context():
            new_item = ItemModel(
                item_name=item_name,
                descriptions=descriptions,
                time_used=time_used,
                donor_id=donor_id,
                category_id=category,
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

    # For a number of products at once with pagination support
    @app.route('/api/get_products', methods=['GET'])
    def get_products():
        try:
            page = request.args.get('page', default=1, type=int)
            per_page = request.args.get('per_page', default=10, type=int)
            
            products = ItemModel.query.paginate(page=page, per_page=per_page, error_out=False)

            products_data = [
                {
                    "item_id": item.item_id,
                    "item_name": item.item_name,
                    "descriptions": item.descriptions,
                    "time_used": item.time_used,
                    "donor_id": item.donor_id,
                    "category": item.category_id,
                    "item_address": item.item_address,
                    "image_info": item.image_info,
                    "specification": item.specification,
                    "org_id": item.org_id
                }
                for item in products.items
            ]

            return jsonify({
                "items": products_data,
                "total_pages": products.pages,
                "current_page": products.page,
                "status": "success"
            })

        except Exception as e:
            return jsonify({"message": "An error occurred", "error": str(e), "status": "error"}), 500


    @app.route('/api/get_product/<int:item_id>', methods=['GET'])    
    def get_product(item_id):
        try:
            item = ItemModel.query.get(item_id)

            if item:
                item_data = {
                    "item_id": item.item_id, 
                    "item_name": item.item_name,
                    "descriptions": item.descriptions,
                    "time_used": item.time_used,
                    "donor_id": item.donor_id,
                    "category": item.category_id,
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
    
    @app.route('/api/search_items', methods=['GET'])
    def search_items():
        try:
            # Get the search query from the request
            search_query = request.args.get('query')

            # Split the search query into keywords
            keywords = search_query.split()

            # Create a base query for items
            query = ItemModel.query

            # Apply filters based on keywords
            if keywords:
                # Use the OR condition to search for any keyword in the specified fields
                query = query.filter(
                    or_(
                        *[
                            ItemModel.item_name.contains(keyword) |
                            ItemModel.descriptions.contains(keyword) |
                            ItemModel.specification.contains(keyword)
                            for keyword in keywords
                        ]
                    )
                )

            # Execute the query and retrieve the items
            items = query.all()

            # Create a list of item data
            item_list = []
            for item in items:
                item_data = {
                    "item_id": item.item_id,
                    "item_name": item.item_name,
                    "descriptions": item.descriptions,
                    "time_used": item.time_used,
                    "donor_id": item.donor_id,
                    "category": item.category_id,
                    "item_address": item.item_address,
                    "image_info": item.image_info,
                    "specification": item.specification,
                    "org_id": item.org_id,
                }
                item_list.append(item_data)

            response = {"items": item_list, "status": "success"}

            return jsonify(response)

        except Exception as e:
            return jsonify({"message": "An error occurred", "error": str(e), "status": "error"}), 500

    @app.route('/api/search_by_category', methods=['GET'])
    def search_by_category():
        category = request.args.get('category')

        if category not in ['clothes', 'medicine', 'medical supplies', 'furniture']:
            return jsonify({"message": "Invalid category.", "status": "danger"}), 400

        items = ItemModel.query.filter_by(category=category).all()

        if not items:
            return jsonify({"message": "No items found in this category.", "status": "info"})

        item_list = [{"item_name": item.item_name, "description": item.descriptions} for item in items]

        return jsonify({"items": item_list, "status": "success"})
  
    @app.route('/api/add_user/<username>/<password>', methods=['GET'])
    def add_user(username, password):
        with current_app.app_context():  # Ensure you're within the application context
            user = UserModel(username=username, password=password)
            db.session.add(user)
            db.session.commit()

        return jsonify({
            "message": "Added new user!",
             "status": "success"})






