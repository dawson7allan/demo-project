from demo import db, bcrypt
from uuid import uuid1


# User Model to authorize users with api keys
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    api_key = db.Column(db.String(40), nullable=False)

    # Returns a uuid, which we will use for api key
    @staticmethod
    def get_api_key():
        return uuid1()

    # Hashes the plain text password using bcrypt
    @staticmethod
    def hash_password(password):
        return bcrypt.generate_password_hash(password).decode('utf-8')

    # Checks the user entered password against the existing hash in the database
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    # Just to see what object without having to access it's attributes
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


# Product Model to store all the products
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_time = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    elevation = db.Column(db.Integer, nullable=False)

    # Just to see what object without having to access it's attributes
    def __repr__(self):
        return f"Product('{self.description}', '{self.date_time}')"
