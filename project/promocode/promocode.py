from flask import Blueprint, jsonify, g, request, Flask
from datetime import datetime

promocode_bp = Blueprint('promocode', __name__)


@promocode_bp.get("/show-promocode")
def show_promocode():
    cursor = g.db.cursor(dictionary=True)
    cursor.execute(
        f"SELECT id,coupon_image,promocode,discription,expire_time,discount_type,discount_value from tbl_promocode WHERE CURRENT_TIMESTAMP < expire_time;")
    coupons = cursor.fetchall()
    if coupons:
        return jsonify({"Show_promocodes": coupons})

    else:
        return jsonify({"messege": "Every coupones hase been expired."})
