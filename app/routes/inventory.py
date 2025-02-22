from flask import Blueprint, jsonify

inventory_bp = Blueprint('inventory', '__name__')

@inventory_bp.route('/')
def inventory_home():
    return jsonify({'message': 'This is the inventory home.'}), 200
