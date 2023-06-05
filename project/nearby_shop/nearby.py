from flask import Blueprint, request, jsonify, g, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


nearby_bp = Blueprint('nearby', __name__)


@nearby_bp.get('/select-location')
@jwt_required()
def get_select_location():
    user_id = get_jwt_identity()
    cursor = g.db.cursor()
    cursor.execute(
        f"SELECT id, user_id, address_type, property_type, property_number, street, landmark, area, city FROM "
        f"tbl_user_address WHERE is_active=1 AND is_delete=0 AND user_id='{user_id}'")
    user = cursor.fetchall()
    if user:
        columns = [column[0] for column in cursor.description]
        results = []
        for row in user:
            results.append(dict(zip(columns, row)))
        # print(results)
        return jsonify(results), 200
    else:
        return jsonify({"message": "user not found"}), 200


@nearby_bp.get('/stores-nearby/<add_id>')
@jwt_required()
def get_stores_nearby(add_id):
    try:
        user_id = get_jwt_identity()
        cursor = g.db.cursor(dictionary=True)

        cursor.execute(
            f"SELECT latitude, longitude FROM tbl_user_address WHERE is_active = 1 AND is_delete = 0 AND user_id = {user_id} and id = {add_id} "
        )
        user_location = cursor.fetchone()
        if not user_location:
            return jsonify({'error': 'User address not found'}), 400

        user_latitude = user_location['latitude']
        user_longitude = user_location['longitude']

        cursor.execute(
            f"SELECT s.id, s.name, ROUND(6371 * 2 * ASIN(SQRT(POWER(SIN((RADIANS({user_latitude}) - RADIANS("
            f"s.latitude)) / 2), 2) + COS(RADIANS({user_latitude})) * COS(RADIANS(s.latitude)) * POWER(SIN((RADIANS("
            f"{user_longitude}) - RADIANS(s.longitude)) / 2), 2))), 2) AS distance_km FROM tbl_store AS s WHERE "
            f"s.is_active = 1 AND s.is_delete = 0 HAVING distance_km < 9 "
        )
        stores_nearby = cursor.fetchall()

        cursor.fetchall()

        return jsonify(stores_nearby), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@nearby_bp.get('/select-store/<store_id>')
@jwt_required()
def get_select_store(store_id):
    cursor = g.db.cursor()
    cursor.execute(f"""
                    SELECT s.image, s.name, st.day, st.start_time, st.end_time, s.address,
                           CASE
                               WHEN TIME_TO_SEC(st.end_time) - TIME_TO_SEC(st.start_time) > 0 THEN 'OPEN'
                               ELSE 'CLOSED'
                           END AS status
                    FROM tbl_store s
                    JOIN tbl_store_timing st ON st.store_id = s.id
                    WHERE st.day = CASE
                        WHEN DAYNAME(NOW()) = 'Sunday' THEN 'Sunday'
                        WHEN DAYNAME(NOW()) = 'Monday' THEN 'Monday'
                        WHEN DAYNAME(NOW()) = 'Tuesday' THEN 'Tuesday'
                        WHEN DAYNAME(NOW()) = 'Wednesday' THEN 'Wednesday'
                        WHEN DAYNAME(NOW()) = 'Thursday' THEN 'Thursday'
                        WHEN DAYNAME(NOW()) = 'Friday' THEN 'Friday'
                        WHEN DAYNAME(NOW()) = 'Saturday' THEN 'Saturday'
                    END
                    AND s.id = {store_id};
                    """)
    store = cursor.fetchone()
    if store:
        store_dict = {
            "image": store[0],
            "name": store[1],
            "day": store[2],
            "start_time": str(store[3]),
            "end_time": str(store[4]),
            "address": store[5],
            "status": store[6]
        }
        return jsonify(store_dict), 200
