from flask import request, jsonify
from app import app, db
from app.user_management import UserManager
from app.inventory import update_inventory
from app.sales import register_sale, add_sale_detail
from app.purchases import register_purchase, add_purchase_detail
from app.reports import generate_sales_report
from app.schemas import UserSchema, LoginSchema
from marshmallow import ValidationError
from app.auth import generate_token
from unittest.mock import patch

@app.route('/')
def index():
    return "Bienvenido al Sistema de Gestión de Inventario"

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    # ...validación...
    UserManager.register_user(data['email'], data['password'], data['name'])
    return jsonify({"message": "User registered successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = UserManager.authenticate_user(data['email'], data['password'])
    if user:
        # ...
        pass

@app.route('/inventory/update', methods=['POST'])
def update_inventory_route():
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity')
    movement_type = data.get('movement_type')
    user = data.get('user')
    description = data.get('description')
    reference_document = data.get('reference_document')
    update_inventory(product_id, quantity, movement_type, user, description, reference_document)
    return jsonify({"message": "Inventory updated successfully"}), 200

@app.route('/sales/register', methods=['POST'])
def register_sale_route():
    data = request.get_json()
    client = data.get('client')
    payment_method = data.get('payment_method')
    user = data.get('user')
    sale_id = register_sale(client, payment_method, user, db)

    for detail in data.get('details', []):
        add_sale_detail(sale_id, detail['product_id'], detail['quantity'], detail['price_unit'], detail['discount'])
    return jsonify({"message": "Sale registered successfully"}), 201

@app.route('/purchases/register', methods=['POST'])
def register_purchase_route():
    data = request.get_json()
    supplier_id = data.get('supplier')  # Cambiar 'supplier' a 'supplier_id'

    user = data.get('user')
    details = data.get('details', [])
    
    for detail in details:
        product_id = detail['product_id']
        quantity = detail['quantity']
        price_unit = detail['price_unit']
        cost = quantity * price_unit
        purchase_id = register_purchase(product_id, quantity, supplier_id, cost, db)  # Asegurarse de que se pase supplier_id


        
        if purchase_id:
            add_purchase_detail(purchase_id, product_id, quantity, price_unit)
    
    return jsonify({'message': 'Purchase registered successfully', 'purchase_id': purchase_id}), 201

@app.route('/reports/sales', methods=['GET'])
def generate_sales_report_route():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    report = generate_sales_report(start_date, end_date)
    return jsonify({"report": report}), 200
