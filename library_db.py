from  important import *


def library_dispensary(mongo,api):
    payload = api.payload
    wd = mongo.db.library_lent
    wi = mongo.db.warehouse_items
    wd.insert(api.payload)
    data = wd.find().sort('created', -1)
    mthd = []
    # dat = int(-1*payload['quantity'])
    wi.update({'batch': payload['batch'], 'location_id': payload['from']['_id'], 'name': payload['name']},
              {
                  '$inc': {'quantity': payload['quantity']}
              })

    for i in data:
        sdata = json.dumps(i, default=my_handler)
        jdata = loads(sdata, object_hook=json_util.object_hook)

        mthd.append(jdata)
    return mthd, 200


def get_library_dispense(mongo,api):
    wd = mongo.db.library_lent
    data = wd.find().sort('created', -1)
    mthd = []
    for i in data:
        sdata = json.dumps(i, default=my_handler)
        jdata = loads(sdata, object_hook=json_util.object_hook)

        mthd.append(jdata)
    return mthd, 200


def update_dispensed(mongo,api):
    payload = api.payload
    updateData = api.payload
    updateData['status'] = 'returned'
    print(payload)
    wd = mongo.db.library_lent
    wi = mongo.db.warehouse_items
    # wd.insert(api.payload)
    dat = int(-1 * payload['quantity'])
    wd.update({'_id': id},
              {
                  "$set": {'status': "returned"}
              })
    wi.update({'batch': payload['batch'], 'location_id': payload['location_id'], 'name': payload['name']},
              {
                  '$inc': {'quantity': dat}
              })
    data = wd.find().sort('created', -1)
    mthd = []

    # wd.update({'_id': id})

    for i in data:
        sdata = json.dumps(i, default=my_handler)
        jdata = loads(sdata, object_hook=json_util.object_hook)

        mthd.append(jdata)
    return mthd, 200


def library_adjustment(mongo,api):
    payload = api.payload
    print(payload)
    wd = mongo.db.warehouse_items
    wa = mongo.db.library_adjustment
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


def get_library_adjustment(mongo):
    wd = mongo.db.library_adjustment
    data = wd.find().sort("adjusted", -1)
    mthd = []
    for i in data:
        sdata = json.dumps(i, default=my_handler)
        jdata = loads(sdata, object_hook=json_util.object_hook)

        mthd.append(jdata)
    return mthd, 200


def update_library_adjustment(mongo,api):
    payload = api.payload
    wd = mongo.db.warehouse_items
    dat = int(-1 * payload['quantity'])
    # print(dat)
    wd.update({'batch': payload['batch'], 'location_id': payload['from']['_id'], 'name': payload['name']},
              {
                  '$inc': {'quantity': dat}
              })

    return 200


def get_shelf(mongo,api):
    pay = mongo.db.shelf

    print(api.payload)
    data = pay.find()
    mthd = []
    for i in data:
        sdata = json.dumps(i, default=my_handler)
        jdata = loads(sdata, object_hook=json_util.object_hook)

        mthd.append(jdata)
    return mthd, 200


def add_shelf(mongo,api):
    print('dsdfs', api.payload)
    pay = mongo.db.shelf
    pay.insert(api.payload)
    # print(api.payload)
    data = pay.find()
    mthd = []
    for i in data:
        sdata = json.dumps(i, default=my_handler)
        jdata = loads(sdata, object_hook=json_util.object_hook)

        mthd.append(jdata)
    return mthd, 201


def delete_shelf(mongo, id):
    pay = mongo.db.shelf
    pay.remove({"_id": id})
    data = pay.find()
    mthd = []
    for i in data:
        sdata = json.dumps(i, default=my_handler)
        jdata = loads(sdata, object_hook=json_util.object_hook)

        mthd.append(jdata)
    return mthd, 200



























