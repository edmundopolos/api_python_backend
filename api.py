
# from flask_restplus import Api, Resource, fields
from important import *



from operator import itemgetter
app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/mschool'
app.config["UPLOADS"] = "/var/www/files/"
CORS(app)
mongo =PyMongo(app)
# app.wsgi_app = ProxyFix(app.wsgi_app)
blueprint = Blueprint('Mschool', __name__)
api = Api(blueprint) #,doc=False
app.register_blueprint(blueprint)
app.app_context().push()


#user
userModel = {
    "_id": fields.String("id",readonly=True),
    "username": fields.String("username"),
    "token": fields.String("token"),
    "user_id": fields.String("user id"),
    "usertype": fields.String("userType"),
    "avatar": fields.String("avi")

}
userM = api.model('user', userModel)

us = api.namespace('user')
@us.route('/')
class User(Resource):

    @api.expect(userM)
    def post(self):
        user = mongo.db.users
        test=api.payload
        # print(test)
        check = user.find_one({'user_id':api.payload['user_id']})
        # print('check',check)

        if check != None:
            pdata = []
            ndata = json.dumps(check, default=my_handler)
            ldata = loads(ndata, object_hook=json_util.object_hook)
            # print('test  ',ldata)
            pdata.append(ldata)
            return pdata,200
        else:
            user.insert(api.payload)
            data = user.find({'user_id':api.payload['user_id']})
            pdata = []
            for i in data:
                ndata = json.dumps(i, default=my_handler)
                ldata = loads(ndata, object_hook=json_util.object_hook)
                # print('test  ',ldata)
                pdata.append(ldata)
            return pdata,201


@us.route('/<int:userId>/')
class UserAvi(Resource):
    @api.expect(upload_parser)
    def put(self,userId):
        args = upload_parser.parse_args()

        if args.file:

            imgname = args.file.filename
            file = args.file

            print(imgname)
            if imgname and allowed_file(imgname):
                imagename = secure_filename(imgname)
                # file.save(filename)
                print(imagename)
                destination = os.path.join(app.config['UPLOADS'], './')
                if not os.path.exists(destination):
                    os.makedirs(destination)
                ext = get_ext(imagename)
                print(ext)
                Iname = str(uuid.uuid4()) + '.' +  ext
                print(Iname)
                imageUpload = '%s%s' % (destination, Iname)
                Imageurl = 'http://192.168.43.136:900/' + Iname
                file.save(imageUpload)

                user = mongo.db.users
                user.update({'user_id':userId},{'$set':{'avatar':Imageurl}},upsert=True)
                data = user.find({'user_id':userId})
                pdata = []
                for i in data:
                    ndata = json.dumps(i, default=my_handler)
                    ldata = loads(ndata, object_hook=json_util.object_hook)
                    print('test  ',ldata)
                    pdata.append(ldata)
                return pdata,200
    def get(self,userId):
        user = mongo.db.users
        data = user.find({'user_id':userId})
        pdata = []
        for i in data:
            ndata = json.dumps(i, default=my_handler)
            ldata = loads(ndata, object_hook=json_util.object_hook)
            print('test  ',ldata)
            pdata.append(ldata)
        return pdata,200



@us.route('/<ObjectId:id>')
class OneUser(Resource):
    def get(self,id):
        user = mongo.db.post
        data = user.find({"_id:id"})
        pdata = []
        for i in data:
            ndata = json.dumps(i, default=my_handler)
            ldata = loads(ndata, object_hook=json_util.object_hook)
            print('test  ',ldata)
            pdata.append(ldata)
        return pdata,200


#posts
postModel =  {
    "_id": fields.String(readonly=True,),
      "message": fields.String("message"),
      "title": fields.String("title"),
      "image": fields.Raw,
      "username": fields.String("username"),
      "group": fields.String("group"),
      "classId": fields.String("class"),
      "doc": fields.String("doc"),
      "docUri": fields.String("docUri"),
      "feed":fields.String("feed"),
      "userType": fields.String("userType"),
      "created": fields.String("Sun Apr 05 2020 21:16:01 GMT+0100 (West Africa Standard Time)"),
      "teacher_id": fields.Integer(),
      "comments": fields.List(fields.Raw)
    }

post = api.model('posts', postModel)

ps = api.namespace('post')


@ps.route('/')
class Post(Resource):

    @api.expect(upload_parser)
    def post(self):
        # print(json.dumps(api.payload, default=my_handler))

        args = upload_parser.parse_args()
        data = json.loads(args['message'])
        if args.doc:
            file_name = args.doc.filename
            file = args.doc

            print('test ',data)
            print(file_name)
            if file_name and allowed_file(file_name):
                filename = secure_filename(file_name)
                # file.save(filename)
                print(filename)
                destination = os.path.join(app.config['UPLOADS'], './')
                if not os.path.exists(destination):
                    os.makedirs(destination)
                ext = get_ext(filename)

                name = str(uuid.uuid4()) + '.' +  ext

                fileToUpload = '%s%s' % (destination, name)
                Docurl = 'http://192.168.43.136:900/' + name
                file.save(fileToUpload)
                data['doc'] = {}
                data['doc']['uri'] = Docurl
                data['doc']['name'] = filename



        if args.file:

            image_name = args.file.filename
            file = args.file
            print('test ',data)
            # print(image_name)
            if image_name and allowed_file(image_name):
                imagename = secure_filename(image_name)
                # file.save(filename)
                # print(imagename)
                destination = os.path.join(app.config['UPLOADS'], './')
                if not os.path.exists(destination):
                    os.makedirs(destination)
                ext = get_ext(imagename)
                print(ext)
                Iname = str(uuid.uuid4()) + '.' +  ext
                print(Iname)
                imageUpload = '%s%s' % (destination, Iname)
                Imageurl = 'http://192.168.43.136:900/' + Iname
                file.save(imageUpload)
                data['image'] = Imageurl
        print(data)
        post = mongo.db.post
        post.insert(data)
        data = post.find()
        pdata = []
        for i in data:
            ndata = json.dumps(i, default=my_handler)
            ldata = loads(ndata, object_hook=json_util.object_hook)
            print('test  ',ldata)
            pdata.append(ldata)
        return pdata,201
        # return 201

    # @api.marshal_with(post)
    def get(self):
        post = mongo.db.post
        data = post.find()
        pdata = []
        for i in data:
            ndata = json.dumps(i, default=my_handler)
            ldata = loads(ndata, object_hook=json_util.object_hook)
            print('test  ',ldata)
            pdata.append(ldata)
        return pdata,200


@ps.route('/<ObjectId:id>')
class Posts(Resource):

    def delete(self, id):
        post = mongo.db.post
        data = post.remove(id)
        if data:
            return {'message': 'post deleted!', 'status': 200},200
        else:
            return {'error': 'unable to delete post',  'status': 400},400\

likeModel =  {
      "_id": fields.String(readonly=True,),
      "user_id": fields.String(),
    }

like = api.model('like', likeModel)

ls = api.namespace('like')
@ls.route('/<ObjectId:id>/')
class Like(Resource):

    @api.expect(like)
    def post(self,id):
        payload = api.payload['user_id']

        post = mongo.db.post
        check = post.find({},{'like':payload,'_id':id})
        for i in check:

            if len(i['like']) == 0:
                update = post.update({'_id': id},
                                   {
                                       '$push': {'like': payload}
                                   },
                                  upsert= True
                                    )
                print(update)
                if update:
                    data = post.find()
                    posts = []
                    for i in data:
                        sdata = json.dumps(i, default=my_handler)
                        jdata = loads(sdata, object_hook=json_util.object_hook)

                        posts.append(jdata)
                    return posts,201
            else:
                remove = post.update({'_id': id},
                                     {
                                         '$pull':{'like': payload}
                                     },
                                     upsert=True)
                print(remove)
                if remove:
                    data = post.find()
                    posts = []
                    for i in data:
                        sdata = json.dumps(i, default=my_handler)
                        jdata = loads(sdata, object_hook=json_util.object_hook)

                        posts.append(jdata)
                    return posts,201
        # return 201


@ps.route('/comment/<ObjectId:id>/')
class PostUpdate(Resource):
    @api.expect(upload_parser)
    def put(self,id):
        args = upload_parser.parse_args()
        data = json.loads(args['message'])
        if args.doc:
            file_name = args.doc.filename
            file = args.doc

            print('test ',data)
            print(file_name)
            if file_name and allowed_file(file_name):
                filename = secure_filename(file_name)
                # file.save(filename)
                print(filename)
                destination = os.path.join(app.config['UPLOADS'], './')
                if not os.path.exists(destination):
                    os.makedirs(destination)
                ext = get_ext(filename)
                name = str(uuid.uuid4()) + '.' +  ext
                fileToUpload = '%s%s' % (destination, name)
                Docurl = 'http://192.168.43.136:900/' + name
                file.save(fileToUpload)
                data['doc'] = {}
                data['doc']['uri'] = Docurl
                data['doc']['name'] = filename
        if args.file:

            image_name = args.file.filename
            file = args.file
            print('test ',data)
            # print(image_name)
            if image_name and allowed_file(image_name):
                imagename = secure_filename(image_name)
                # file.save(filename)
                # print(imagename)
                destination = os.path.join(app.config['UPLOADS'], './')
                if not os.path.exists(destination):
                    os.makedirs(destination)
                ext = get_ext(imagename)
                print(ext)
                Iname = str(uuid.uuid4()) + '.' +  ext
                print(Iname)
                imageUpload = '%s%s' % (destination, Iname)
                Imageurl = 'http://192.168.43.136:900/' + Iname
                file.save(imageUpload)
                data['image'] = Imageurl
        print(data)
        post = mongo.db.post
        update = post.update({'_id':id},
                           {
                               '$push': {'comment': data}
                           },
                          upsert= True
                            )
        if update:
            data = post.find()
            pdata = []
            for i in data:
                ndata = json.dumps(i, default=my_handler)
                ldata = loads(ndata, object_hook=json_util.object_hook)
                print('test  ',ldata)
                pdata.append(ldata)
                return pdata,200
        else:
            return {'error': 'unable to delete post',  'status': 400},400


commentModel = {
    "_id": fields.String(readonly=True,),
      "message": fields.String("message"),
      "title": fields.String("title"),

      "username": fields.String("username"),
      "postId" : fields.String("class"),
      "doc": fields.String("doc"),
      "image": fields.String("docUri"),
      "created": fields.String("Sun Apr 05 2020 21:16:01 GMT+0100 (West Africa Standard Time)"),
    }

comment = api.model('comment', commentModel)

coms = api.namespace('comment')
@coms.route('/rmcomment/<ObjectId:id>/')
class CommentUpdate(Resource):
    @api.expect(comment)
    def put(self,id):
        data= api.payload
        post = mongo.db.post
        print(data)
        remove = post.update({'_id': id},
                                     {
                                         '$pull':{'comment': data}
                                     },
                                     upsert=True)
        print(remove)
        if remove:
            data = post.find()
            posts = []
            for i in data:
                sdata = json.dumps(i, default=my_handler)
                jdata = loads(sdata, object_hook=json_util.object_hook)

                posts.append(jdata)
            return posts,200



#assignment
assignmentModel =  {
    "_id": fields.String(readonly=True,),
      "duedate": fields.String("Duedate"),
      "title": fields.String("title"),
      "attachment": fields.List(fields.Raw),
      "guide": fields.String("guide"),
      "classId": fields.Integer(),
      "groupId": fields.String("groupId"),
      "created": fields.String("created when"),
      "file": fields.List(fields.Raw,readonly=True),
      "form": fields.List(fields.Raw,readonly=True)

    }
assignment = api.model('assignments', assignmentModel)

ps = api.namespace('assignment')
@ps.route('/')
class Assignment(Resource):
    @api.marshal_with(assignment)
    def get(self):
        assignment = mongo.db.assignment
        data = assignment.find()
        adata = []
        for i in data:
            ndata = json.dumps(i, default=my_handler)
            ldata = loads(ndata, object_hook=json_util.object_hook)
            print('test  ',ldata)
            adata.append(ldata)
        return adata,200


    @api.expect(upload_parser)
    def post(self):
        args = upload_parser.parse_args()
        data = json.loads(args['message'])
        if args.doc:
            file_name = args.doc.filename
            file = args.doc

            print('test ',data)
            print(file_name)
            if file_name and allowed_file(file_name):
                filename = secure_filename(file_name)
                # file.save(filename)
                print(filename)
                destination = os.path.join(app.config['UPLOADS'], './')
                if not os.path.exists(destination):
                    os.makedirs(destination)
                ext = get_ext(filename)
                name = str(uuid.uuid4()) + '.' +  ext
                fileToUpload = '%s%s' % (destination, name)
                Docurl = 'http://192.168.43.136:900/' + name
                file.save(fileToUpload)
                data['uri'] = Docurl
                data['name'] = name
        assignment = mongo.db.assignment
        data['form'] = []
        assignment.insert(data)
        data = assignment.find()
        adata = []
        for i in data:
            ndata = json.dumps(i, default=my_handler)
            ldata = loads(ndata, object_hook=json_util.object_hook)

            adata.append(ldata)
        return adata,201


@ps.route('/class/<ObjectId:id>')
class ClassAssignments(Resource):

    # @api.marshal_list_with(assignment)
    def get(self,id):
        assignment = mongo.db.assignment
        data = assignment.find({"_id":id})

        adata = []
        for i in data:
            ndata = json.dumps(i, default=my_handler)
            ldata = loads(ndata, object_hook=json_util.object_hook)
            adata.append(ldata)
            # print(ndata)

        return adata[0]['form'],200

    @api.expect(assignment)
    def post(self,id):
            assignment = mongo.db.assignment
            data=assignment.update({'_id': id},{'$set':{'form':api.payload['task_data']}},upsert=True)
            print(data)
            # print(api.payload['task_data'])
            return  api.payload,200



@ps.route('/answer/<aid>/<cid>/<sid>')
class AssignmentAnswer(Resource):

    # @api.marshal_list_with(assignment)
    def get(self,aid,cid,sid):
        answer = mongo.db.assignment_answer
        data = answer.find_one({'assignmentId':aid,'classId':cid,'student':sid})
        print('check',data)

        if data == None:
            return [],200
        else:
            print('check',data['answer'])
            return data['answer'],200

        # return adata,200

    # @api.expect(assignment)
    def post(self,aid,cid,sid):
            answer = mongo.db.assignment_answer
            # data=answer.update({'_id': id},{'$set':{'form':api.payload['task_data']}},upsert=True)
            data = answer.find_one({'assignmentId':aid,'classId':cid,'student':sid})

            # print('test i',data)
            if data == None:
                payload = {}
                payload['assignmentId'] = aid
                payload['classId'] = cid
                payload['student'] = sid
                payload['answer'] = api.payload
                data= answer.insert(payload)
                # print(data)
                print(api.payload)
                return  api.payload,200
            else:
                payload = {}
                payload['assignmentId'] = aid
                payload['classId'] = cid
                payload['student'] = sid
                payload['answer'] = api.payload
                answer.update({'assignmentId':aid,'classId':cid,'student':sid},{'$set':{'answer':api.payload}},upsert=True)
                # print(data)
                print(api.payload)
                return  api.payload,200

@ps.route('/<ObjectId:id>')
class Assignments(Resource):

    @api.marshal_list_with(assignment)
    def get(self,id):
        assignment = mongo.db.assignment
        data = assignment.find({"classId":id})

        adata = []
        for i in data:
            ndata = json.dumps(i, default=my_handler)
            ldata = loads(ndata, object_hook=json_util.object_hook)
            adata.append(ldata)
            print(ndata)

        return adata,200



    def delete(self, id):
        assignment = mongo.db.assignment
        data = assignment.remove({'_id':id})
        if data:
            return {'message': 'post deleted!', 'status': 200},200
        else:
            return {'error': 'unable to delete post',  'status': 400}, 400

#studentgroup

groupModel =  {
      "_id": fields.String(readonly=True,),
      "classId": fields.Integer(),
      "studentId": fields.Integer(),
      "name": fields.String("name"),
      "groupId": fields.String("group id"),
      "purpose": fields.String("purpose for group")
    }


studentgroup = api.model('student_group', groupModel)
ps = api.namespace('student_group')
@ps.route('/', endpoint="student_group")
class StudentGroup(Resource):

    @api.expect(studentgroup)
    def post(self):
        student = mongo.db.student_group
        student.insert(api.payload)
        data = student.find()
        gdata = []
        for i in data:
            sdata = json.dumps(i, default=my_handler)
            jdata = loads(sdata, object_hook=json_util.object_hook)

            gdata.append(jdata)
        return gdata,201



    @api.marshal_with(studentgroup)
    def get(self):
        student = mongo.db.student_group

        data = student.find()
        gdata = []
        for i in data:
            sdata = json.dumps(i, default=my_handler)
            jdata = loads(sdata, object_hook=json_util.object_hook)

            gdata.append(jdata)
        return gdata,200

ps = api.namespace('student_group')
@ps.route('/<ObjectId:id>')
class StudentGroups(Resource):

    def delete(self, id):
        student = mongo.db.student_group
        student.remove(id)
        data = student.find()
        gdata = []
        for i in data:
            sdata = json.dumps(i, default=my_handler)
            jdata = loads(sdata, object_hook=json_util.object_hook)

            gdata.append(jdata)
        return gdata,200



classGroupModel =  {
        "_id":fields.String(readonly=True,),
      "max": fields.String("max"),
      "classId": fields.Integer(),
      "purpose": fields.String("purpose"),
      "created": fields.String("Sun Apr 05 2020 21:16:01 GMT+0100 (West Africa Standard Time)"),
      "name": fields.String("name"),
       "class": fields.String("class Name")
    }


classgroup = api.model('class_group', classGroupModel)

ps = api.namespace('class_group')

@ps.route('/',endpoint="class_group")
class ClassGroup(Resource):

    @api.expect(classgroup)
    def post(self):
        classes = mongo.db.class_group
        classes.insert(api.payload)
        data = classes.find()
        gdata = []
        for i in data:
            sdata = json.dumps(i, default=my_handler)
            jdata = loads(sdata, object_hook=json_util.object_hook)

            gdata.append(jdata)
        return gdata,201

    @api.marshal_with(classgroup)
    def get(self):
        classes = mongo.db.class_group
        data = classes.find()
        gdata = []
        for i in data:
            sdata = json.dumps(i, default=my_handler)
            jdata = loads(sdata, object_hook=json_util.object_hook)

            gdata.append(jdata)
        return gdata,200

@ps.route('/<ObjectId:id>')
class ClassGroups(Resource):

    def delete(self, id):
        classes = mongo.db.class_group
        classes.remove(id)
        data = classes.find()
        gdata = []
        for i in data:
            sdata = json.dumps(i, default=my_handler)
            jdata = loads(sdata, object_hook=json_util.object_hook)

            gdata.append(jdata)
        return gdata,200
#folders
folderModel =  {
    "_id": fields.String(readonly=True,),
      "name": fields.String("name"),
      "class": fields.String("class"),
      "groups": fields.String("group"),

    }

folder = api.model('folder', folderModel)

fs = api.namespace('folder')

@fs.route('/', endpoint="folder")
class Folder(Resource):

    @api.expect(folder)
    def post(self):
        folder = mongo.db.folder
        folder.insert(api.payload)
        data = folder.find()
        fdata = []
        for i in data:
            sdata = json.dumps(i, default=my_handler)
            jdata = loads(sdata, object_hook=json_util.object_hook)

            fdata.append(jdata)
        return fdata,201

    @api.marshal_with(folder)
    def get(self):
        folder = mongo.db.folder

        data = folder.find()
        fdata = []
        for i in data:
            sdata = json.dumps(i, default=my_handler)
            jdata = loads(sdata, object_hook=json_util.object_hook)

            fdata.append(jdata)
        return fdata,200

#files

@fs.route('/<ObjectId:id>')
class Folders(Resource):

    def delete(self, id):
        folder = mongo.db.folder
        folder.remove(id)
        data = folder.find()
        fdata = []
        for i in data:
            sdata = json.dumps(i, default=my_handler)
            jdata = loads(sdata, object_hook=json_util.object_hook)

            fdata.append(jdata)
        return fdata,200


fileModel =  {
      "_id": fields.String(readonly=True),
      "name": fields.String("name"),
      "class": fields.String("class"),
      "groups": fields.String("group"),
      "uri": fields.String("uri"),
      "size": fields.String("size"),
       "folder": fields.String("folder")
    }

file = api.model('file', fileModel)

fs = api.namespace('file')

@fs.route('/',endpoint="file")
class File(Resource,):

    @api.expect(upload_parser)
    def post(self):
        args = upload_parser.parse_args()
        data = json.loads(args['message'])
        if args.doc:
            file_name = args.doc.filename
            file = args.doc

            print('test ',data)
            print(file_name)
            if file_name and allowed_file(file_name):
                filename = secure_filename(file_name)
                # file.save(filename)
                print(filename)
                destination = os.path.join(app.config['UPLOADS'], './')
                if not os.path.exists(destination):
                    os.makedirs(destination)
                ext = get_ext(filename)
                name = str(uuid.uuid4()) + ext
                fileToUpload = '%s%s' % (destination, name)
                Docurl = 'http://192.168.43.136:900/' + name
                file.save(fileToUpload)
                data['uri'] = Docurl
                data['name'] = name
        file = mongo.db.files
        file.insert(data)
        data = file.find()
        fdata = []
        for i in data:
            sdata = json.dumps(i, default=my_handler)
            jdata = loads(sdata, object_hook=json_util.object_hook)

            fdata.append(jdata)
        return fdata,201

    @api.marshal_with(file)
    def get(self):
        file = mongo.db.files

        data = file.find()
        fdata = []
        for i in data:
            sdata = json.dumps(i, default=my_handler)
            jdata = loads(sdata, object_hook=json_util.object_hook)

            fdata.append(jdata)
        return fdata,200


files = api.model('file', fileModel)

fs = api.namespace('file')
@fs.route('/<ObjectId:id>')
class Files(Resource):


    def delete(self, id):
        file = mongo.db.files
        file.remove(id)
        data = file.find()
        fdata = []
        for i in data:
            sdata = json.dumps(i, default=my_handler)
            jdata = loads(sdata, object_hook=json_util.object_hook)

            fdata.append(jdata)
        return fdata,200


#assignment
quizModel = {
    "_id": fields.String(readonly=True,),
      "duedate": fields.String("due"),
      "title": fields.String("title"),
      "attachment": fields.List(fields.Raw),
      "guide": fields.String("guide"),
      "classId": fields.String("class"),
      "groupId": fields.String("groupId"),
      "created": fields.String("Sun Apr 05 2020 21:16:01 GMT+0100 (West Africa Standard Time)")
    }

quiz = api.model('quiz', quizModel)

ps = api.namespace('quiz')
@ps.route('/')
class Quiz(Resource):

    @api.expect(upload_parser)
    def post(self):
        args = upload_parser.parse_args()
        data = json.loads(args['message'])
        if args.doc:
            file_name = args.doc.filename
            file = args.doc

            print('test ',data)
            print(file_name)
            if file_name and allowed_file(file_name):
                filename = secure_filename(file_name)
                # file.save(filename)
                print(filename)
                destination = os.path.join(app.config['UPLOADS'], './')
                if not os.path.exists(destination):
                    os.makedirs(destination)
                ext = get_ext(filename)
                name = str(uuid.uuid4()) + '.' + ext
                fileToUpload = '%s%s' % (destination, name)
                Docurl = 'http://192.168.43.136:900/' + name
                file.save(fileToUpload)
                data['uri'] = Docurl
                data['name'] = name
        quiz = mongo.db.quiz
        quiz.insert(data)
        data = quiz.find()
        qdata = []
        for i in data:
            sdata = json.dumps(i, default=my_handler)
            jdata = loads(sdata, object_hook=json_util.object_hook)

            qdata.append(jdata)
        return qdata,201

    @api.marshal_with(quiz)
    def get(self):
        quiz = mongo.db.quiz
        data = quiz.find()
        qdata = []
        for i in data:
            sdata = json.dumps(i, default=my_handler)
            jdata = loads(sdata, object_hook=json_util.object_hook)

            qdata.append(jdata)
        return qdata,200


@ps.route('/class/<int:id>')
class OneQuiz(Resource):

    @api.marshal_with(quiz)
    def get(self,id):
        quiz = mongo.db.quiz
        data = quiz.find({"classId":id})
        qdata = []
        for i in data:
            sdata = json.dumps(i, default=my_handler)
            jdata = loads(sdata, object_hook=json_util.object_hook)
            qdata.append(jdata)

        return qdata,200


@ps.route('/<ObjectId:id>')
class OneQuiz(Resource):

    @api.marshal_with(quiz)
    def get(self,id):
        quiz = mongo.db.quiz
        data = quiz.find(id)
        qdata = []
        for i in data:
            sdata = json.dumps(data, default=my_handler)
            jdata = loads(sdata, object_hook=json_util.object_hook)
            qdata.append(jdata)

        return qdata,200

    def delete(self, id):
        quiz = mongo.db.quiz
        quiz.remove(id)
        data = quiz.find()
        jdata = []
        for i in data:
            sdata = json.dumps(i, default=my_handler)
            jdata = loads(sdata, object_hook=json_util.object_hook)

            jdata.append(jdata)
        return jdata,200


messageModel =  {
      "_id": fields.String(readonly=True,),
      "text": fields.String("message"),
      "user": fields.Raw(),
      "user_id": fields.String(),
        "createdAt": fields.DateTime(),
      "read": fields.Boolean(),
      "token": fields.String("token"),
    }


msg = api.model('message', messageModel)

ps = api.namespace('message')
@ps.route('/')
class Message(Resource):

    @api.expect(msg)
    def post(self):
        msg = mongo.db.message
        msg.insert(api.payload)
        data = msg.find()
        msgs = []
        for i in data:
            sdata = json.dumps(i, default=my_handler)
            jdata = loads(sdata, object_hook=json_util.object_hook)

            msgs.append(jdata)
        return msgs,201


@ps.route('/user/<int:user>/<int:res>')
class UserMessage(Resource):
    @api.marshal_with(msg)
    def get(self,user,res):
        msg = mongo.db.message
        data = msg.find({"user._id":user,"recepient":res}).sort("createdAt",-1)
        rdata = msg.find({"user._id":res,"recepient":user}).sort("createdAt",-1)
        mdata = []
        for i in data:

            sdata = json.dumps(i, default=my_handler)
            jdata = loads(sdata, object_hook=json_util.object_hook)
            mdata.append(jdata)
        for i in rdata:
            # print(i)
            sdata = json.dumps(i, default=my_handler)
            jdata = loads(sdata, object_hook=json_util.object_hook)
            mdata.append(jdata)
        print(mdata)
        # sorted(mdata, key=itemgetter('createdAt'))
        return mdata,200


@ps.route('/<ObjectId:id>')
class Messages(Resource):

    # @api.marshal_with(msg)
    # def get(self,id):
    #     msg = mongo.db.message
    #     data = msg.find_one({})
    #
    #
    #     sdata = json.dumps(data, default=my_handler)
    #     jdata = loads(sdata, object_hook=json_util.object_hook)


        # return jdata,200

    def delete(self, id):
        msg = mongo.db.message
        msg.remove(id)
        data = msg.find()
        msgs = []
        for i in data:
            sdata = json.dumps(i, default=my_handler)
            jdata = loads(sdata, object_hook=json_util.object_hook)

            msg.append(jdata)
        return msgs,201


uploadModel =  {
      # "_id": fields.String(readonly=True,),
      "name": fields.String("message")

    }


upd = api.model('upload', uploadModel)

ps = api.namespace('upload')
@ps.route('/')
class Uploads(Resource):

    @api.expect(upload_parser)
    def post(self):
        args = upload_parser.parse_args()
        print(args)


        return 200
        # except  :
        #
        #     return {"error":'unknown'},400


@ps.route('/<classId>')
class uploaded(Resource):

    def get(self,classId):
        # asgn = mongo.db.assignment
        # args = upload_parser.parse_args()
        # print(args)
        print(classId)
        return  200

    def post(self,classId):
        asgn = mongo.db.assignment
        asgn.find()
        print(api.payload)
        return 200


if __name__ == '__main__':
  app.run(host='0.0.0.0',port='5000',debug=True)
