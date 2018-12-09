from flask import Blueprint, jsonify


# Create errors Blueprint
errors = Blueprint('errors', __name__)


# Function to Handle error 404
@errors.app_errorhandler(404)
def error_404(error):
    return jsonify({ 'message': 'Page Not Found' }), 404


# Function to Handle error 403
@errors.app_errorhandler(403)
def error_403(error):
    return jsonify({ 'message': 'Forbidden' }), 403


# Function to Handle error 500
@errors.app_errorhandler(500)
def error_500(error):
    return jsonify({ 'message': 'Something went wrong, please try again later!' }), 500