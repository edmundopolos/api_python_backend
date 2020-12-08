from important import *


def add_quiz(upload_parser,mongo):
    args = upload_parser.parse_args()
    data = json.loads(args['message'])
    if args.doc:
        file_name = args.doc.filename
        file = args.doc

        print('test ', data)
        print(file_name)
        if file_name and allowed_file(file_name):
            filename = secure_filename(file_name)
            # file.save(filename)
            print(filename)
            destination = os.path.join(app.config['UPLOADS'], '')
            if not os.path.exists(destination):
                os.makedirs(destination)
            ext = get_ext(filename)
            name = str(uuid.uuid4()) + '.' + ext
            fileToUpload = '%s%s' % (destination, name)
            Docurl = name
            file.save(fileToUpload)
            data['uri'] = Docurl
            data['name'] = name
    quiz = mongo.db.quiz
    data['form'] = []
    quiz.insert(data)
    data = quiz.find()
    qdata = []
    for i in data:
        sdata = json.dumps(i, default=my_handler)
        jdata = loads(sdata, object_hook=json_util.object_hook)

        qdata.append(jdata)
    return qdata, 201


def get_quiz(mongo):
    quiz = mongo.db.quiz
    data = quiz.find()
    qdata = []
    for i in data:
        sdata = json.dumps(i, default=my_handler)
        jdata = loads(sdata, object_hook=json_util.object_hook)

        qdata.append(jdata)
    return qdata, 200


def get_one_class_quiz(mongo, id):
    quiz = mongo.db.quiz
    data = quiz.find({"classId": id})
    qdata = []
    for i in data:
        sdata = json.dumps(i, default=my_handler)
        jdata = loads(sdata, object_hook=json_util.object_hook)
        qdata.append(jdata)

    return qdata, 200


def get_one_quiz(mongo):
    quiz = mongo.db.quiz
    data = quiz.find_one({"_id": id})
    qdata = []

    sdata = json.dumps(data, default=my_handler)
    qdata = loads(sdata, object_hook=json_util.object_hook)

    return qdata, 200


def delete_quiz(mongo,id):
    quiz = mongo.db.quiz
    quiz.remove(id)
    data = quiz.find()
    data = []
    for i in data:
        sdata = json.dumps(i, default=my_handler)
        jdata = loads(sdata, object_hook=json_util.object_hook)

        data.append(jdata)
    return data, 200


def get_quiz_form(mongo,id):
    assignment = mongo.db.quiz
    data = assignment.find({"_id": id})

    adata = []
    for i in data:
        ndata = json.dumps(i, default=my_handler)
        ldata = loads(ndata, object_hook=json_util.object_hook)
        adata.append(ldata)
        # print(ndata)

    return adata[0]['form'], 200


def add_quiz_form(mongo,api,id):
    quiz = mongo.db.quiz
    print('testing', api.payload)
    data = quiz.update({'_id': id}, {'$set': {'form': api.payload['task_data']}}, upsert=True)
    print(data)
    # print(api.payload['task_data'])
    return api.payload, 200


def get_quiz_answer(mongo,aid,cid,sid):
    answer = mongo.db.quiz_answer
    data = answer.find_one({'quizId': aid, 'classId': cid, 'student': sid})
    # print('checkit',data)

    if data == None:
        # print('null')
        return [], 200
    else:
        # print('check',data['answer'])
        return data['answer'], 200


def update_quiz_answer(mongo, api, aid, cid, sid):
    answer = mongo.db.quiz_answer
    answer.update({'quizId': aid, 'classId': cid, 'student': sid},
                  {'$set': {'grade': api.payload['grade']}}, upsert=True)
    data = answer.find_one({'quizId': aid, 'classId': cid, 'student': sid})

    if data == None:
        # print('null')
        return [], 200
    else:
        # print('check',data['answer'])
        return data['answer'], 200


def add_quiz_answer(mongo,api,aid,cid,sid):
    answer = mongo.db.quiz_answer
    # data=answer.update({'_id': id},{'$set':{'form':api.payload['task_data']}},upsert=True)
    data = answer.find_one({'assignmentId': aid, 'classId': cid, 'student': sid})

    # print('test i',data)
    if data == None:
        payload = {}
        payload['assignmentId'] = aid
        payload['classId'] = cid
        payload['student'] = sid
        payload['answer'] = api.payload
        data = answer.insert(payload)
        # print(data)
        print(api.payload)
        return api.payload, 200
    else:
        payload = {}
        payload['assignmentId'] = aid
        payload['classId'] = cid
        payload['student'] = sid
        payload['answer'] = api.payload
        answer.update({'assignmentId': aid, 'classId': cid, 'student': sid}, {'$set': {'answer': api.payload}},
                      upsert=True)
        # print(data)
        print(api.payload)
        return api.payload, 200



