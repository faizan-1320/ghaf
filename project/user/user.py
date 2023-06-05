from flask import Blueprint, request, jsonify, g
from werkzeug.utils import secure_filename
from flask_jwt_extended import jwt_required,get_jwt_identity,jwt_required
import os
from werkzeug.security import check_password_hash, generate_password_hash
from random import randint
from flask_mail import Mail, Message

user_bp = Blueprint('user', __name__)

def is_user(user_id):
    cur = g.db.cursor()
    cur.execute(f"select user_type from tbl_users where id={user_id}")
    user = cur.fetchone()
    if user:
        if user[0] == 'user':
            return True
        return False
    


def is_admin(user_id):
    cur = g.db.cursor()
    cur.execute(f"select user_type from tbl_users where id={user_id}")
    user = cur.fetchone()
    if user:
        if user[0] == 'admin':
            return True
        return False



#--------------------------------------------------page.38---------------------------------------------

@user_bp.get('/home_screen')
@jwt_required()
def home_screen():
    try:
        user_id=get_jwt_identity()

        if not is_user(user_id):
            return jsonify({"error":"Unauthrized Access"}),401
        
        cursor=g.db.cursor(dictionary=True)

        cursor.execute('SELECT prefix,firstname FROM tbl_users WHERE is_active= 1 AND is_delete=0 AND is_verify=1 AND id = %s',(user_id,))

        user=cursor.fetchone()

        import time    
        import datetime
        currentTime = time.strftime('%H:%M') 
        currentTime = datetime.datetime.now()

        if 6 <= currentTime.hour < 12 :
            time_u=('Good morning')

        elif 12 <= currentTime.hour < 16:
            time_u=('Good afternoon')

        elif 16 <= currentTime.hour < 22 :
            time_u=('Good evening')

        else:
             time_u=('Good night')

        cursor.execute('SELECT id,service FROM tbl_service')
        user_service = cursor.fetchall()

        cursor.execute('SELECT image,tital,description FROM tbl_announcement')
        user_announcement = cursor.fetchall()

        if user:
            return jsonify({"user":time_u,
                            "name":user,
                            "announcement":user_announcement,
                            "Service":user_service}),200
        
    except Exception as e:
        return jsonify({"Error": str(e) }),400
    



#-------Announcement---------------------page.41----------------------------

@user_bp.post('/announcement')
@jwt_required()
def announcement():
    try:
        user_id=get_jwt_identity()

        if not is_admin(user_id):
            return jsonify({"error":"Unauthrized Access"}),401
        
        cursor=g.db.cursor()

        avatar = request.files['image']
        if not avatar: 
            return jsonify({'Error': 'Image Required'})
        
        filename = secure_filename(avatar.filename)

        avatar.save(os.path.join('project/media',filename))

        titel = request.form.get('titel')

        description = request.form.get('descipation')
      
        if not titel: 
            return jsonify({'Error': 'Titel Required'})
        
        if not description:
            return jsonify({'Error': 'Descipation Required'})


        cursor.execute('INSERT INTO tbl_announcement (image,tital,description) VALUES (%s, %s, %s)',
                        (filename,titel,description))
        g.db.commit()

        return jsonify({'Meassage' : 'Announcement Successfully'}),200
        
    except Exception as e:
        return jsonify({"Error": str(e) }),400
    



@user_bp.get('/announcement_list')
@jwt_required()
def announcement_list():
    try:
        cursor = g.db.cursor()
        cursor.execute('SELECT image,tital,description FROM tbl_announcement')
        user = cursor.fetchall()
        return jsonify(user)
    except Exception as e:
        return jsonify({"Error": str(e) }),400
    


@user_bp.post('/competition_answer/<id>')
@jwt_required()
def competition_answer(id):
    try:
        user_id = get_jwt_identity()

        if not is_user(user_id):
                return jsonify({"error":"Unauthrized Access"}),401

        cursor = g.db.cursor()
        cursor.execute(f'SELECT id, question FROM tbl_questions WHERE id={id}')
        user = cursor.fetchone()   
        print(user)

        if not user:
            return jsonify({'Error': 'Not Found Question'}),400

        question_id = user[0]  
        answer = request.json.get('answer')

        if not answer:
            return jsonify({'Error': 'Answer Required'})

        cursor.execute('INSERT INTO tbl_question_answer(question_id,user_id,answer) VALUES (%s, %s, %s)',
                            (question_id,user_id,answer))
        g.db.commit()
        return jsonify({'Message' : 'Answer Successfully Insert'}),200
    
    except Exception as e:
        return jsonify({"Error": str(e) }),400
 

@user_bp.get('/user_notification')
@jwt_required()
def user_notification():
    try:
        user_id = get_jwt_identity()

        if not is_user(user_id):
                    return jsonify({"error":"Unauthrized Access"}),401
        
        cursor = g.db.cursor(dictionary=True)
        cursor.execute('SELECT notification_title,notification_description,created_at FROM tbl_notification')
        user = cursor.fetchall()

        for users in user:
            users['created_at'] = str(users['created_at'])

        return jsonify(user),200
    
    except Exception as e:
        return jsonify({"Error": str(e) }),400

otp = randint(0000, 9999)
u_otp = str(otp)

@user_bp.post('/edit_profile_user')
@jwt_required()
def edit_profile_user():
    try:
        user_id = get_jwt_identity()
        if not is_user(user_id):
                return jsonify({"error":"Unauthrized Access"}),401
        
        cursor = g.db.cursor()
        cursor.execute('SELECT id FROM tbl_users WHERE id=%s',(user_id,))
        user = cursor.fetchone()
        print(user)
        u_id = user[0]
        print(u_id)

        if not user:
            return jsonify({'Error': 'User Not Found'}),401

        prefix = request.json.get('prefix')
        firstname = request.json.get('firstname')
        lastname = request.json.get('lastname')
        nationality = request.json.get('nationality')
        dob = request.json.get('dob')
        gender = request.json.get('gender')
        email = request.json.get('email')
        phone_code = request.json.get('phone_code')
        phone_number = request.json.get('phone_number')

        if prefix not in ['Mr','Mrs','Miss','Ms']:
                return jsonify({"Message": "Prefix Must Be Mr,Mrs,Miss Or Ms"}), 400
        
        if not firstname:
            return jsonify({'error': 'Firstname Required'}), 400
        
        if not lastname:
            return jsonify({'error': 'lastname Required'}), 400
        
        if nationality:
            cursor.execute(f'SELECT id,country FROM tbl_country WHERE id = {nationality}')
            user = cursor.fetchall()
            print("country_List..............................",user)
            if user:
                pass
            else:
                return jsonify({'Message': 'Country Not Found'}),400
            
        if not nationality:
            return jsonify({'error': 'Nationality Required'}), 400
        
        if not dob:
            return jsonify({'error': 'Date Of Birth Required'}), 400
        
        if gender not in ['male','female']:
                return jsonify({"Message": "Gender Must Be male And female"}), 400
        
        if not email:
            return jsonify({'error': 'Email Required'}), 400
        
        if not phone_code:
            return jsonify({'error': 'Phone_code Required'}), 400
        
        if not phone_number:
            return jsonify({'error': 'Phone_number Required'}), 400
        

        cursor.execute(f"""UPDATE tbl_users set prefix = '{prefix}', firstname = '{firstname}',
                        lastname = '{lastname}' , nationality = {nationality},
                        dob = '{dob}', gender = '{gender}', email = '{email}',
                        phone_code = '{phone_code}', phone_number = '{phone_number}' WHERE id = {u_id}""")
        g.db.commit()

        cursor.execute('SELECT id FROM tbl_users WHERE is_active=1 AND is_delete=0 AND email=%s',(email,))
        user =cursor.fetchall()
        id = user[0]
        print("bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb")
        print(user)
        print(id)
        print(id[0])
        
        from project import mail
    
        msg = Message(
                    'otp',
                    sender='jigoprajapati01@gmail.com',
                    recipients=['jigoprajapati01@gmail.com']
                )
        msg.body = u_otp

        cursor = g.db.cursor()
        
        cursor.execute('INSERT INTO tbl_user_otp (user_id,otp) VALUES (%s,%s)',(id[0],u_otp,))
        
        g.db.commit()  
        mail.send(msg)

        return jsonify({'Message': 'User Profile Complete'})
    
    except Exception as e:
        return jsonify({"Error": str(e) }),400



@user_bp.post('/user_otp')
def user_otp():
    try:
        data = request.json
        u_otp =  data.get('otp')
        print("otp",type(u_otp))

        cursor = g.db.cursor()
        cursor.execute('SELECT o.otp,o.user_id FROM tbl_user_otp o JOIN tbl_users tu ON o.user_id = tu.id WHERE o.otp = %s ', (u_otp,))
        result = cursor.fetchone()
        
        if not u_otp:
            return jsonify({"message": "OTP are Insert"}), 400

        if result:
            if result[0] == int(u_otp):
                u = result[1]
                verify = 1
                cursor = g.db.cursor()

                cursor.execute(f'UPDATE tbl_users SET is_verify={verify} WHERE id={u}')

                cursor.execute(f'UPDATE tbl_user_otp SET otp = NULL WHERE user_id={u}')

                g.db.commit()

                return jsonify({'message': 'otp successfully matched'}), 201
            else:
                return jsonify({'message': "otp Not match"}),400
        else:
            return jsonify({'message': "otp Not found"}),400
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@user_bp.post('/change_password_user')
@jwt_required()
def change_password_user():
    try:
        id = get_jwt_identity()

        if not is_user(id):
                return jsonify({"error":"Unauthrized Access"}),401
        
        data = request.json
    
        old_password = data.get('old_password')
        new_password = data.get('new_password')

        if not old_password:
            return jsonify({"Meassge": " old password field is required"}), 400

        if not new_password:
            return jsonify({"Meassge": "New Password field is required"}), 400

        cursor = g.db.cursor()
        cursor.execute('select password from tbl_users WHERE id = %s', (id,))
        user = cursor.fetchone()
        
        if user:
            old_pass = check_password_hash(user[0], old_password)
            new_pass = check_password_hash(user[0], new_password)

            if old_pass == new_pass:
                return jsonify({"Message": "old password in new password can not be same."}), 400
            
            if old_pass:
                pwd_hash = generate_password_hash(new_password, method='sha256', salt_length=8)
                cursor.execute('UPDATE tbl_users set password = %s WHERE id = %s', (pwd_hash, id))
                g.db.commit()

                if cursor.rowcount == 1:
                    return jsonify({'message': 'Seccessfully password updated'}), 200

        return jsonify({"message": "Old Password is Wrong"}), 401
    
    except Exception as e:
        return jsonify({"Error": str(e) }),400
    
@user_bp.get('/user_favourites')
@jwt_required()
def user_favourites():
    try:

        id = get_jwt_identity()
        if not is_user(id):
                    return jsonify({"error":"Unauthrized Access"}),401
        
        cursor = g.db.cursor(dictionary=True)
        cursor.execute(f"""SELECT cp.product_name,cp.price,cp.product_unit,pi.image FROM tbl_user_favorite uf 
                        JOIN tbl_category_product cp ON uf.product_id = uf.id 
                        JOIN tbl_product_image pi ON pi.product_id = cp.id WHERE uf.user_id={id}""")
        user = cursor.fetchall()
        if not user:
            return jsonify({'Message' : 'User Undefined'})
        return jsonify(user),200
    except Exception as e:
        return jsonify({"Error": str(e) }),400





