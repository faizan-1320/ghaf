from flask import Blueprint, jsonify, g, request, Flask
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity


user_favourite_bp = Blueprint('favourite', __name__)


@user_favourite_bp.post("/user-favourite/<id>")
def user_favourite(id):
    user_id = id
    cursor = g.db.cursor()
    cursor.execute(
        f"SELECT id as user_id from tbl_users WHERE id = '{user_id}';")
    user = cursor.fetchone()
    # print(user)
    if user:
        product_id = request.json.get("product_id")
        print(product_id)
        if not product_id:
            return jsonify({"error": "Product id is required."}), 400
        cursor = g.db.cursor()
        cursor.execute(
            f"SELECT * from tbl_category_product WHERE id='{product_id}'")
        product = cursor.fetchone()
        if product:
            cursor = g.db.cursor()
            cursor.execute(
                f"SELECT * from tbl_user_favorite WHERE user_id='{user_id}' AND product_id='{product_id}' AND is_active=1;"
            )
            user_favourite = cursor.fetchone()
            if user_favourite:
                return jsonify({
                    "error":
                    f"This user allready added this item into favourite list."
                })
            cursor = g.db.cursor()
            cursor = g.db.cursor()
            cursor.execute(
                f"SELECT * FROM tbl_user_favorite WHERE user_id='{user_id}' AND product_id='{product_id}'"
            )
            user_product = cursor.fetchone()
            if user_product:
                cursor = g.db.cursor()
                cursor.execute(
                    f"UPDATE tbl_user_favorite SET is_active=1 WHERE user_id='{user_id}' AND product_id='{product_id}'"
                )
                g.db.commit()
                return jsonify({"messege": "Add product into favourite."})
            cursor.execute(
                "INSERT INTO tbl_user_favorite(user_id, product_id,is_active) VALUES  (%s, %s,%s)",
                (user_id, product_id, 1))
            g.db.commit()
            return jsonify({"messege": "Add product into favourite."})
        else:
            return jsonify({"error": "No such product found"})
    else:
        return jsonify({"error": "No such user found"})
    

@user_favourite_bp.post("/user-favourite")
@jwt_required()
def user_favourite():
    user_id = get_jwt_identity()
    product_id = request.json.get("product_id")
    print(product_id)
    if not product_id:
        return jsonify({"error": "Product id is required."}), 400
    cursor = g.db.cursor()
    cursor.execute(
        f"SELECT * from tbl_category_product WHERE id='{product_id}'")
    product = cursor.fetchone()
    if product:
        cursor = g.db.cursor()
        cursor.execute(
            f"SELECT * from tbl_user_favorite WHERE user_id='{user_id}' AND product_id='{product_id}' AND is_active=1;"
        )
        user_favourite = cursor.fetchone()
        if user_favourite:
            return jsonify({
                "error":
                f"This user allready added this item into favourite list."
            })
        cursor = g.db.cursor()
        cursor = g.db.cursor()
        cursor.execute(
            f"SELECT * FROM tbl_user_favorite WHERE user_id='{user_id}' AND product_id='{product_id}'"
        )
        user_product = cursor.fetchone()
        if user_product:
            cursor = g.db.cursor()
            cursor.execute(
                f"UPDATE tbl_user_favorite SET is_active=1 WHERE user_id='{user_id}' AND product_id='{product_id}'"
            )
            g.db.commit()
            return jsonify({"messege": "Add product into favourite."})
        cursor.execute(
            "INSERT INTO tbl_user_favorite(user_id, product_id,is_active) VALUES  (%s, %s,%s)",
            (user_id, product_id, 1))
        g.db.commit()
        return jsonify({"messege": "Add product into favourite."})
    else:
        return jsonify({"error": "No such product found"})
