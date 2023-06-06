from flask import Blueprint,g,request,jsonify,session

cart_bp = Blueprint('cart',__name__)

@cart_bp.post('/add_to_cart')
def add_to_cart():
    product_id = request.json.get('product_id')
    user_id = request.json.get('user_id')
    cursor = g.db.cursor()
    cursor.execute("select product_id from tbl_cart where product_id = %s and user_id=%s",(product_id,user_id))
    is_product_in_cart = cursor.fetchone()
    print(not is_product_in_cart)
    if not is_product_in_cart:
        cursor.execute('INSERT INTO tbl_cart(user_id,product_id,quentity) VALUES(%s,%s,%s)',(user_id,product_id,1))
        g.db.commit()
    return jsonify({"massage":"sucessfully add product to cart"})


@cart_bp.delete('/remove_form_cart')
def remove_form_cart():
    product_id = request.json.get('product_id')
    user_id = request.json.get('user_id')
    cursor = g.db.cursor()
    cursor.execute("DELETE FROM tbl_cart WHERE product_id = %s and user_id=%s",(product_id,user_id))
    g.db.commit()
    return jsonify({"massage":"sucessfully remove product from cart"})

@cart_bp.patch('/increase_quentity')
def increase_quentity():
    product_id = request.json.get('product_id')
    user_id = request.json.get('user_id')
    cursor = g.db.cursor()
    cursor.execute("SELECT id FROM tbl_category_product WHERE stock >= quentity and id = %s",(product_id,))
    stock = cursor.fetchone()
    if stock:
        cursor.execute("SELECT p.stock, p.quentity * c.quentity ,p.quentity FROM tbl_category_product AS p JOIN tbl_cart AS c on p.id = c.product_id WHERE p.id = %s",(product_id,))
        check_stock = cursor.fetchone()
        print(check_stock)
        ch_st = check_stock[1]
        qt = check_stock[2]
        print(ch_st,qt)
        if check_stock[0] <= ch_st + qt:
            return jsonify({"massage":"out of stock"})
        
        if check_stock[0]>check_stock[1]:
            cursor.execute("UPDATE tbl_cart SET quentity = quentity+1 WHERE product_id = %s and user_id=%s",(product_id,user_id))
            g.db.commit()
            return jsonify({"massage":"sucessfully increase by + 1"})
        else:
            return jsonify({"massage":"out of stock"})
    else:
        return jsonify({"massage":"out of stock"})
    
@cart_bp.patch('/decrease_quentity')
def decrease_quentity():
    user_id = request.json.get('user_id')
    product_id = request.json.get('product_id')
    cursor = g.db.cursor()
    cursor.execute("select quentity from tbl_cart where product_id = %s and user_id=%s",(product_id,user_id))
    quentity = cursor.fetchone()
    print(quentity)
    if quentity[0] > 1:
        cursor.execute("UPDATE tbl_cart SET quentity = quentity-1 WHERE product_id = %s and user_id=%s",(product_id,user_id))
        g.db.commit()
        return jsonify({"massage":"sucessfully decrease by - 1"})
    else:
        return jsonify({"massage":"last limit of decrease"})
    
@cart_bp.get('/display_cart_product')
def display_cart_product():
    user_id = request.json.get('user_id')
    falicity_id = request.json.get('falicity_id')
    print(falicity_id)
    cursor = g.db.cursor()
    # dictionary=True

    if falicity_id:
        cursor.execute(f'SELECT facility_charges FROM tbl_additional_facility WHERE id = {falicity_id}')
        falicity_charges = cursor.fetchall()
    falicity_charges_total = 0
    if falicity_id:
        for i in falicity_charges:
            falicity_charges_total=falicity_charges_total + i[0]
    cursor.execute("select c.product_id, c.quentity, p.price, p.product_unit, p.quentity, p.product_name, c.quentity * p.price AS zsub_total from tbl_cart as c join tbl_category_product as p on c.product_id = p.id where c.user_id=%s",(user_id,))
    cart_data = cursor.fetchall()

    cursor.execute("select count(id) from tbl_cart where user_id = %s",(user_id,))
    count = cursor.fetchone()
    cursor.execute("select firstname,lastname from tbl_users where id = %s",(user_id,))
    name = cursor.fetchone()
    print(count)
    print(cart_data)
    products = [{"product_id":data[0],"quentity":data[1],"price":data[2],"product_unit":data[3],"quentity":data[4],"product_name":data[5],"subtotel":data[6]} for data in cart_data]
    sub_total = 0
    print(products)
    for i in products:
        sub_total = sub_total + i['subtotel']
    if falicity_id:
        sub_total=sub_total+falicity_charges_total
    name = name[0]+ " " +name[1]
    return jsonify({"products":products, "sub_total":sub_total,"user_name":name,"total_item":count[0],"falicity_charges_total":falicity_charges_total})


# import qrcode
# qr = qrcode.make("www.google.com")  
# qr.save("google.jpg") 