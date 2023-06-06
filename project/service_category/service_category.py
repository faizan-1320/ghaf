import json
import pytz
from datetime import datetime, timedelta
import datetime
from flask import Blueprint, app, request, jsonify, g
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
from flask import Flask
from datetime import timedelta
from werkzeug.utils import secure_filename
from flask_mysql_connector import MySQL

import random

app = Flask(__name__)


fish_market_category_bp = Blueprint('fish_market_category', __name__)
blacklist = set()


@fish_market_category_bp.post("/market_category/<int:category>")
def market_category(category):
    cursor = g.db.cursor()
    cursor.execute(f"SELECT * FROM `tbl_service` where  id = {category}")
    service = cursor.fetchone()
    if service is None:
        return jsonify({'Error': "enter valid category"}), 400
    elif service[0] == 1 or 2:
        tz_NY = pytz.timezone('Asia/Kolkata')
        datetime_NY = datetime.now(tz_NY)
        India_time = datetime_NY.strftime("%H:%M:%S")
        India_day = datetime_NY.strftime("%A")
        cursor = g.db.cursor(dictionary=True)
        query = f"""SELECT
            tbl_service_category.category_name,
            tbl_service_category.category_image,
            CASE
                WHEN (
                    tbl_market_timeing.openday = '{India_day}'
                    AND tbl_market_timeing.opentime < '{India_time}'
                    AND tbl_market_timeing.closetime >= '{India_time}'
                ) THEN
                    tbl_market_timeing.closetime
                ELSE
                    tbl_market_open_at.open_datetime
            END AS shoptime
        FROM
            tbl_service
        LEFT JOIN
            tbl_service_category ON tbl_service_category.service_id = tbl_service.id
        LEFT JOIN
            tbl_market_timeing ON tbl_market_timeing.market_id = tbl_service_category.id
        LEFT JOIN
            tbl_market_open_at ON tbl_market_open_at.market_id = tbl_service_category.id
        WHERE
            tbl_market_timeing.openday = '{India_day}'
            AND tbl_service.id = {category}"""
        cursor.execute(query)
        USER = cursor.fetchall()
        return jsonify({'Success': USER}), 200
    else:
        return jsonify({'Error': "enter valid details"}), 400
