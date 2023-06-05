from flask import Blueprint,jsonify,request,g

advertisement_bp=Blueprint('adv',__name__)

@advertisement_bp.get("/advertis_available_slots")
def advertis_available_slots():
    try:
        data = request.json
    except:
        return jsonify({'error':'no data found'}),404
    date = data.get('date')
    if not date:
        return jsonify({"error":"date not found"}),404
    

    cur = g.db.cursor(dictionary=True)
    cur.execute(f"select id from tbl_advertis_book_slot abs where abs.book_date='{date}'and abs.is_active=1")
    available_slot_data = cur.fetchall()
    if not available_slot_data:
        cur.execute(f"select tas.id,tas.slot_type,concat(tas.start_time,' to ',tas.end_time) as time,tas.price from tbl_advertis_slot tas")
        available_slot_data = cur.fetchall()
        return jsonify({'available_slot_data':available_slot_data})
    slots = ()
    for i in available_slot_data:
        slots = slots + (i['id'],)
    if len(slots) == 1:
        que = f"select tas.id,tas.slot_type,concat(tas.start_time,' to ',tas.end_time) as time,tas.price from tbl_advertis_slot tas where tas.id not in ({available_slot_data[0]['id']})"
    else:
        que = f"select tas.id,tas.slot_type,concat(tas.start_time,' to ',tas.end_time) as time,tas.price from tbl_advertis_slot tas where tas.id not in {str(slots)}"
    cur.execute(que)
    available_slot_data = cur.fetchall()
    return jsonify({'available_slot_data':available_slot_data})


@advertisement_bp.post("/advertis_order")
def advertis_order():
    try:
        data = request.json
        # print("sddddddddddddddddddddd",data)

    except Exception as e:
        return jsonify({"error":f"no data found {e}"}),404
    print("sddddddddddddddddddddd",data)
    
    if not data:
        return jsonify({"error":"no data found"}),404
    corporate_name = data.get("corporate_name")
    contacted_person_perfix = data.get("contacted_person_perfix")
    contacted_person_name = data.get("contacted_person_name")
    contacted_person_position = data.get("contacted_person_position")
    phone = data.get("phone")
    email = data.get("email")
    meeting_date = data.get("meeting_date")
    meeting_time = data.get("meeting_time")
    location = data.get("location")
    city = data.get("city")
    area_name = data.get("area_name")
    property = data.get("property")

    villa_number = data.get("villa_number")
    landmark = data.get("landmark")
    building_number = data.get("building_number")
    building_name = data.get("building_name")
    apratment_number = data.get("apratment_number")
    hotel_name = data.get("hotel_name")
    room_number = data.get("room_number")
    hospital_name = data.get("hospital_name")
    section = data.get("section")
    floor = data.get("floor")
    location_name = data.get("location_name")
    location_number = data.get("location_number")

    street_name_number = data.get("street_name_number")
    
    plateform = data.get("plateform")
    content_type = data.get("content_type")
    total_amount = data.get("total_amount")
    website_link = data.get("website_link")
    card_type = data.get("card_type")
    card_number = data.get("card_number")
    exp_date = data.get("exp_date")
    cvv = data.get("cvv")
    payment_status = data.get("payment_status")
    slot_id = data.get("slot_id")
    book_date = data.get("book_date")

    if not corporate_name:
        return jsonify({"error":"corporate_name is required"}),404
    if not contacted_person_perfix:
        return jsonify({"error":"contacted_person_perfix is required"}),404
    if not contacted_person_name:
        return jsonify({"error":"contacted_person_name is required"}),404
    if not contacted_person_position:
        return jsonify({"error":"contacted_person_position is required"}),404
    if not phone:
        return jsonify({"error":"phone is required"}),404
    if not email:
        return jsonify({"error":"email is required"}),404
    if not meeting_date:
        return jsonify({"error":"meeting_date is required"}),404
    if not meeting_time:
        return jsonify({"error":"meeting_time is required"}),404
    if not location:
        return jsonify({"error":"location is required"}),404
    if not city:
        return jsonify({"error":"city is required"}),404
    if not area_name:
        return jsonify({"error":"area_name is required"}),404
    if not property:
        return jsonify({"error":"property is required"}),404
    
    
    if not plateform:
        return jsonify({"error":"plateform is required"}),404
    if not content_type:
        return jsonify({"error":"content_type is required"}),404
    if not total_amount:
        return jsonify({"error":"total_amount is required"}),404
    if not website_link:
        return jsonify({"error":"website_link is required"}),404
    if website_link not in ['0','1']:
        return jsonify({"error":"enter weblink input either 0 or 1"}),400
    if not card_type:
        return jsonify({"error":"card_type is required"}),404
    if not card_number:
        return jsonify({"error":"card_number is required"}),404
    if not exp_date:
        return jsonify({"error":"exp_date is required"}),404
    if not cvv:
        return jsonify({"error":"cvv is required"}),404
    if not slot_id:
        return jsonify({"error":"slot_id is required"}),404
    if not payment_status:
        return jsonify({"error":"payment_status is required"}),404
    if not book_date:
        return jsonify({"error":"book_date is required"}),404
    
    if not street_name_number:
        return jsonify({"error":"street_name_number is required"}),404
    if property not in ['villa','apartment','hotel','hospital','other']:
        return jsonify({"error":"enter valid property"}),400
    if property == "villa":
        if not villa_number:
            return jsonify({"error":"villa_number is required"}),404
        if not landmark:
            return jsonify({"error":"landmark is required"}),404
        meeting_query = f'''insert into tbl_advertis_meeting (corporate_name,contacted_person_perfix,contacted_person_name,contacted_person_position,phone,email,meeting_date,meeting_time,location,city,area_name,property,villa_number,street_name_number,landmark) values
        ('{corporate_name}','{contacted_person_perfix}','{contacted_person_name}','{contacted_person_position}','{phone}','{email}','{meeting_date}','{meeting_time}','{location}','{city}','{area_name}','{property}','{villa_number}','{street_name_number}','{landmark}')'''
    if property == "apartment":
        if not building_name:
            return jsonify({"error":"building_name is required"}),404
        if not building_number:
            return jsonify({"error":"building_number is required"}),404
        if not apratment_number:
            return jsonify({"error":"apratment_number is required"}),404
        if not landmark:
            return jsonify({"error":"landmark is required"}),404
        meeting_query = f'''insert into tbl_advertis_meeting (corporate_name,contacted_person_perfix,contacted_person_name,contacted_person_position,phone,email,meeting_date,meeting_time,location,city,area_name,property,building_name,building_number,apratment_number,street_name_number,landmark) values
         ('{corporate_name}','{contacted_person_perfix}','{contacted_person_name}','{contacted_person_position}','{phone}','{email}','{meeting_date}','{meeting_time}','{location}','{city}','{area_name}','{property}','{building_name}','{building_number}','{apratment_number}','{street_name_number}','{landmark}')'''
        
    if property == "hotel":
        if not hotel_name:
            return jsonify({"error":"hotel_name is required"}),404
        if not room_number:
            return jsonify({"error":"room_number is required"}),404
        meeting_query = f'''insert into tbl_advertis_meeting (corporate_name,contacted_person_perfix,contacted_person_name,contacted_person_position,phone,email,meeting_date,meeting_time,location,city,area_name,property,hotel_name,room_number,street_name_number) values
         ('{corporate_name}','{contacted_person_perfix}','{contacted_person_name}','{contacted_person_position}','{phone}','{email}','{meeting_date}','{meeting_time}','{location}','{city}','{area_name}','{property}','{hotel_name}','{room_number}','{street_name_number}')'''
        
    if property == "hospital":
        if not hospital_name:
            return jsonify({"error":"hospital_name is required"}),404
        if not section:
            return jsonify({"error":"section is required"}),404
        if not floor:
            return jsonify({"error":"floor is required"}),404
        if not room_number:
            return jsonify({"error":"room_number is required"}),404
        meeting_query = f'''insert into tbl_advertis_meeting (corporate_name,contacted_person_perfix,contacted_person_name,contacted_person_position,phone,email,meeting_date,meeting_time,location,city,area_name,property,hospital_name,section,floor,room_number,street_name_number) values
         ('{corporate_name}','{contacted_person_perfix}','{contacted_person_name}','{contacted_person_position}','{phone}','{email}','{meeting_date}','{meeting_time}','{location}','{city}','{area_name}','{property}','{hospital_name}','{section}','{floor}','{room_number}','{street_name_number}')'''
        
    if property == "other":
        if not location_name:
            return jsonify({"error":"location_name is required"}),404
        if not location_number:
            return jsonify({"error":"location_number is required"}),404
        if not landmark:
            return jsonify({"error":"landmark is required"}),404
        meeting_query = f'''insert into tbl_advertis_meeting (corporate_name,contacted_person_perfix,contacted_person_name,contacted_person_position,phone,email,meeting_date,meeting_time,location,city,area_name,property,location_name,location_number,street_name_number,landmark) values
         ('{corporate_name}','{contacted_person_perfix}','{contacted_person_name}','{contacted_person_position}','{phone}','{email}','{meeting_date}','{meeting_time}','{location}','{city}','{area_name}','{property}','{location_name}','{location_number}','{street_name_number}','{landmark}')'''

    if len(book_date) != len(slot_id):
        return jsonify({"error":"length of slot id and booking date not match"}),400
        
            
    

    cur = g.db.cursor(dictionary=True)
    print(list(data.keys()))
    cur.execute(meeting_query)
    g.db.commit()
    meeting_id=cur.lastrowid
    cur.execute(f"insert into tbl_advertis_payment (card_type,card_number,exp_date,cvv,payment_status) values ('{card_type}','{card_number}','{exp_date}',{cvv},'{payment_status}')")
    g.db.commit()
    payment_id = cur.lastrowid
    book_slot_id = []
    for i in range(len(slot_id)):
        cur.execute(f"insert into tbl_advertis_book_slot (slot_id,book_date) values ({slot_id[i]},'{book_date[i]}')")
        g.db.commit()
        book_slot_id.append(cur.lastrowid)
    cur.execute(f"insert into tbl_advertis_order (meeting_id,content_type,website_link,payment_id,total_amount) values ({meeting_id},'{content_type}','{website_link}','{payment_id}',{total_amount})")
    g.db.commit()
    order_id = cur.lastrowid
    for i in book_slot_id:
        cur.execute(f"insert into tbl_advertis_order_details (order_id,book_slot_id) values ({order_id},{i})")
        g.db.commit()
    print(book_slot_id)

    print(payment_id)

    return jsonify({"message":"order placed successfully"}),200

@advertisement_bp.get('/order_details/<order_id>')
def order_details(order_id):
    cur = g.db.cursor(dictionary=True)
    cur.execute(f'''SELECT ao.plateform,ao.content_type,ao.website_link,ao.total_amount,ap.card_type,ap.card_number,am.corporate_name,am.contacted_person_perfix,am.contacted_person_name,am.contacted_person_position,am.phone,am.email,concat(am.meeting_date,' at ',am.meeting_time),am.property,am.location FROM `tbl_advertis_order` ao 
                        join tbl_advertis_meeting am on ao.meeting_id=am.id 
                        join tbl_advertis_payment ap on ao.payment_id=ap.id 
                        WHERE ao.id = {order_id}''')
    order_data = cur.fetchone()
    cur.execute(f'''select aas.slot_type,concat(aas.start_time,' to ',aas.end_time) as time,aas.price,abs.book_date  from tbl_advertis_order_details aod 
                    join tbl_advertis_book_slot abs on aod.order_id = abs.id 
                    JOIN tbl_advertis_slot aas on abs.slot_id = aas.id
                    where aod.order_id={order_id}''')
    book_slot_data = cur.fetchall()
    order_data['advertis_slot'] = book_slot_data
    return jsonify({"data":order_data}),200
    