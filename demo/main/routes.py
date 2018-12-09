from flask import request, Blueprint, redirect


# Create main Blueprint
main = Blueprint('main', __name__)


# Redirect requests to api documentation
@main.route("/")
def home():
    return redirect('https://documenter.getpostman.com/view/6103792/RzfiGnqP'), 302