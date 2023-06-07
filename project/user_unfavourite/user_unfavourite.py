from flask import Blueprint, jsonify, g, request, Flask
from flask_jwt_extended import jwt_required, JWTManager, get_jwt_identity

user_unfavourite_bp = Blueprint('unfavourite', __name__)


@user_unfavourite_bp.post("/user-unfavourite")
@jwt_required()
def user_unfavourite():
    user_id = get_jwt_identity()
    product_id = request.json.get("product_id")
    # print(product_id)
    if not product_id:
        return jsonify({"error": "Product id is required."}), 400
    cursor = g.db.cursor()
    cursor.execute(
        f"SELECT * from tbl_category_product WHERE id='{product_id}'")
    product = cursor.fetchone()
    if product:
        cursor = g.db.cursor()
        cursor.execute(
            f"SELECT * FROM tbl_user_favorite WHERE user_id='{user_id}' AND product_id='{product_id}' AND is_active=1;"
        )
        user_favourite = cursor.fetchone()
        if user_favourite:
            cursor = g.db.cursor()
            cursor.execute(
                f"UPDATE tbl_user_favorite SET is_active=0 WHERE user_id='{user_id}' AND product_id='{product_id}'"
            )
            g.db.commit()
            return jsonify(
                {"messege": "Remove product from favourite list."}), 501
        else:
            return jsonify({
                "error":
                "This product does not into favourite list by perticuler user."
            }), 400
    else:
        return jsonify({"error": "No such product found"}), 400
