from  important import *

def add_building(mongo,api):
    whs = mongo.db.hostel
    whs.insert(api.payload)
    # print(api.payload)
    data = whs.find()
    mthd = []
    for i in data:
        sdata = json.dumps(i, default=my_handler)
        jdata = loads(sdata, object_hook=json_util.object_hook)

        mthd.append(jdata)
    return mthd, 201

def get_building(mongo,api):
    whs = mongo.db.hostel

    print(api.payload)
    data = whs.find()
    mthd = []
    for i in data:
        sdata = json.dumps(i, default=my_handler)
        jdata = loads(sdata, object_hook=json_util.object_hook)

        mthd.append(jdata)
    return mthd, 200


def delete_building(mongo,id):
    pay = mongo.db.hostel
    pay.remove({"_id": id})
    data = pay.find()
    mthd = []
    for i in data:
        sdata = json.dumps(i, default=my_handler)
        jdata = loads(sdata, object_hook=json_util.object_hook)

        mthd.append(jdata)
    return mthd, 200


def update_building(mongo,api,id):
    payload = api.payload
    updateData = api.payload
    updateData['status'] = 'returned'
    print(payload)
    wd = mongo.db.hostel

    data = wd.find().sort('created', -1)
    mthd = []

    wd.update({'_id': id},
              {"$set": json.loads(api.payload)}, upsert=True)
    for i in data:
        sdata = json.dumps(i, default=my_handler)
        jdata = loads(sdata, object_hook=json_util.object_hook)

        mthd.append(jdata)
    return mthd, 200



def add_vendor(mongo,api):
    whs = mongo.db.warehouse_vendor
    whs.insert(api.payload)
    # print(api.payload)
    data = whs.find()
    mthd = []
    for i in data:
        sdata = json.dumps(i, default=my_handler)
        jdata = loads(sdata, object_hook=json_util.object_hook)

        mthd.append(jdata)
    return mthd, 201

def get_vendor(mongo,api):
    whs = mongo.db.warehouse_vendor

    print(api.payload)
    data = whs.find()
    mthd = []
    for i in data:
        sdata = json.dumps(i, default=my_handler)
        jdata = loads(sdata, object_hook=json_util.object_hook)

        mthd.append(jdata)
    return mthd, 200


def add_student(mongo,api):
    wi = mongo.db.warehouse_items
    print(api.payload)
    wi.insert_one(api.payload)
    data = wi.find()
    mthd = []
    for i in data:
        sdata = json.dumps(i, default=my_handler)
        jdata = loads(sdata, object_hook=json_util.object_hook)

        mthd.append(jdata)
    return mthd, 200

def get_student(mongo,api):
    print('dsdfs', api.payload)
    wi = mongo.db.warehouse_items

    print(api.payload)
    data = wi.find()
    mthd = []
    for i in data:
        sdata = json.dumps(i, default=my_handler)
        jdata = loads(sdata, object_hook=json_util.object_hook)

        mthd.append(jdata)
    return mthd, 200


# def add_student(mongo,api):
#     payload = api.payload
#     wd = mongo.db.hostel_room
#     wd.insert(api.payload)
#     data = wd.find().sort('created', -1)
#     mthd = []
#     dat = int(-1 * payload['quantity'])
#     wd.update({'batch': payload['batch'], 'location_id': payload['from']['_id'], 'name': payload['name']},
#               {
#                   '$inc': {'quantity': dat}
#               })
#
#     for i in data:
#         sdata = json.dumps(i, default=my_handler)
#         jdata = loads(sdata, object_hook=json_util.object_hook)
#
#         mthd.append(jdata)
#     return mthd, 200


def get_hostel_rooms(mongo,api):
    wd = mongo.db.hostel_room
    data = wd.find().sort('created', -1)
    mthd = []
    for i in data:
        sdata = json.dumps(i, default=my_handler)
        jdata = loads(sdata, object_hook=json_util.object_hook)

        mthd.append(jdata)
    return mthd, 200


def update_hostel_room(mongo,api,id):
    payload = api.payload
    updateData = api.payload
    updateData['status'] = 'returned'
    print(payload)
    wd = mongo.db.hostel_room

    data = wd.find().sort('created', -1)
    mthd = []

    wd.update({'_id': id},
              {"$set": json.loads(api.payload)}, upsert=True)
    for i in data:
        sdata = json.dumps(i, default=my_handler)
        jdata = loads(sdata, object_hook=json_util.object_hook)

        mthd.append(jdata)
    return mthd, 200


def delete_hostel_room(mongo,api,id):
    payload = api.payload
    updateData = api.payload
    updateData['status'] = 'returned'
    print(payload)
    wd = mongo.db.hostel_room

    data = wd.find().sort('created', -1)
    mthd = []

    wd.remove({'_id': id})
    for i in data:
        sdata = json.dumps(i, default=my_handler)
        jdata = loads(sdata, object_hook=json_util.object_hook)

        mthd.append(jdata)
    return mthd, 200


def add_to_room(mongo,api):
    payload = api.payload
    print(payload)
    wd = mongo.db.hostel_room

    wd.insert(payload)

    data = wd.find().sort("created", -1)
    mthd = []

    for i in data:
        sdata = json.dumps(i, default=my_handler)
        jdata = loads(sdata, object_hook=json_util.object_hook)

        mthd.append(jdata)
    return mthd, 200




# def get_assigned(mongo):
#     wd = mongo.db.warehouse_adjustment
#     data = wd.find().sort("created", -1)
#     mthd = []
#     for i in data:
#         sdata = json.dumps(i, default=my_handler)
#         jdata = loads(sdata, object_hook=json_util.object_hook)
#
#         mthd.append(jdata)
#     return mthd, 200


def update_assigned(mongo,api,id):
    payload = api.payload
    wd = mongo.db.assign_room

    # print(dat)
    wd.update({"_id": id},
              {
                  '$set': {'room_id': payload['room_id']}
              })

    return 200


def delete_assigned(mongo, id):
    wd = mongo.db.assign_room
    ar = mongo.db.hostel_room
    data = wd.find_one({'_id': id})
    ar.update({'_id': ObjectId(data['room']['_id'])},
              {
                  '$inc': {'capacity': 1}
              }, upsert=True)
    wd.remove({"_id": id})

    return 200


def add_assigned(mongo,api):
    payload = api.payload
    wd = mongo.db.assign_room
    ar = mongo.db.hostel_room

    wd.insert_one(payload)
    ar.update({"_id": ObjectId(payload['room']['_id'])},
              {
                  '$inc': {'capacity': payload['capacity']}
              }, upsert=True)
    data = wd.find()
    mthd = []
    for i in data:
        sdata = json.dumps(i, default=my_handler)
        jdata = loads(sdata, object_hook=json_util.object_hook)

        mthd.append(jdata)
    return mthd, 200



def get_assigned(mongo):
    # print('dsdfs', api.payload)
    wi = mongo.db.assign_room

    data = wi.find()
    mthd = []
    for i in data:
        sdata = json.dumps(i, default=my_handler)
        jdata = loads(sdata, object_hook=json_util.object_hook)

        mthd.append(jdata)
    return mthd, 200


def add_sales_item(mongo,api):
    print('dsdfs', api.payload)
    price = mongo.db.sales_item
    data = price.find_one({'name': api.payload['name']})

    # print('test i',data)
    if data == None:

        price.insert(api.payload)
        print(api.payload)
        data = price.find()
        all_tranx = []
        for i in data:
            sdata = json.dumps(i, default=my_handler)
            jdata = loads(sdata, object_hook=json_util.object_hook)

            all_tranx.append(jdata)
        return all_tranx, 201

    else:
        price.update({'sectionId': api.payload['sectionId']}, {'$set': {
            'name': api.payload['name'],
            'type': api.payload['type'],
            'category': api.payload['category'],
            'amount': api.payload['amount']
        }}, upsert=True)
        data = price.find()
        all_tranx = []
        for i in data:
            sdata = json.dumps(i, default=my_handler)
            jdata = loads(sdata, object_hook=json_util.object_hook)
            all_tranx.append(jdata)
        return all_tranx, 200


def get_sales_item(mongo):
    fees = mongo.db.sales_item
    data = fees.find()
    all_tranx = []
    for i in data:
        sdata = json.dumps(i, default=my_handler)
        jdata = loads(sdata, object_hook=json_util.object_hook)

        all_tranx.append(jdata)
    return all_tranx, 200


def delete_sales_item(mongo,api,id):
    fee = mongo.db.sales_item
    fee.remove({'_id': ObjectId(id)})
    data = fee.find()
    mthd = []
    for i in data:
        sdata = json.dumps(i, default=my_handler)
        jdata = loads(sdata, object_hook=json_util.object_hook)

        mthd.append(jdata)
    return mthd, 200


def add_session_attendance(mongo,api):
    print('dsdfs', api.payload)
    pay = mongo.db.hostel_session_attendance
    pay.insert(api.payload)
    # print(api.payload)
    data = pay.find()
    mthd = []
    for i in data:
        sdata = json.dumps(i, default=my_handler)
        jdata = loads(sdata, object_hook=json_util.object_hook)

        mthd.append(jdata)
    return mthd, 200






def get_session_attendance(mongo):
    pay = mongo.db.hostel_session_attendance


    data = pay.find()

    mthd = []
    for i in data:
        sdata = json.dumps(i, default=my_handler)
        jdata = loads(sdata, object_hook=json_util.object_hook)

        mthd.append(jdata)
        # print(mthd)
    return mthd, 200


def update_session_attendance(mongo, api, id):
    payload = api.payload
    wd = mongo.db.hostel_session_attendance

    # print(dat)
    wd.update({"_id": id},
              {
                  '$set': {'status': 'out'}
              })

    return 200


def delete_session_attendance(mongo,api):
    pay = mongo.db.hostel_session_attendance
    pay.remove({"_id": id})
    data = pay.find()
    mthd = []
    for i in data:
        sdata = json.dumps(i, default=my_handler)
        jdata = loads(sdata, object_hook=json_util.object_hook)

        mthd.append(jdata)
    return mthd, 200


def add_attendance(mongo,api):
    print('dsdfs', api.payload)
    pay = mongo.db.hostel_attendance
    pay.insert(api.payload)
    # print(api.payload)
    data = pay.find()
    mthd = []
    for i in data:
        sdata = json.dumps(i, default=my_handler)
        jdata = loads(sdata, object_hook=json_util.object_hook)

        mthd.append(jdata)
    return mthd, 200


def get_attendance(mongo):
    pay = mongo.db.hostel_attendance

    # print(api.payload)
    data = pay.find()
    mthd = []
    for i in data:
        sdata = json.dumps(i, default=my_handler)
        jdata = loads(sdata, object_hook=json_util.object_hook)

        mthd.append(jdata)
    return mthd, 200


def update_attendance(mongo, api, id):
    payload = api.payload
    wd = mongo.db.hostel_attendance

    # print(dat)
    wd.update({"_id": ObjectId(id)},
              {
                  '$set': {'room_id': payload['room_id']}
              })

    return 200


def delete_attendance(mongo,id):
    pay = mongo.db.hostel_attendance
    pay.remove({"_id": ObjectId(id)})
    data = pay.find()
    mthd = []
    for i in data:
        sdata = json.dumps(i, default=my_handler)
        jdata = loads(sdata, object_hook=json_util.object_hook)

        mthd.append(jdata)
    return mthd, 200













