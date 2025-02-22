from flask import Blueprint, jsonify

category_bp = Blueprint('category', '__name__')

@category_bp.route('/')
def category_home():
    return jsonify({'message': 'This is the category home.'}), 200
