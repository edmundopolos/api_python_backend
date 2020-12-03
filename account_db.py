from  important import *


def add_transaction(mongo,api):
    tranx = mongo.db.transaction
    tranx.insert(api.payload)
    print(api.payload)
    data = tranx.find()
    all_tranx = []
    for i in data:
        sdata = json.dumps(i, default=my_handler)
        jdata = loads(sdata, object_hook=json_util.object_hook)

        all_tranx.append(jdata)
    return all_tranx, 201


def get_transaction(mongo):
    tranx = mongo.db.transaction
    data = tranx.find().sort("createdAt", -1)
    all_tranx = []
    for i in data:
        sdata = json.dumps(i, default=my_handler)
        jdata = loads(sdata, object_hook=json_util.object_hook)

        all_tranx.append(jdata)
    return all_tranx, 200


def get_transaction_person(mongo, id):
    tranx = mongo.db.transaction
    data = tranx.find({"user_id": id}).sort("createdAt", -1)
    all_tranx = []
    for i in data:
        sdata = json.dumps(i, default=my_handler)
        jdata = loads(sdata, object_hook=json_util.object_hook)

        all_tranx.append(jdata)
        print(jdata)
    return all_tranx, 200



def update_transaction(mongo,api,id):
    trnx = mongo.db.transaction
    update = trnx.update({'_id': id},
                         {
                             "$set": {'action': api.payload['action'], 'status': api.payload['status']}
                         },
                         upsert=True
                         )
    if update:
        data = trnx.find()
        pdata = []
        for i in data:
            ndata = json.dumps(i, default=my_handler)
            ldata = loads(ndata, object_hook=json_util.object_hook)
            print('test  ', ldata)
            pdata.append(ldata)
            print('comment', pdata)
            return pdata, 200
    else:
        return {'error': 'unable to delete post',
                'status': 404}, 404


def get_one_transaction(mongo, id):
    tranx = mongo.db.transaction
    data = tranx.find_one({'_id': id})

    sdata = json.dumps(data, default=my_handler)
    tdata = loads(sdata, object_hook=json_util.object_hook)

    return tdata, 200


def delete_transaction(mongo,id):
    tranx = mongo.db.transaction
    tranx.remove({'_id': id})
    data = tranx.find()
    tdata = []
    for i in data:
        sdata = json.dumps(i, default=my_handler)
        jdata = loads(sdata, object_hook=json_util.object_hook)

        tdata.append(jdata)
    return tdata, 200


def bill_class(mongo,api,id):
    payload = api.payload
    url = 'http://0.0.0.0:8000/api/class_students/%s' % id
    s = requests.session()
    r = s.get(url, headers={"Content-Type": "application/json"})
    res = str(r.status_code)
    newData = r.json()
    if res == '200':
        allItems = []
        tranx = mongo.db.transaction
        for i in newData:
            d = {'payer': i['name'], 'amount': int(-1 * payload['amount']), 'type': payload['type'],
                 'createdAt': payload['createdAt'],
                 'created_by': payload['created_by'], 'status': payload['status'], 'reason': payload['reason'],
                 'token': payload['token'],
                 'description': payload['description'], "transaction_date": payload['transaction_date'],
                 'reversed': False, 'reversed_by': 'null', 'canceled_by': 'null', 'canceled_on': 'null',
                 'payment_method': '', 'reciever': '', 'action': 'null', 'user_id': i['Uid']}
            # allItems.append(d)
            tranx.insert(d)

        try:
            print(allItems)

        except Exception as e:
            return e
        nT = mongo.db.transaction
        data = nT.find()
        all_tranx = []
        for i in data:
            sdata = json.dumps(i, default=my_handler)
            jdata = loads(sdata, object_hook=json_util.object_hook)

            all_tranx.append(jdata)
        return all_tranx, 201

def set_fee(mongo,api):
    print('dsdfs', api.payload)
    fees = mongo.db.classFees
    data = fees.find_one({'sectionId': api.payload['sectionId']})

    # print('test i',data)
    if data == None:

        fees.insert(api.payload)
        print(api.payload)
        data = fees.find()
        all_tranx = []
        for i in data:
            sdata = json.dumps(i, default=my_handler)
            jdata = loads(sdata, object_hook=json_util.object_hook)

            all_tranx.append(jdata)
        return all_tranx, 201

    else:
        fees.update({'sectionId': api.payload['sectionId']}, {'$set': {
            'className': api.payload['className'],
            'classId': api.payload['classId'],
            'sectionId': api.payload['sectionId'],
            'amount': api.payload['amount'],
            'sectionName': api.payload['sectionName']
        }}, upsert=True)
        data = fees.find()
        all_tranx = []
        for i in data:
            sdata = json.dumps(i, default=my_handler)
            jdata = loads(sdata, object_hook=json_util.object_hook)
            all_tranx.append(jdata)
        return all_tranx, 200


def get_fee(mongo):
    fees = mongo.db.classFees
    data = fees.find()
    all_tranx = []
    for i in data:
        sdata = json.dumps(i, default=my_handler)
        jdata = loads(sdata, object_hook=json_util.object_hook)

        all_tranx.append(jdata)
    return all_tranx, 200


def delete_fee(mongo,id):
    fee = mongo.db.classFees
    fee.remove({'_id': id})
    data = fee.find()
    mthd = []
    for i in data:
        sdata = json.dumps(i, default=my_handler)
        jdata = loads(sdata, object_hook=json_util.object_hook)

        mthd.append(jdata)
    return mthd, 200


def payment_config(mongo,api):
    print('dsdfs', api.payload)
    pay = mongo.db.payment_method
    pay.insert(api.payload)
    # print(api.payload)
    data = pay.find()
    mthd = []
    for i in data:
        sdata = json.dumps(i, default=my_handler)
        jdata = loads(sdata, object_hook=json_util.object_hook)

        mthd.append(jdata)
    return mthd, 201


def get_payment_config(mongo,api):
    pay = mongo.db.payment_method

    print(api.payload)
    data = pay.find()
    mthd = []
    for i in data:
        sdata = json.dumps(i, default=my_handler)
        jdata = loads(sdata, object_hook=json_util.object_hook)

        mthd.append(jdata)
    return mthd, 200


def delete_payment_config(mongo,id):
    pay = mongo.db.payment_method
    pay.remove({"_id": id})
    data = pay.find()
    mthd = []
    for i in data:
        sdata = json.dumps(i, default=my_handler)
        jdata = loads(sdata, object_hook=json_util.object_hook)

        mthd.append(jdata)
    return mthd, 200


def payment_reason(mongo,api):
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


def get_payment_reason(mongo,api):
    pay = mongo.db.payment_reason

    print(api.payload)
    data = pay.find()
    mthd = []
    for i in data:
        sdata = json.dumps(i, default=my_handler)
        jdata = loads(sdata, object_hook=json_util.object_hook)

        mthd.append(jdata)
    return mthd, 200


def delete_payment_reason(mongo,id):
    pay = mongo.db.payment_reason
    pay.remove({"_id": ObjectId(id)})
    data = pay.find()
    mthd = []
    for i in data:
        sdata = json.dumps(i, default=my_handler)
        jdata = loads(sdata, object_hook=json_util.object_hook)

        mthd.append(jdata)
    return mthd, 200








