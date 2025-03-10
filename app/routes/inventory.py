from flask import Blueprint, jsonify, request
from datetime import datetime

from app.extensions import db
from app.models import Product, Inventory

inventory_bp = Blueprint('inventory', '__name__')

@inventory_bp.route('/')
def inventory_home():
    return jsonify({'message': 'This is the inventory home.'}), 200

@inventory_bp.route('/list-view', methods=["GET"])
def get_inventory_list_view():
    get_entire_inventory = Inventory.query.all()
    return jsonify([inventory.get_list_view() for inventory in get_entire_inventory]), 200


@inventory_bp.route('/detail-view/<int:id>', methods=["GET"])
def get_inventory_detail_view(id):
    selected_inventory = Inventory.query.filter_by(id=id).first()
    if not selected_inventory:
            return jsonify({'error': f"Inventory with id {id} not found"}), 404
    return jsonify(selected_inventory.get_detail_view()), 200


@inventory_bp.route('/new-product-entry', methods=["POST"])
def add_product_to_inventory():
     if request.method == 'POST':
        
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid data!"}), 400

        required_product = Product.query.filter_by(id=data['product_id']).first()
        if not required_product:
            return jsonify({"error": f"Product with id {data['product_id']} not found!"}), 404

        new_inventory_entry = Inventory(
            purchase_price = data['purchase_price'],
            max_qty = data['max_qty'],
            available_qty = data['available_qty'],
            reorder_level = data['reorder_level'],
            reorder_qty = data['reorder_qty'],
            shelf_no = data['shelf_no'],
            exp_date = datetime.fromisoformat(data['exp_date']),
            is_available = data['is_available'],
            product = required_product
        )
        db.session.add(new_inventory_entry)
        db.session.commit()
        return jsonify({"message": f"Product added to the Inventory successfully!"}), 201

@inventory_bp.route('/edit-product-entry/<int:id>', methods=["PUT"])
def edit_existing_product_entry_in_inventory(id):
    if request.method == 'PUT':

        fetched_inventory_entry = db.session.get(Inventory, id)
        if not fetched_inventory_entry:
            return jsonify({'error': f"Inventory entry with id {id} not found"}), 404
        
        data = request.get_json()

        if not data:
            return jsonify({"error": "Invalid data!"}), 400

        # Update fields only if they are present in the request body
        if 'product_id' in data:
            product_to_assign = Product.query.get(data['product_id'])
            if not product_to_assign:
                return jsonify({'error': f'Product with id {data['product_id']} not found'}), 404
            fetched_inventory_entry.product = product_to_assign

        if 'purchase_price' in data:
            fetched_inventory_entry.purchase_price = data['purchase_price']
        if 'max_qty' in data:
            fetched_inventory_entry.max_qty = data['max_qty']
        if 'available_qty' in data:
            fetched_inventory_entry.available_qty = data['available_qty']
        if 'reorder_level' in data:
            fetched_inventory_entry.reorder_level = data['reorder_level']
        if 'reorder_qty' in data:
            fetched_inventory_entry.reorder_qty = data['reorder_qty']
        if 'shelf_no' in data:
            fetched_inventory_entry.shelf_no = data['shelf_no']
        if 'is_available' in data:
            fetched_inventory_entry.is_available = data['is_available']
            
        if 'exp_date' in data:
            try:
                fetched_inventory_entry.exp_date = datetime.fromisoformat(data['exp_date'])
            except ValueError:
                return jsonify({"error": "Invalid expiration date format. Use ISO 8601 format (YYYY-MM-DDTHH:MM:SS)"}), 400       
                   
        db.session.commit()
        return jsonify({'message': 'Inventory entry updated successfully!'}), 200


@inventory_bp.route('/delete/<int:id>', methods=["DELETE"])
def delete_inventory_by_id(id):
    if request.method == 'DELETE':
        selected_inventory = db.session.get(Inventory, id)
        if not selected_inventory:
            return jsonify({'error': f"Inventory with id {id} not found"}), 404
        
        db.session.delete(selected_inventory)
        db.session.commit()

        return jsonify({'message': 'Inventory deleted successfully!'}), 200
