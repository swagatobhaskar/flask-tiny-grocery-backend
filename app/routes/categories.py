from flask import Blueprint, jsonify, request

from app.extensions import db
from app.models import Category

category_bp = Blueprint('category', '__name__')

@category_bp.route('/')
def category_home():
    return jsonify({'message': 'This is the category home.'}), 200

@category_bp.route('/list-view', methods=['GET'])
def get_all_ategories():
    all_categories = Category.query.all()
    return jsonify([category.get_list_view() for category in all_categories]), 200

@category_bp.route('/detail-view/<int:id>', methods=["GET"])
def get_category_detail(id):
    selected_category = Category.query.filter_by(id=id).first()
    if not selected_category:
            return jsonify({'error': f"Category with id {id} not found"}), 404
    return jsonify(selected_category.get_detail_view()), 200

@category_bp.route('/add-new', methods=["POST"])
def add_new_category():
    if request.method == "POST":
        data = request.get_json()

        new_category = Category(
            name = data['name'],
            description = data['description']
        )
        db.session.add(new_category)
        db.session.commit()
        return jsonify({"message": f"Category {data['name']} added successfully!"}), 201
    

@category_bp.route('/edit/<int:id>', methods=["PUT"])
def edit_category(id):
    if request.method == 'PUT':
        fetched_category = db.session.get(Category, id)
        if not fetched_category:
            return jsonify({'error': f"Category with id {id} not found"}), 404
        
        data = request.get_json()
        # print("DATA::", data)
        if not data:
            return jsonify({"error": "Invalid data!"}), 400

        # Update fields only if they are present in the request body
        if 'name' in data:
            fetched_category.name = data['name']
        if 'description' in data:
            fetched_category.description = data['description']
        
        db.session.commit()
        return jsonify({'message': 'Category updated successfully!'}), 200


@category_bp.route('/delete/<int:id>', methods=["DELETE"])
def delete_product_by_id(id):
    if request.method == 'DELETE':
        selected_category = db.session.get(Category, id)
        if not selected_category:
            return jsonify({'error': f"Category with id {id} not found"}), 404
        
        db.session.delete(selected_category)
        db.session.commit()

        return jsonify({'message': 'Category deleted successfully!'}), 200
