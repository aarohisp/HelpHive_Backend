from flask import request, jsonify

def set_user_routes(app):
    @app.route('/api/test-get', methods=['GET'])
    def test_get():
        data = {"message": "This is a test GET API"}
        return jsonify(data), 200

    @app.route('/api/test-post', methods=['POST'])
    def test_post():
        data = request.json  # Get JSON data from the request body

        # Process the JSON data (you can perform any logic here)

        response_data = {"message": "This is a test POST API", "data_received": data}
        return jsonify(response_data), 201
