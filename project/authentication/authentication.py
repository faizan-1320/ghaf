from flask import Flask, session, url_for, redirect
from flask_mail import Mail, Message
from flask import Blueprint, request, jsonify, g
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, get_jwt
from flask import Blueprint, render_template, abort
import random
from datetime import datetime, timedelta
import datetime
import os
from werkzeug.utils import secure_filename

authentication_bp = Blueprint('auth', __name__)


def send_email(users):
    from project import mail
    otp = random.randint(1000, 9999)
    if users:
        user_id = users[0]
        msg = Message("Verification email", sender="jaybthakkar2305@gmail.com",
                      recipients=['jaybthakkar2305@gmail.com'])
        msg.body = f"{otp} is your OTP for user verification."
        mail.send(msg)
        from datetime import datetime, timedelta
        current_datetime = datetime.now()
        is_expire = current_datetime + timedelta(minutes=10)
        timestamp = is_expire.timestamp()
        rounded_timestamp = round(timestamp)
        print(rounded_timestamp)
        cursor = g.db.cursor()
        cursor.execute(
            f"INSERT INTO tbl_user_otp(user_id, otp, is_expire) VALUES('{user_id}', '{otp}', '{rounded_timestamp}')")
        g.db.commit()
        return "user ragister successfully"
    return "user not found"

# ------------------------------------select country---------------------------------


@authentication_bp.post('/select_country')
def select_country():
    try:
        try:
            data = request.json
        except:
            return jsonify({'error': 'data not found'}), 404

        country = data.get('country')
        currency = data.get('currency')
        language = data.get('language')

        if not country or not currency or not language:
            return jsonify({'error': 'Invalid data provided'}), 400

        cursor = g.db.cursor()
        cursor.execute(f"""SELECT tbl_country.country, tbl_currency.currency,
                           tbl_language.language FROM tbl_country
                           JOIN tbl_currency ON tbl_currency.country_id = tbl_country.id
                           JOIN tbl_language ON tbl_language.country_id = tbl_country.id
                           WHERE tbl_country.country = '{country}'
                           AND tbl_language.language = '{language}'
                           AND tbl_currency.currency = '{currency}'""")
        user = cursor.fetchone()

        if not user:
            return jsonify({'error': 'Data not found'}), 404

        return jsonify({"msg": user}), 200
    except:
        return jsonify({'error': 'Data not found'}), 404


# ------------------------------------register--------------------------------


@authentication_bp.post('/register')
def register():
    try:
        try:
            data = request.json
        except:
            return jsonify({'error': 'data not found'}), 404
        user_type = data.get('user_type')
        prefix = data.get('prefix')
        firstname = data.get('firstname')
        lastname = data.get('lastname')
        nationality = data.get('nationality')
        gender = data.get('gender')
        dob = data.get('dob')
        email = data.get('email')
        password = data.get('password')
        phone_code = data.get('phone_code')
        phone_number = data.get('phone_number')

        if user_type == '':
            return jsonify({'error': 'enter user_type'}), 400
        if user_type not in ['admin', 'user', 'guest']:
            return jsonify({'error': 'invalid user_type'}), 400
        if prefix == '':
            return jsonify({'error': 'enter prefix'}), 400
        if not prefix:
            return jsonify({'error': 'please enter prefix'}), 400
        if prefix not in ['Mr', 'Mrs', 'Miss', 'Ms']:
            return jsonify({'error': 'invalid prefix'}), 400
        if not firstname:
            return jsonify({'error': 'please enter firstname'}), 400
        if not lastname:
            return jsonify({'error': 'please enter lastname'}), 400
        if not nationality:
            return jsonify({'error': 'please enter nationality'}), 400
        if gender == '':
            return jsonify({'error': 'enter gender'}), 400
        if gender not in ['male', 'female']:
            return jsonify({'error': 'please enter gender'}), 400
        if not dob:
            return jsonify({'error': 'please enter dob'}), 400
        if not email:
            return jsonify({'error': 'please enter email'}), 400
        if not password:
            return jsonify({'error': 'please enter password'}), 400
        if not phone_code:
            return jsonify({'error': 'please enter phone number'}), 400
        if not phone_number:
            return jsonify({'error': 'please enter phone number'}), 400

        cursor = g.db.cursor()
        cursor.execute(f"SELECT * from tbl_users where email='{email}'")
        users = cursor.fetchone()
        password_hash = generate_password_hash(
            password, method='sha256', salt_length=8)
        if not users:
            cursor = g.db.cursor(buffered=True)
            cursor.execute(
                f"INSERT INTO tbl_users(user_type,prefix,firstname,lastname,nationality,gender,dob,email,password,phone_code,mobile_number) VALUES('{user_type}','{prefix}','{firstname}','{lastname}','{nationality}','{gender}','{dob}','{email}', '{password_hash}','{phone_code}','{phone_number}' )")
            cursor = g.db.cursor(buffered=True)
            cursor.execute(
                f"INSERT INTO tbl_users(user_type,prefix,firstname,lastname,nationality,gender,dob,email,password,phone_code,phone_number) VALUES('{user_type}','{prefix}','{firstname}','{lastname}','{nationality}','{gender}','{dob}','{email}', '{password_hash}','{phone_code}','{phone_number}' )")
            g.db.commit()
            cursor = g.db.cursor()
            cursor.execute(
                f"SELECT * from tbl_users where email='{email}' ORDER BY email DESC")
            users = cursor.fetchone()
            a = send_email(users)
            return jsonify({"msg": a}), 200
        return jsonify({'message': 'user already exist'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# ------------------------------------verify otp---------------------------------


@authentication_bp.post('/verify_otp/<user_id>')
def verifyotp(user_id):
    try:
        try:
            data = request.json
        except:
            return jsonify({'error': 'data not found'}), 404
        otp = data.get('otp')
        print(otp)
        if not otp:
            return jsonify({'error': 'otp required'}), 400
        cursor = g.db.cursor(dictionary=True)
        cursor.execute(
            f"SELECT otp,id,is_expire,user_id FROM tbl_user_otp WHERE user_id = {user_id} and is_active=1 ORDER by id DESC LIMIT 1")
        res = cursor.fetchone()
        print(res)
        from datetime import datetime, timedelta
        current_datetime = datetime.now()
        timestamp = current_datetime.timestamp()
        print(timestamp)
        rounded_timestamp = round(timestamp)
        print(rounded_timestamp)
        if res['is_expire'] > str(rounded_timestamp):
            print("sssss")
            if res:
                if int(otp) != int(res['otp']):
                    return jsonify({'message': 'otp not match'})
                print(res['user_id'])
                cursor.execute(
                    f"update tbl_user_otp set is_active = 0 where user_id={user_id}")
                cursor.execute(
                    f"update tbl_users set is_verify=1 where id={user_id}")
                g.db.commit()
                return jsonify({"successfull": "user is verified"})
            else:
                return jsonify({"message": "otp not verified"})
        else:
            return jsonify({"error": "enter otp is expire genrate new"})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# ------------------------------------login---------------------------------


@authentication_bp.post('/login')
def login():
    try:
        try:
            data = request.json
        except:
            return jsonify({'error': 'data not found'}), 404
        email = data.get('email')
        password = data.get('password')
        if not email:
            return jsonify({'error': 'please enter email'}), 400
        if not password:
            return jsonify({'error': 'please enter password'}), 400
        cursor = g.db.cursor(dictionary=True)
        cursor.execute(
            f"SELECT * FROM tbl_users WHERE email = '{email}' and is_verify=1")
        user = cursor.fetchone()
        print(user)
        if user:
            is_pass_correct = check_password_hash(user['password'], password)
            print(is_pass_correct)
            if is_pass_correct:
                access = create_access_token(identity=user['id'])
                return jsonify({
                    'user': {
                        'access': access,
                        'email': user['email']
                    }
                }), 200
            else:
                return jsonify({'error': 'Wrong credentital'}), 401
        else:
            return jsonify({'error': 'Wrong credentital'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 400


# ------------------------------------forgot password-------------------------------


@authentication_bp.post('/forgot_pwd')
def forgot_pwd():
    try:
        try:
            data = request.json
        except:
            return jsonify({'error': 'data not found'}), 404
        email = data.get("email")
        if not email:
            return jsonify({'error': 'email is required'}), 404
        cursor = g.db.cursor(dictionary=True)
        cursor.execute(
            f"select * from tbl_users where email='{email}' and is_active=1 and is_delete=0 and is_verify=1")
        user = cursor.fetchone()
        if user:
            from project import mail
            from datetime import datetime, timedelta
            current_datetime = datetime.now()
            is_expire = current_datetime + timedelta(minutes=10)
            timestamp = is_expire.timestamp()
            rounded_timestamp = round(timestamp)
            cursor.execute(
                f"UPDATE tbl_users SET forgot_exp={rounded_timestamp} where id={user['id']}")
            g.db.commit()
            hash_id = generate_password_hash(
                str(user['id']), method='sha256', salt_length=8)
            msg = Message('Hello', sender='mailto:jaybthakkar2305@gmail.com',
                          recipients=['jaybthakkar2305@gmail.com'])
            msg.body = f"click here to reset your password http://127.0.0.1:5000/reset_pwd/{hash_id}/{user['id']}"
            mail.send(msg)
            # print(f"{hash_id}/{user['id']}")
            return jsonify({"message": "Email Send Successfully"}), 200
        return jsonify({"error": "Enter valid Email"}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400


# ------------------------------------reset password---------------------------------


@authentication_bp.post('/reset_pwd/<hash_id>/<user_id>')
def reset_pwd(hash_id, user_id):
    try:
        is_id = check_password_hash(hash_id, user_id)
        if is_id:
            cursor = g.db.cursor(dictionary=True)
            cursor.execute(
                f"""SELECT password,forgot_exp FROM tbl_users WHERE id='{user_id}' AND is_active=1 AND is_delete=0 AND is_verify=1""")
            user = cursor.fetchone()
            # print(user)

            if user:
                if user['password'] is not None:
                    from datetime import datetime, timedelta
                    current_datetime = datetime.now()
                    timestamp = current_datetime.timestamp()
                    # print(timestamp)
                    rounded_timestamp = round(timestamp)
                    # print(rounded_timestamp)
                    print(user['forgot_exp'])
                    if user['forgot_exp'] > (rounded_timestamp):
                        print("p")
                        new_pwd = request.json.get('new_password')
                        if not new_pwd:
                            return jsonify({"error": "New password is required"}), 400
                        if new_pwd == user['password']:
                            return jsonify({"error": "New password must be different from the old password"}), 400

                        hash_pwd = generate_password_hash(
                            new_pwd, method='sha256', salt_length=8)
                        cursor.execute(
                            f"UPDATE tbl_users SET password='{hash_pwd}', forgot_exp=NULL WHERE id={user_id}")
                        g.db.commit()
                        return jsonify({"message": "Password updated successfully"}), 200
                    else:
                        return jsonify({'error': 'Your password reset link has expired'}), 400
                else:
                    return jsonify({"error": "User has not requested a password reset"}), 400
            else:
                return jsonify({"error": "User not found"}), 404
        else:
            return jsonify({"error": "Invalid user ID or hash ID"}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400


# ------------------------------------admin login---------------------------------

@authentication_bp.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        # try:
        email = request.form.get('email')
        password = request.form.get('password')
        cursor = g.db.cursor(buffered=True)
        cursor.execute(
            'SELECT id,prefix,firstname,lastname,email,phone_code,mobile_number,gender,dob,nationality FROM tbl_users WHERE user_type="admin"')
        admin = cursor.fetchone()
        session['email'] = admin
        # print(password,phone)
        if not email:
            empty_message = "Please Enter Email"
            return render_template('login.html', error_phone=empty_message)
            # return jsonify({"massage":"phone number or email missing required for login"})

        if not password:
            empty_password = "Please Enter Password"
            return render_template('login.html', error_password=empty_password)
            # return jsonify({"massage":"password missing password required"})

        cursor = g.db.cursor()
        cursor.execute(
            'select * from tbl_users where  email = %s and is_active = 1 and is_delete = 0 AND user_type="admin"', (email,))
        admin = cursor.fetchone()

        if admin:
            check_pass = check_password_hash(admin[9], password)
            if check_pass:
                if admin[14] == True:

                    return redirect(url_for('admin.dashboard'))
                else:
                    return jsonify({
                        "massage": "Admin is not verified",
                        "email": admin[4]
                    })
            error_data = "wrong credential"
            return render_template('login.html', error_data=error_data)
            # else:
            #     return({
            #         "error":"wrong credential"
            #     })
        else:
            error_admin = "Only Admin Can Login"
            return render_template('login.html', error=error_admin)
    else:
        return render_template('login.html')


@authentication_bp.route('/logout')
def logout():
    session.pop('email')
    return redirect(url_for('auth.admin_login'))
