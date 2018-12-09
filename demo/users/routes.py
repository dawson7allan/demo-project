from flask import Blueprint
from demo import db, api
from demo.models import User
from flask_restful import Resource, reqparse
from demo.users.utils import check_user_creds, check_email


# Create users Blueprint
users = Blueprint('users', __name__)


# Class to handle user registration
class Register(Resource):

    @check_user_creds
    def post(self):
        # Parse the arguments sent by user
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, help='Incorrect / Missing username, should be a string')
        parser.add_argument('email', type=str, required=True, help='Incorrect / Missing email, should be a string')
        parser.add_argument('password', type=str, required=True, help='Incorrect / Missing password, should be a string')
        args = parser.parse_args()

        # Try to create the user account, if exception handle appropriately and let the user know what happened
        try:
            user = User()
            user.username = args['username']
            user.email = args['email']
            user.password = user.hash_password(args['password'])
            user.api_key = str(user.get_api_key())
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            cause = str(e.__cause__)
            if('email' in cause):
                return { 'message': 'Email already exists' }, 403
            elif('username' in cause):
                return { 'message': 'Username already exists' }, 403
            else:
                return { 'message': 'Something went wrong' }, 500

        return { 'message': 'User has been successfully added', 'api_key': user.api_key }, 201


# Class to handle user login
class Login(Resource):

    @check_email
    def post(self):
        # Parse the arguments sent by user
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True, help='Incorrect / Missing email, should be a string')
        parser.add_argument('password', type=str, required=True, help='Incorrect / Missing password, should be a string')
        args = parser.parse_args()

        try:
            # Get the user by email
            user = User.query.filter_by(email=args['email']).first()

            # If no user found give user feedback
            if(user is None):
                return { 'message': 'Invalid credentials' }, 200

            # Check the given password against the one in database
            check_password = user.check_password(args['password'])

            # If the passwords match return api key
            if(check_password):
                return { 'api_key': user.api_key }, 200
            else:
                return { 'message': 'Invalid credentials' }, 200
        except:
            return { 'message': 'Something went wrong' }, 500


# Register the route to access the above classes
api.add_resource(Register, '/api/v1/register')
api.add_resource(Login, '/api/v1/login')