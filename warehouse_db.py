from  important import *

def add_location(mongo,api):
    whs = mongo.db.warehouse
    whs.insert(api.payload)
    # print(api.payload)
    data = whs.find()
    mthd = []
    for i in data:
        sdata = json.dumps(i, default=my_handler)
        jdata = loads(sdata, object_hook=json_util.object_hook)

        mthd.append(jdata)
    return mthd, 201

def get_location(mongo,api):
    whs = mongo.db.warehouse

    print(api.payload)
    data = whs.find()
    mthd = []
    for i in data:
        sdata = json.dumps(i, default=my_handler)
        jdata = loads(sdata, object_hook=json_util.object_hook)

        mthd.append(jdata)
    return mthd, 200


def delete_location(mongo,id):
    pay = mongo.db.warehouse
    pay.remove({"_id": id})
    data = pay.find()
    mthd = []
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


def add_item(mongo,api):
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

def get_item(mongo,api):
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


def add_dispensed(mongo,api):
    payload = api.payload
    wd = mongo.db.warehouse_dispense
    wd.insert(api.payload)
    data = wd.find().sort('created', -1)
    mthd = []
    dat = int(-1 * payload['quantity'])
    wd.update({'batch': payload['batch'], 'location_id': payload['from']['_id'], 'name': payload['name']},
              {
                  '$inc': {'quantity': dat}
              })

    for i in data:
        sdata = json.dumps(i, default=my_handler)
        jdata = loads(sdata, object_hook=json_util.object_hook)

        mthd.append(jdata)
    return mthd, 200


def get_dispensed(mongo,api):
    wd = mongo.db.warehouse_dispense
    data = wd.find().sort('created', -1)
    mthd = []
    for i in data:
        sdata = json.dumps(i, default=my_handler)
        jdata = loads(sdata, object_hook=json_util.object_hook)

        mthd.append(jdata)
    return mthd, 200


def update_dispensed(mongo,api,id):
    payload = api.payload
    updateData = api.payload
    updateData['status'] = 'returned'
    print(payload)
    wd = mongo.db.warehouse_dispense
    wi = mongo.db.warehouse_items
    wd.insert(api.payload)
    data = wd.find().sort('created', -1)
    mthd = []

    wd.update({'_id': id},
              {"$set": {'status': "returned"}}, upsert=True)

    wi.update({'batch': payload['batch'], 'location_id': payload['location_id'], 'name': payload['name']},
              {
                  '$inc': {'quantity': payload['quantity']}
              })

    for i in data:
        sdata = json.dumps(i, default=my_handler)
        jdata = loads(sdata, object_hook=json_util.object_hook)

        mthd.append(jdata)
    return mthd, 200


def add_adjustment(mongo,api):
    payload = api.payload
    print(payload)
    wd = mongo.db.warehouse_items
    wa = mongo.db.warehouse_adjustment
    check = wd.find_one({'batch': payload['batch'], 'location_id': payload['location_id'], 'name': payload['name']})
    print('if none', check)
    if check == None:
        wd.insert({'name': payload['name'], 'expires': payload['expires'], 'created': payload['created'],
                   'createdBy': payload['createdBy'],
                   'quantity': payload['quantity'], 'batch': payload['batch'], 'purchased': payload['purchased'],
                   'category': payload['category'], 'type': payload['type'], 'location_id': payload['location_id'],
                   'vendor': payload['vendor']})
        wa.insert(payload)
        data = wa.find().sort("adjusted", -1)
        mthd = []
        dat = int(-1 * payload['quantity'])
        # print(dat)
        wd.update({'batch': payload['batch'], 'location_id': payload['from']['_id'], 'name': payload['name']},
                  {
                      '$inc': {'quantity': dat}
                  })

        for i in data:
            sdata = json.dumps(i, default=my_handler)
            jdata = loads(sdata, object_hook=json_util.object_hook)

            mthd.append(jdata)
        return mthd, 200
    else:
        wd.update({'batch': payload['batch'], 'location_id': payload['location_id'], 'name': payload['name']},
                  {
                      '$inc': {'quantity': payload['quantity']}
                  })
        dat = int(-1 * payload['quantity'])
        # print(dat)
        wd.update({'batch': payload['batch'], 'location_id': payload['from']['_id'], 'name': payload['name']},
                  {
                      '$inc': {'quantity': dat}
                  })

        wa.insert(payload)
        data = wa.find().sort("adjusted", -1)
        mthd = []
        for i in data:
            sdata = json.dumps(i, default=my_handler)
            jdata = loads(sdata, object_hook=json_util.object_hook)

            mthd.append(jdata)
        return mthd, 200


def get_adjustment(mongo):
    wd = mongo.db.warehouse_adjustment
    data = wd.find().sort("adjusted", -1)
    mthd = []
    for i in data:
        sdata = json.dumps(i, default=my_handler)
        jdata = loads(sdata, object_hook=json_util.object_hook)

        mthd.append(jdata)
    return mthd, 200


def update_adjustment(mongo,api):
    payload = api.payload
    wd = mongo.db.warehouse_items
    dat = int(-1 * payload['quantity'])
    # print(dat)
    wd.update({'batch': payload['batch'], 'location_id': payload['from']['_id'], 'name': payload['name']},
              {
                  '$inc': {'quantity': dat}
              })

    return 200


def add_receipt(mongo,api):
    payload = api.payload
    wd = mongo.db.warehouse_items
    wi = mongo.db.warehouse_receipt
    check = wd.find_one({'batch': payload['batch'], 'location_id': payload['location_id'], 'name': payload['name']})
    print('if none', check)
    if check == None:
        wi.insert_one(api.payload)
        wd.insert_one(payload)
        data = wi.find()
        mthd = []
        for i in data:
            sdata = json.dumps(i, default=my_handler)
            jdata = loads(sdata, object_hook=json_util.object_hook)

            mthd.append(jdata)
        return mthd, 200


def get_receipt(mongo,api):
    print('dsdfs', api.payload)
    wi = mongo.db.warehouse_receipt

    print(api.payload)
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
    fee.remove({'_id': id})
    data = fee.find()
    mthd = []
    for i in data:
        sdata = json.dumps(i, default=my_handler)
        jdata = loads(sdata, object_hook=json_util.object_hook)

        mthd.append(jdata)
    return mthd, 200


def add_attribute(mongo,api):
    print('dsdfs', api.payload)
    pay = mongo.db.payment_reason
    pay.insert(api.payload)
    # print(api.payload)
    data = pay.find()
    mthd = []
    for i in data:
        sdata = json.dumps(i, default=my_handler)
        jdata = loads(sdata, object_hook=json_util.object_hook)

        mthd.append(jdata)
    return mthd, 201


def get_attribute(mongo,api):
    pay = mongo.db.payment_reason

    print(api.payload)
    data = pay.find()
    mthd = []
    for i in data:
        sdata = json.dumps(i, default=my_handler)
        jdata = loads(sdata, object_hook=json_util.object_hook)

        mthd.append(jdata)
    return mthd, 200


def delete_attribute(mongo,api):
    pay = mongo.db.payment_reason
    pay.remove({"_id": id})
    data = pay.find()
    mthd = []
    for i in data:
        sdata = json.dumps(i, default=my_handler)
        jdata = loads(sdata, object_hook=json_util.object_hook)

        mthd.append(jdata)
    return mthd, 200













