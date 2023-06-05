from flask import Blueprint, request, jsonify, g
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta, datetime
from flask_mail import Message
from werkzeug.exceptions import BadRequest
import jwt, string
# import datetime
import os
import random

category_product_bp = Blueprint('category_product',__name__)
@category_product_bp.get('/category-product/<service_category_id>')
def category_product(service_category_id):
    try:
        if not service_category_id:
            return jsonify({"error":"Enter valid service category id"})
        cursor = g.db.cursor(dictionary=True)
        if service_category_id == '2':
            cursor.execute(f"SELECT p.id,p.product_name, p.price, p.quantity, p.product_unit,(SELECT pi.image FROM tbl_product_image pi WHERE pi.product_id = p.id LIMIT 1) AS Product_image from tbl_category_product p WHERE p.service_category_id={service_category_id} AND p.is_active = 1 AND p.is_delete = 0;")
            data = cursor.fetchall()
            cursor.execute(f"SELECT id, facility_name, facility_charges FROM tbl_additional_facility WHERE id=1 AND is_active=1 AND is_delete=0 ")
            additional_data = cursor.fetchall()
            g.db.commit()
            return jsonify({"product_details":data, "additional_facility":additional_data})
        else:
            cursor.execute(f"SELECT p.id,p.product_name, p.price, p.quantity, p.product_unit,(SELECT pi.image FROM tbl_product_image pi WHERE pi.product_id = p.id LIMIT 1) AS Product_image from tbl_category_product p WHERE p.service_category_id={service_category_id} AND p.is_active = 1 AND p.is_delete = 0;")
            data = cursor.fetchall()
            g.db.commit()
            return jsonify(data), 200
    except Exception as e:
        return jsonify({"error":f"{e}"})

@category_product_bp.get('/category-product-details/<product_id>')
def category_product_details(product_id):
    try:
        cursor = g.db.cursor(dictionary=True)
        cursor.execute(f"SELECT service_category_id FROM tbl_category_product WHERE id={product_id} AND is_active=1 AND is_delete=0;")
        data = cursor.fetchone()
        service_category_id = data['service_category_id']
        cursor.execute(f"SELECT image FROM tbl_product_image WHERE product_id={product_id} AND is_active=1 AND is_delete=0 ")
        product_image = cursor.fetchall()
        if service_category_id == 2:
            cursor.execute(f"SELECT p.product_name, s.name as storename, p.price, p.product_unit, p.quantity FROM tbl_category_product p JOIN tbl_store s ON p.store_id = s.id WHERE p.id={product_id} AND p.is_active=1 AND p.is_delete=0;")
            product_details = cursor.fetchall()
            cursor.execute(f"SELECT facility_name, facility_charges FROM tbl_additional_facility WHERE id != 0")
            additional_facility = cursor.fetchall()
            return jsonify({"product_images": product_image, "product and store details": product_details, "additional_facility": additional_facility})
        else:
            cursor.execute(f"SELECT p.product_name, p.price, p.product_unit, p.quantity, p.description FROM tbl_category_product p WHERE p.id={product_id} AND p.is_active=1 AND p.is_delete=0;")
            product_details = cursor.fetchall()
            # return jsonify(product_image, product_details)
            return jsonify({"product_images":product_image, "product and store details":product_details})
    except Exception as e:
        return jsonify({"error": f"{e}"})
