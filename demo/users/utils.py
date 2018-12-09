from flask_restful import reqparse
from functools import wraps
import re


# Function to check / validate user credentials
def check_user_creds(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        # Parse arguments sent by user
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, help='Incorrect / Missing username, should be a string')
        parser.add_argument('email', type=str, required=True, help='Incorrect / Missing email, should be a string')
        parser.add_argument('password', type=str, required=True, help='Incorrect / Missing password, should be a string')
        p_args = parser.parse_args()

        # Validate arguments
        if(len(p_args['username'].strip()) <= 3):
            return { 'message': 'Username has to be more than 3 characters long' }, 200
        if(not re.match(r"\w+@\w+\.\w+", p_args['email'])):
            return { 'message': 'Please enter a valid email' }, 200
        if(len(p_args['password']) <= 5):
            return { 'message': 'Password has to be more than 5 characters long' }, 200


        return func(*args, **kwargs)

    return decorated_function


# Function to validate just the email
def check_email(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True, help='Incorrect / Missing email, should be a string')
        p_args = parser.parse_args()

        if(not re.match(r"\w+@\w+\.\w+", p_args['email'])):
            return { 'message': 'Please enter a valid email' }, 200

        return func(*args, **kwargs)

    return decorated_function