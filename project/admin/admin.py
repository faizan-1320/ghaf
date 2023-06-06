from flask import Blueprint,g,jsonify,request,render_template,redirect,url_for,session,flash
from werkzeug.utils import secure_filename
from flask_jwt_extended import jwt_required,get_jwt_identity,create_access_token #pip install flask-jwt-extended
import os
from enum import Enum

admin_bp=Blueprint('admin',__name__)

class gender(Enum):
    male='male'
    female='female'
# from project import app
@admin_bp.before_request
def before_request():
    g.email=None
    if 'email' in session:
            g.email=session['email']

# @admin_bp.get('/company-list', endpoint='company_list')
# def company_list():
#     if g.email:
#         cursor=g.db.cursor(dictionary=True)
#         cursor.execute('SELECT company_name,user_id,company_size,description,registration,logo,website,start_time,end_time,address FROM tbl_company')
#         cmopany=cursor.fetchall()
#         return render_template('company_list.html',cmopany=cmopany)
#     return redirect(url_for('auth.admin_login'))

@admin_bp.get('/dashboard')
def dashboard():
    if g.email:
        cursor=g.db.cursor(dictionary=True)
        cursor.execute('SELECT COUNT(id) AS total_user FROM tbl_users WHERE user_type!="admin" AND is_active=1 AND is_delete=0')
        user_count=cursor.fetchone()
        # print("this is email=====>",g.email['firstname'])
        cursor.execute('SELECT COUNT(id) AS total_store FROM tbl_store WHERE is_active=1 AND is_delete=0')
        store_count=cursor.fetchone()
        cursor.execute('SELECT COUNT(id) AS total_product FROM tbl_category_product WHERE is_active=1 AND is_delete=0')
        product_count=cursor.fetchone()
        cursor.execute('SELECT COUNT(id) AS total_service FROM tbl_service WHERE is_active=1 AND is_delete=0')
        service_count=cursor.fetchone()
        return render_template('index.html',user_count=user_count,service_count=service_count,store_count=store_count,product_count=product_count)
    return redirect(url_for('auth.admin_login'))

@admin_bp.get('/user')
def tables_data():
    if g.email:
        cursor=g.db.cursor(dictionary=True)
        cursor.execute('SELECT id,prefix,firstname,lastname,email,phone_code,mobile_number,gender,dob,nationality FROM tbl_users WHERE user_type!="admin" AND is_active=1 AND is_delete=0')
        users=cursor.fetchall()
        return render_template('users_list.html',user_lists=users)
    return redirect(url_for('auth.admin_login'))

@admin_bp.get('/product-list')
def product_list():
    if g.email:
        cursor=g.db.cursor(dictionary=True)
        cursor.execute('SELECT product_name,price,quntity,product_unit,additional_charge,stock,description FROM tbl_category_product WHERE is_active=1 AND is_delete=0')
        product_all=cursor.fetchall()
        return render_template('product_list.html',product_all=product_all)
    return redirect(url_for('auth.admin_login'))

@admin_bp.get('/admin-profile')
def admin_profile():
    try:
        if g.email:
            try:
                cursor=g.db.cursor(dictionary=True)
                cursor.execute('SELECT id,prefix,firstname,lastname,email,phone_code,mobile_number,gender,dob,nationality FROM tbl_users WHERE user_type="admin" AND is_active=1 AND is_delete=0')
                admin_pro=cursor.fetchone()
                return render_template('admin-profile.html',a=admin_pro)
            except:
                return redirect('auth.admin_login')
    except:
        return redirect('auth.admin_login')

@admin_bp.get('/store-list')
def store_list():
    if g.email:
        cursor=g.db.cursor(dictionary=True)
        cursor.execute('SELECT name,address,image,owner_name,number FROM tbl_store WHERE is_active=1 AND is_delete=0')
        store=cursor.fetchall()
        return render_template('store_list.html',store=store)
    return redirect(url_for('auth.admin_login'))

@admin_bp.get('/service-list')
def service_list():
    if g.email:
        cursor=g.db.cursor(dictionary=True)
        cursor.execute('SELECT service FROM tbl_service WHERE is_active=1 AND is_delete=0')
        service=cursor.fetchall()
        return render_template('service_list.html',s1=service)
    return redirect(url_for('auth.admin_login'))

@admin_bp.route('/admin-update/<user_id>',methods=['post','get'])
def admin_update(user_id):
    # try:
    if g.email:
        cursor=g.db.cursor(dictionary=True)
        cursor.execute('SELECT id,prefix,firstname,lastname,email,phone_code,mobile_number,gender,dob,nationality FROM tbl_users WHERE user_type!="admin" AND id=%s',(user_id,))
        userupdate=cursor.fetchone()
        print(userupdate)
        if request.method=='POST':
            print('hee')
            data = request.form
            change = []
            value = []
            print("**********************************************************",data)

            if "prefix" in data:
                change.append("prefix=%s")
                value.append(data['prefix'])
                print(value)

            if "firstname" in data:
                change.append("firstname=%s")
                value.append(data['firstname'])

            if "lastname" in data:
                change.append("lastname=%s")
                value.append(data['lastname'])

            if "email" in data:
                change.append("email=%s")
                value.append(data['email'])

            if "phonecode" in data:
                change.append("phone_code=%s")
                value.append(data['phonecode'])

            if "phonenumber" in data:
                change.append("mobile_number=%s")
                value.append(data['phonenumber'])

            if "gender" in data:
                change.append("gender=%s")
                value.append(data['gender'])

            if "dob" in data:
                change.append("dob=%s")
                value.append(data['dob'])
            args=tuple(value)
            print(args)
            print(change)
            print(value)
            print(change)
            query=f"UPDATE tbl_users SET {','.join(change)} WHERE id = {user_id} and is_active=1 and is_delete=0"
            cursor = g.db.cursor()
            cursor.execute(query,args)
            g.db.commit()
            print(value)
            print(change)
            if cursor.rowcount==1:
                error="Successfully updated user profile"
                return render_template('update_user.html',userupdate=userupdate,gender=gender.__members__,error=error)
                # return jsonify({"message":"Successfully updated user profile"}),200

            # return jsonify({"message":f"{cursor.rowcount} rows updated"}),400
        return render_template('update_user.html',userupdate=userupdate,gender=gender.__members__)
        # return render_template('login.html')
        # except Exception as e:
        #     return jsonify({"error":f"{e}"}) 
    return redirect(url_for('auth.admin_login'))

@admin_bp.route('/delete-user/<user_id>')
def del_user(user_id):
    if g.email:
        try:
            cursor = g.db.cursor()
            cursor.execute('UPDATE tbl_users SET is_active=0, is_delete=1 WHERE id = %s', (user_id,))
            g.db.commit()
            flash('User deleted successfully!', 'success')
        except Exception as e:
            flash('An error occurred while deleting the user.', 'error')
            # Log the error or handle it as needed
            print(e)
        return redirect(url_for('admin.tables_data'))
    return redirect(url_for('admin.tables_data'))


def is_admin(user_id):
    cur = g.db.cursor()
    cur.execute(f"select user_type from tbl_users where id={user_id}")
    user = cur.fetchone()
    if user:
        if user[0] == 'admin':
            return True
        return False
        
@admin_bp.post('/announcement')
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


        cursor.execute('INSERT INTO tbl_announcement (image,titel,description) VALUES (%s, %s, %s)',
                        (filename,titel,description))
        g.db.commit()

        return jsonify({'Meassage' : 'Announcement Successfully'}),200
        
    except Exception as e:
        return jsonify({"Error": str(e) }),400
    
@admin_bp.route('/add_product', methods=['POST', 'GET'])
def add_product():
    cursor = g.db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tbl_store")
    store = cursor.fetchall()
    print(store)

    cursor = g.db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tbl_service_category")
    service = cursor.fetchall()
    print(service)
    if request.method == 'POST':

        data = request.form
        store_id = data.get("store_id")
        service_category_id = data.get("service_id")
        p_name = data.get('p_name')
        p_price = data.get('p_price')
        p_quntity = data.get('p_quntity')
        p_unit = data.get('p_unit')
        p_charges = data.get('p_charges')
        p_stock = data.get('p_stock')
        p_description = data.get('p_description')

        cursor = g.db.cursor()
        cursor.execute("INSERT INTO tbl_category_product(store_id,service_category_id,product_name,price,quntity,product_unit,additional_charge,stock,description) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                       (store_id, service_category_id, p_name, p_price, p_quntity, p_unit, p_charges, p_stock, p_description,))
        g.db.commit()
    return render_template('product.html', s=store, ss=service)


@admin_bp.route('/product_img', methods=['POST', 'GET'])
def product_img():

    cursor = g.db.cursor(dictionary=True)
    cursor.execute("SELECT id FROM  tbl_category_product")
    p = cursor.fetchall()
    print("--------------->", p)

    if request.method == 'POST':

        data = request.form
        p_id = data.get("p_id")
        image = data.get('p_image')

        cursor = g.db.cursor()
        cursor.execute("INSERT INTO tbl_product_image(product_id,image) VALUES(%s,%s)",
                       (p_id, image,))
        g.db.commit()
    return render_template('product-image.html', pro=p,)


@admin_bp.route('/add_service', methods=['POST', 'GET'])
def add_service():

    if request.method == 'POST':

        data = request.form
        service = data.get("service")

        cursor = g.db.cursor()
        cursor.execute("INSERT INTO tbl_service(service) VALUES(%s)",
                       (service,))
        g.db.commit()
    return render_template('add-service.html')