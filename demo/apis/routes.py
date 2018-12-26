from flask import request, Blueprint, jsonify
from demo import db, api
from demo.models import Product
from demo.schema import ProductSchema
from flask_restful import Resource, reqparse
from demo.apis.utils import validate_datetime, check_api_key, check_product_id, limit_per_page


# Create apis Blueprint
apis = Blueprint('apis', __name__)


# Class to handle Product List request
class Products(Resource):

    @check_api_key
    @limit_per_page
    # Gets a list of products
    def get(self):
        # Parse the arguments sent by user
        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, required=False, help='Incorrect page, should be an integer')
        parser.add_argument('per_page', type=int, required=False, help='Incorrect per_page, should be an integer')
        parser.add_argument('date_time', type=str, required=False, help='Incorrect / Missing date_time, should be "YYYY-MM-DD HH:MM:SS"')
        parser.add_argument('description', type=str, required=False, help='Incorrect / Missing description, should be a string')
        args = parser.parse_args()
        
        page = args['page'] if(args['page']) else 1
        per_page = args['per_page'] if(args['per_page']) else 5

        try:
            # Query the Product table and paginate results
            if(args['date_time'] and args['description']):
                date_time = validate_datetime(args['date_time'])
                # print(args['date_time'], args['description'])
                paginated_products = Product.query.filter_by(date_time=date_time, description=args['description']).paginate(page=page, per_page=per_page)

                if(paginated_products.total == 0):
                    return { 'message': 'Product with given date_time and description was not found' }, 404
            else:
                paginated_products = Product.query.paginate(page=page, per_page=per_page)
                
            products = paginated_products.items
            # Use the ProductSchema to convert SQLAlchemy object to JSON
            product_schema = ProductSchema(many=True)
            product_result = product_schema.dump(products)
            # Add some useful info to the JSON
            product_result = { 
                'cur_page': paginated_products.page,
                'total_pages': paginated_products.pages,
                'total_products': paginated_products.total,
                'products_per_page': paginated_products.per_page,
                'products': product_result
            }
            return product_result, 200
        except Exception as err:
            print(err)
            # If the page doesn't exist, give user feedback
            return {'message': 'This page does not exist'}, 404

    @check_api_key
    # Saves a product to the database
    def post(self):
        # Parse the arguments sent by user
        parser = reqparse.RequestParser()
        parser.add_argument('date_time', type=str, required=True, help='Incorrect / Missing date_time, should be "YYYY-MM-DD HH:MM:SS"')
        parser.add_argument('description', type=str, required=True, help='Incorrect / Missing description, should be a string')
        parser.add_argument('latitude', type=float, required=True, help='Incorrect / Missing latitude, should be a float')
        parser.add_argument('longitude', type=float, required=True, help='Incorrect / Missing longitude, should be a float')
        parser.add_argument('elevation', type=int, required=True, help='Incorrect / Missing elevation, should be an integer')
        args = parser.parse_args()

        # Check the if the given date_time is valid
        is_date_time, date_time = validate_datetime(args['date_time'])
        if(not is_date_time):
            return date_time, 200

        # Add the product to the database
        product = Product(date_time=date_time, description=args['description'], latitude=args['latitude'], longitude=args['longitude'], elevation=args['elevation'])
        db.session.add(product)
        db.session.commit()

        return { 'message': 'Product has been successfully added' }, 201


# Class to handle product view, update and delete
class Product_View(Resource):

    @check_api_key
    @check_product_id
    # Gets a product
    def get(self, product_id):
        try:
            # Query the product with it's product id
            product = Product.query.get(int(product_id))
            # If product exists return product
            if(product):
                product_schema = ProductSchema()
                product_result = product_schema.dump(product)
                return product_result.data, 200
            else:
                raise Exception
        except:
            return {'message': 'This product does not exist'}, 404

    @check_api_key
    @check_product_id
    # Updates a product
    def put(self, product_id):
        # Parse the arguments sent by user
        parser = reqparse.RequestParser()
        parser.add_argument('date_time', type=str, required=False, help='Incorrect / Missing date_time, should be "YYYY-MM-DD HH:MM:SS"')
        parser.add_argument('description', type=str, required=False, help='Incorrect / Missing description, should be a string')
        parser.add_argument('latitude', type=float, required=False, help='Incorrect / Missing latitude, should be a float')
        parser.add_argument('longitude', type=float, required=False, help='Incorrect / Missing longitude, should be a float')
        parser.add_argument('elevation', type=int, required=False, help='Incorrect / Missing elevation, should be an integer')
        args = parser.parse_args()

        # Check if date_time is valid
        date_time = validate_datetime(args['date_time'])

        # Try to update the product, if an exception handle it and give user feedback
        try:
            if(date_time):
                product = Product.query.get(int(product_id))
                product.date_time = date_time
                for argument in args:
                    if(args[argument] is not None):
                        if(argument == 'description'):
                            product.description = args[argument]
                        elif(argument == 'latitude'):
                            product.latitude = args[argument]
                        elif(argument == 'longitude'):
                            product.longitude = args[argument]
                        elif(argument == 'elevation'):
                            product.elevation = args[argument]

                db.session.add(product)
                db.session.commit()
                return { 'message': 'This product has been successfully updated' }, 201
        except:
            return { 'message': 'This product does not exist' }, 404

    @check_api_key
    @check_product_id
    # Deletes a product
    def delete(self, product_id):
        try:
            # Get the product with product id
            product = Product.query.get(int(product_id))
            # If product exists, delete it, else raise exception and give user feedback
            if(product):
                db.session.delete(product)
                db.session.commit()
            else:
                raise Exception

            return { 'message': 'This product has been successfully deleted' }, 201
        except Exception as e:
            print(e)
            return { 'message': 'This product does not exist' }, 404


# Register the route to access the above classes
api.add_resource(Products, '/api/v1/products')
api.add_resource(Product_View, '/api/v1/product/<int:product_id>')