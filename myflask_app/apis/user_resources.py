#Each module has its own resources file. This will contain classes that define the RESTful resources using Flask-RESTful.
from flask_restful import Resource, reqparse
from services.user_services import UserService

parser = reqparse.RequestParser()
parser.add_argument('username', type=str, required=True, help='Username cannot be blank')
parser.add_argument('password', type=str, required=True, help='Password cannot be blank')
parser.add_argument('email', type=str, required=True, help='Email cannot be blank')

class UserResource(Resource):
    def get(self, user_id):
        user = UserService.get_user_by_id(user_id)
        if user:
            return {
            'id': user.id,
            'username': user.username,
            'email': user.email
            }
            return {'message': 'User not found'}, 404

    def post(self):
        data = parser.parse_args()
        UserService.create_user(data['username'], data['password'], data['email'])
        return {'message': 'User created successfully'}, 201
