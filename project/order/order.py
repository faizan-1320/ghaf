from flask import Blueprint,request,g,jsonify,json
from flask_jwt_extended import jwt_required,get_jwt_identity,create_access_token
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import random


order_bp=Blueprint('order',__name__)


@order_bp.post('/add-new-address-villa')
def add_new_address_villa():
    # users_id = get_jwt_identity()
    cursor = g.db.cursor(dictionary=True)
    cursor.execute('SELECT *  FROM tbl_users WHERE id = %s AND is_active=1 and is_delete=0 AND is_verify=1',(1,))
    user_data = cursor.fetchone()
    print(user_data)
    if user_data:
        if user_data["user_type"] == "user":
            if user_data["is_verify"] == 1:
                address_type = request.json.get("address_type")
                property_type = request.json.get("property_type")
                property_number = request.json.get("property_number")
                landmark = request.json.get("landmark")
                area = request.json.get("area")
                street = request.json.get("street")
                city = request.json.get("city")
                save_addresh = request.json.get("save address")
                latitude = 22.203651
                longitude = 23.25163
                cursor = g.db.cursor(dictionary=True)
                if save_addresh == "yes" or "YES" or "y" or "Y" or "Yes":
                    cursor.execute("INSERT INTO tbl_user_address (user_id,address_type,property_type,property_number,landmark,area,street,city,latitude,longitude) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(1,address_type,property_type,property_number,landmark,area,street,city,latitude,longitude))
                    g.db.commit()
                    return jsonify({"message":"Added Address"})
            else:
                return jsonify({"message": "You are not verify"})
        else:
            return jsonify({"message":"You are not user"})
    elif not user_data:
        return jsonify({"message":"You are not Registered"})

@order_bp.post('/add-new-address-apartment')
def add_new_address_apartment():
    # users_id = get_jwt_identity()
    cursor = g.db.cursor(dictionary=True)
    cursor.execute('SELECT *  FROM tbl_users WHERE id = %s AND is_active=1 and is_delete=0 AND is_verify=1',(1,))
    user_data = cursor.fetchone()
    print(user_data)
    if user_data:
        if user_data["user_type"] == "user":
            if user_data["is_verify"] == 1:
                address_type = request.json.get("address_type")
                property_type = request.json.get("property_type")
                property_number = request.json.get("property_number")
                landmark = request.json.get("landmark")
                area = request.json.get("area")
                street = request.json.get("street")
                city = request.json.get("city")
                name = request.json.get("name")
                apartment_floor_number = request.json.get("apartment_floor_number")
                save_addresh = request.json.get("save address")
                latitude = 22.203651
                longitude = 23.25163
                cursor = g.db.cursor(dictionary=True)
                if save_addresh == "yes" or "YES" or "y" or "Y" or "Yes":
                    cursor.execute("INSERT INTO tbl_user_address (user_id,address_type,property_type,property_number,landmark,area,street,city,latitude,longitude,name,apartment_floor_number) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(1, address_type, property_type, property_number, landmark, area, street, city, latitude, longitude,name,apartment_floor_number))
                    g.db.commit()
                    return jsonify({"message": "Added Address"})
            else:
                return jsonify({"message": "You are not verify"})
        else:
            return jsonify({"message": "You are not user"})
    elif not user_data:
        return jsonify({"message": "You are not Registered"})

@order_bp.post('/add-new-address-hotel')
def add_new_address_hotel():
    # users_id = get_jwt_identity()
    cursor = g.db.cursor(dictionary=True)
    cursor.execute('SELECT *  FROM tbl_users WHERE id = %s AND is_active=1 and is_delete=0 AND is_verify=1',(1,))
    user_data = cursor.fetchone()
    print(user_data)
    if user_data:
        if user_data["user_type"] == "user":
            if user_data["is_verify"] == 1:
                address_type = request.json.get("address_type")
                property_type = request.json.get("property_type")
                property_number = request.json.get("property_number")
                area = request.json.get("area")
                street = request.json.get("street")
                city = request.json.get("city")
                name = request.json.get("name")
                save_addresh = request.json.get("save address")
                latitude = 22.203651
                longitude = 23.25163
                cursor = g.db.cursor(dictionary=True)
                if save_addresh == "yes" or "YES" or "y" or "Y" or "Yes":
                    cursor.execute(
                        "INSERT INTO tbl_user_address (user_id,address_type,property_type,property_number,area,street,city,latitude,longitude,name) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                        (
                        1, address_type, property_type, property_number, area, street, city, latitude,
                        longitude, name))
                    g.db.commit()
                    return jsonify({"message": "Added Address"})
            else:
                return jsonify({"message": "You are not verify"})
        else:
            return jsonify({"message": "You are not user"})
    elif not user_data:
        return jsonify({"message": "You are not Registered"})

@order_bp.post('/add-new-address-other')
def add_new_address_other():
    # users_id = get_jwt_identity()
    cursor = g.db.cursor(dictionary=True)
    cursor.execute('SELECT *  FROM tbl_users WHERE id = %s AND is_active=1 and is_delete=0 AND is_verify=1',
                   (1,))
    user_data = cursor.fetchone()
    print(user_data)
    if user_data:
        if user_data["user_type"] == "user":
            if user_data["is_verify"] == 1:
                address_type = request.json.get("address_type")
                property_type = request.json.get("property_type")
                property_number = request.json.get("property_number")
                landmark = request.json.get("landmark")
                area = request.json.get("area")
                street = request.json.get("street")
                city = request.json.get("city")
                name = request.json.get("name")
                save_addresh = request.json.get("save address")
                latitude = 22.203651
                longitude = 23.25163
                cursor = g.db.cursor(dictionary=True)
                if save_addresh == "yes" or "YES" or "y" or "Y" or "Yes":
                    cursor.execute(
                        "INSERT INTO tbl_user_address (user_id,address_type,property_type,property_number,landmark,area,street,city,latitude,longitude,name) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                        (
                            1, address_type, property_type, property_number, landmark, area, street, city, latitude,
                            longitude, name))
                    g.db.commit()
                    return jsonify({"message": "Added Address"})
            else:
                return jsonify({"message": "You are not verify"})
        else:
            return jsonify({"message": "You are not user"})
    elif not user_data:
        return jsonify({"message": "You are not Registered"})

@order_bp.post('/add-new-address-hospital')
def add_new_address_hospital():
    # users_id = get_jwt_identity()
    cursor = g.db.cursor(dictionary=True)
    cursor.execute('SELECT *  FROM tbl_users WHERE id = %s AND is_active=1 and is_delete=0 AND is_verify=1',
                   (1,))
    user_data = cursor.fetchone()
    print(user_data)
    if user_data:
        if user_data["user_type"] == "user":
            if user_data["is_verify"] == 1:
                address_type = request.json.get("address_type")
                property_type = request.json.get("property_type")
                property_number = request.json.get("property_number")
                area = request.json.get("area")
                street = request.json.get("street")
                city = request.json.get("city")
                name = request.json.get("name")
                section = request.json.get("section")
                apartment_floor_number = request.json.get("apartment_floor_number")
                save_addresh = request.json.get("save address")
                latitude = 22.203651
                longitude = 23.25163
                cursor = g.db.cursor(dictionary=True)
                if save_addresh == "yes" or "YES" or "y" or "Y" or "Yes":
                    cursor.execute("INSERT INTO tbl_user_address (user_id,address_type,property_type,property_number,area,street,city,latitude,longitude,name,section,apartment_floor_number) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(1, address_type, property_type, property_number, area, street, city, latitude, longitude, name, section, apartment_floor_number))
                    g.db.commit()
                    return jsonify({"message": "Added Address"})
            else:
                return jsonify({"message": "You are not verify"})
        else:
            return jsonify({"message": "You are not user"})
    elif not user_data:
        return jsonify({"message": "You are not Registered"})


"""
receiver_type
1)i-am
2)someone
3)saved-receiver
"""
@order_bp.post('/place-order')
def receiver():
    # users_id = get_jwt_identity()
    user_id = request.json.get('user_id')

    cursor = g.db.cursor(dictionary=True)


    cursor.execute('SELECT *  FROM tbl_users WHERE id = %s AND is_active=1 and is_delete=0 AND is_verify=1',(1,))
    user_data = cursor.fetchone()
    if user_data:
        if user_data["user_type"] == "user":
            if user_data["is_verify"] == 1:
                delivery_date = request.json.get("delivery_date")
                delivery_time = request.json.get("delivery_time")
                receiver_type = request.json.get("receiver_type")
                receiver_detail = request.json.get("receiver_detail")
                ritch_reciver = request.json.get("ritch_reciver")
                promocode = request.json.get("promocode")
                falicity_id = request.json.get('falicity_id')
                print(falicity_id)
                cursor = g.db.cursor(buffered=True)
                if falicity_id:

                    cursor.execute(f'SELECT facility_charges FROM tbl_additional_facility WHERE id in {falicity_id}')
                    falicity_charges = cursor.fetchall()
                falicity_charges_total = 0
                if falicity_id:
                    for i in falicity_charges:
                        falicity_charges_total = falicity_charges_total + i[0]
                cursor.execute(
                    "select c.product_id, c.quentity, p.price, p.product_unit, p.quentity, p.product_name, c.quentity * p.price AS zsub_total from tbl_cart as c join tbl_category_product as p on c.product_id = p.id where c.user_id=%s",
                    (user_id,))
                cart_data = cursor.fetchall()

                cursor.execute("select count(id) from tbl_cart where user_id = %s", (user_id,))
                count = cursor.fetchone()
                products = [
                    {"product_id": data[0], "total_items_quentity": data[1], "price": data[2], "product_unit": data[3],
                     "quentity": data[4],
                     "product_name": data[5], "subtotel": data[6]} for data in cart_data]
                print("***********************",products)
                sub_total = 0
                for i in products:
                    sub_total = sub_total + i['subtotel']
                if falicity_id:
                    sub_total = sub_total + falicity_charges_total

                cursor = g.db.cursor(dictionary=True)

                a = "ABC"
                number = str(random.randint(1000000000, 9999999999))
                order_number_ = (a + number)
                transaction = str(random.randint(1000000000, 9999999999))
                cursor.execute(f"SELECT id FROM `tbl_user_address` WHERE user_id= %s GROUP BY id desc LIMIT 1;",(1,))
                address_data = cursor.fetchone()
                print("---------------------------------->",address_data)
                convert_datetime_str_to_datetime = datetime.strptime(delivery_date, '%d-%m-%Y')
                convert_datetime_to_date = convert_datetime_str_to_datetime.date()
                now = datetime.now()
                order_date = now.date()
                cursor.execute(f"SELECT * FROM tbl_promocode WHERE id = %s;",(promocode,))
                promocode_discount = cursor.fetchone()
                print(type(promocode_discount['discount_value']))
                if promocode_discount["discount_type"] == "percentage":
                    if order_date < convert_datetime_to_date:
                        # print(promocode_discount["discount_value"])
                        promocode_discount_value = sub_total*promocode_discount["discount_value"]/100
                        grant_total = sub_total-promocode_discount_value
                        print(promocode_discount_value)
                        cursor.execute(f"INSERT INTO tbl_order (user_id,shipping_address_id,order_number,promocode,sub_total,grant_total,transaction_id,order_date,delivary_date,delevery_time,ritch_reciver) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                       (user_id,address_data['id'],order_number_,promocode,sub_total,grant_total,transaction,order_date,convert_datetime_str_to_datetime,delivery_time,ritch_reciver))
                        g.db.commit()

                        #insert data in tbl_order_details
                        for x in products:
                            cursor.execute(
                                f"INSERT INTO tbl_order_details(order_number,product_id,product_name,price,quentity,sub_total) VALUES(%s,%s,%s,%s,%s,%s)",(order_number_,x["product_id"],x["product_name"],x["price"],x["total_items_quentity"],x["subtotel"]))
                            g.db.commit()

                        #update stock detail
                        cursor.execute('select * from tbl_order_details where order_number=%s;',(order_number_,))
                        oreder_detail = cursor.fetchall()
                        print("oreder_detail",oreder_detail)
                        for i in oreder_detail:
                            cursor.execute('SELECT id,stock FROM tbl_category_product WHERE id=%s',(i["product_id"],))
                            stock_data = cursor.fetchone()
                            updated_stock = stock_data["stock"] - i["quentity"]
                            # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.",updated_stock)
                            print(stock_data["id"],stock_data["stock"])
                            cursor.execute('UPDATE tbl_category_product SET stock = %s WHERE id = %s;',(updated_stock,i["product_id"]))
                            g.db.commit()



                        #delete user cart data
                        # cursor.execute(f'DELETE FROM tbl_cart WHERE user_id=%s;',(user_id,))
                        # g.db.commit()

                        cursor.execute('select id from tbl_order WHERE order_number=%s;', (order_number_,))
                        order_id = cursor.fetchone()

                        if receiver_type == "i-am":
                            print(order_id)
                            cursor.execute('INSERT INTO tbl_order_receiver (order_id,order_number,reciver_id) VALUES (%s,%s,%s)',(order_id['id'],order_number_,address_data['id']))
                            return jsonify({"massage":'data update sucessfully'})

                        elif receiver_type == "someone":
                            for i,j in zip(receiver_detail["reciver_name"],receiver_detail["reciver_number"]):
                                cursor.execute('INSERT INTO tbl_receiver (user_id,name,phone_number) VALUES (%s,%s,%s)',(user_id,i,j))
                                g.db.commit()
                                cursor.execute('select id from tbl_receiver order by id desc limit 1')
                                recever_id = cursor.fetchone()
                                # print(recever_id)
                                # return "hihihi"
                                cursor.execute('INSERT INTO tbl_order_receiver (order_id,order_number,reciver_id) VALUES (%s,%s,%s)',(order_id['id'],order_number_,recever_id['id']))
                                g.db.commit()
                            return jsonify({"massage": 'data update sucessfully'})

                        elif receiver_type == "saved-receiver":
                            data__ = (receiver_detail["reciver_id"])
                            print(type(data__),data__)
                            for i in data__:
                                print(type(i))
                                print("************************************************************")
                                cursor.execute('INSERT INTO tbl_order_receiver (order_id,order_number,reciver_id) VALUES (%s,%s,%s)',(order_id['id'],order_number_,i))
                                g.db.commit()
                            return jsonify({"massage": 'data update sucessfully'})

                        return jsonify({"massage":'data update sucessfully'})
                    else:
                        return jsonify({"message" : "Please select a valid date"})
            else:
                return jsonify({"message": "You are not verify"})
        else:
            return jsonify({"message": "You are not user"})
    elif not user_data:
        return jsonify({"message": "You are not Registered"})



