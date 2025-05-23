from flask import Blueprint, request, jsonify
from app.status_codes import HTTP_400_BAD_REQUEST,HTTP_200_OK,HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_500_INTERNAL_SERVER_ERROR
import validators
from app.models.product import Product  # Correct: import the class with proper name
from app.extensions import db

# Product Blueprint
product = Blueprint('product', __name__, url_prefix='/api/v1/product')

@product.route('/create', methods=['POST'])
def create_product():
    try:
        data = request.get_json()
        name = data.get('name')
        quantity = data.get('quantity')
        price = data.get('price')
        description = data.get('description')

        # Validations
        if not all([name, price, quantity, description]):
            return jsonify({"error": "All fields are required"}), HTTP_400_BAD_REQUEST

        if not isinstance(price, (int, float)) or price <= 0:
            return jsonify({"error": "Price must be a positive number"}), HTTP_400_BAD_REQUEST

        if not isinstance(quantity, int) or quantity < 0:
            return jsonify({"error": "Quantity must be a positive integer"}), HTTP_400_BAD_REQUEST

        # Create new product
        new_product = Product(
            name=name,
            quantity=quantity,
            price_unit=price,  # Fix: Your model uses 'price_unit' not 'price'
            description=description
        )

        db.session.add(new_product)
        db.session.commit()

        return jsonify({
            'message': f"{name} has been successfully created",
            'product': {
                "id": new_product.id,
                "name": new_product.name,
                "price": new_product.price_unit,  # Fix: Return 'price_unit'
                "quantity": new_product.quantity,
                "description": new_product.description,
                "created_at": new_product.created_at.isoformat() if new_product.created_at else None
            }
        }), HTTP_201_CREATED

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR


@product.route('/', methods=['GET'])
def get_all_products():

    try:
        # to retrieve all the products
        products = Product.query.all()

        # convert product to the list of dictionaries
        product_list = []
        for p in products:
            product_list.append({
                "id": p.id,
                "name": p.name,
                "price": p.price_unit,
                "quantity": p.quantity,
                "description": p.description,
                "created_at": p.created_at.isoformat() if p.created_at else None
            })
        return jsonify({
            "products": product_list,
            "count": len(product_list)
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@product.route('/<int:id>', methods=['DELETE'])  # <- Remove 'delete/' here
def delete_product(id):
    try:
        product_to_delete = Product.query.get(id)
        
        if not product_to_delete:
            return jsonify({"error": "Product not found"}), HTTP_404_NOT_FOUND

        db.session.delete(product_to_delete)
        db.session.commit()

        return jsonify({
            "message": f"Product '{product_to_delete.name}' deleted successfully",
            "id": id
        }), HTTP_200_OK

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
    



# update new information
@product.route('/<int:id>', methods=['PUT'])  # RESTful URL pattern
def update_product(id):
    try:
        # Get the product to update
        product_to_update = Product.query.get(id)
        
        if not product_to_update:
            return jsonify({"error": "Product not found"}), HTTP_404_NOT_FOUND

        data = request.get_json()

        # Validate input data
        if not data:
            return jsonify({"error": "No update data provided"}), HTTP_400_BAD_REQUEST

        # Update fields (only modify provided values)
        if 'name' in data:
            product_to_update.name = data['name']
        
        if 'price' in data:
            # Validate price
            if not isinstance(data['price'], (int, float)) or data['price'] <= 0:
                return jsonify({"error": "Price must be a positive number"}), HTTP_400_BAD_REQUEST
            product_to_update.price_unit = data['price']  # Match your model's field name
        
        if 'quantity' in data:
            # Validate quantity
            if not isinstance(data['quantity'], int) or data['quantity'] < 0:
                return jsonify({"error": "Quantity must be a non-negative integer"}), HTTP_400_BAD_REQUEST
            product_to_update.quantity = data['quantity']
        
        if 'description' in data:
            product_to_update.description = data['description']

        # Automatically updates 'updated_at' via your model's onupdate
        db.session.commit()

        return jsonify({
            "message": "Product updated successfully",
            "product": {
                "id": product_to_update.id,
                "name": product_to_update.name,
                "price": product_to_update.price_unit,
                "quantity": product_to_update.quantity,
                "description": product_to_update.description,
                "updated_at": product_to_update.updated_at.isoformat() if product_to_update.updated_at else None
            }
        }), HTTP_200_OK

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
    