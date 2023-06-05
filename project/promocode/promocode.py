from flask import Blueprint, jsonify, g, request, Flask
from datetime import datetime

promocode_bp = Blueprint('promocode', __name__)


@promocode_bp.get("/show-promocode")
def show_promocode():
    cursor = g.db.cursor(dictionary=True)
    cursor.execute(
        f"SELECT * from tbl_promocode WHERE CURRENT_TIMESTAMP < expire_time;")
    coupons = cursor.fetchall()
    if coupons:        
        return jsonify(coupons)
    else:
        return jsonify({"messege": "Every coupones hase been expired."})
