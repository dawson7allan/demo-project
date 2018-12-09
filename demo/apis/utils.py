from datetime import datetime
from functools import wraps
from flask import request
from demo.models import User, Product
from flask_restful import reqparse


# Function to validate datetime
def validate_datetime(date_time):
    # Check if the user sent argument is a valid date time
    try:
        return True, datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return False, { 'message': { 'date_time': 'Incorrect date_time format, should be YYYY-MM-DD HH:MM:SS' } }


# Function to check / validate api key
def check_api_key(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        # Parse the arguments sent by the user
        parser = reqparse.RequestParser()
        parser.add_argument('key', type=str, required=True, help='Invalid / Missing api key, should be an string')
        args = parser.parse_args()
        
        api_key = args['key']
        # Check key against the database
        user = User.query.filter_by(api_key=api_key).first()

        # If user with key not found give user feedback
        if(user is None):
            return { 'message': 'Invalid / Missing api key' }, 403

        return func(*args, **kwargs)

    return decorated_function


# Fuction to check product id
def check_product_id(func):
    @wraps(func)
    def decorated_function(*args, product_id):

        # If no product id was given, give user feedback
        if(product_id is None):
            return { 'message': 'Missing product_id' }, 404

        # Get the product using the product id
        product = Product.query.get(int(product_id))

        # If no product found, give user feedback
        if(product is None):
            return { 'message': 'Invalid product_id' }, 404
        
        return func(*args, product_id)

    return decorated_function


# Function check the per_page limit number 
def limit_per_page(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):

        # Parse the arguments sent by user
        parser = reqparse.RequestParser()
        parser.add_argument('per_page', type=int, required=False, help='Incorrect per_page, should be an integer')
        args = parser.parse_args()
        
        # If no per_page argument was passed, set it to default of 5
        per_page = args['per_page'] if(args['per_page']) else 5

        # If per page argument is more than 10, give user feedback
        if(per_page is not None and per_page >10):
            return { 'message': 'You can only show a maximum of 10 products per page' }

        return func(*args, **kwargs)

    return decorated_function