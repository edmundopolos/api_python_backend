
# from flask_restplus import Api, Resource, fields
from important import *
from warehouse_db import *
from library_db import *
from account_db import *
from quiz_assignment_db import *
from hostel_db import *

from operator import itemgetter
app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/mschool'
app.config["UPLOADS"] = "/var/www/files/"
app.config["IP"] = 'http://0.0.0.0:900/'
app.config["login"] = '0.0.0.0:8000'
CORS(app)
mongo =PyMongo(app)
# app.wsgi_app = ProxyFix(app.wsgi_app)
authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'x-access-token'
    }
}
blueprint = Blueprint('Mschool', __name__)
api = Api(app, authorizations=authorizations) #,doc=False
app.register_blueprint(blueprint)
app.app_context().push()
app.config['SECRET_KEY'] = 'super-secret'
upload_parser = api.parser()
upload_parser.add_argument('file', location='files',
                           type=FileStorage)
upload_parser.add_argument('message', location='form')
# upload_parser.add_argument('teacher_id', location='form')
upload_parser.add_argument('doc', location='files',
                           type=FileStorage)


def token_required(func):
    @wraps(func)
    def actions(*args,**kwargs):

        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
            # print(json.dumps(token),'here')

        if not token:
            return {'message' : 'Token is missing!'}, 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])

            current_user = data['user']
            print('here',current_user)
        except:
            print({'message': 'Token is invalid'})
            return {'message' : 'Token is invalid!!'}, 401
        # return func(**args,**kwargs)


    return api.doc(security='apikey')(func)
    # return actions


#
#


# def apikey(token_required):
#     return api.doc(security='token_required')(token_required)



loginModel = {
    "username": fields.String("username"),
    "password": fields.String("password")
}
l = api.model('login', loginModel)

ln = api.namespace('login')
@ln.route('/')
class Login(Resource):

    @api.expect(l)
    def post(self):
        username = api.payload['username']
        password = api.payload['password']
        print(password)
        secret_key = '_THIS_na_MY_32_CHARS_SECRET_KEY_'
        encrypted = password
        encrypted = encrypted.split(':')
        # We decode the two bits independently
        nonce = b64decode(encrypted[0])
        encrypted = b64decode(encrypted[1])
        # We create a SecretBox, making sure that out secret_key is in bytes
        box = SecretBox(bytes(secret_key, encoding='utf8'))
        decrypted = box.decrypt(encrypted, nonce).decode('utf-8')
        print(decrypted)
        if username and password:
            url = 'http://'+app.config['login']+'/api/user'
            s = requests.session()
            payload = {
                "username": username,
                "password": decrypted

            }
            r = s.post(url, headers={"Content-Type": "application/json"}, data=json.dumps(payload))
            res = str(r.status_code)
            data = r.json()
            # print(data)
            if res == '200':
                print(r.json())
                data['username'] = username
                token = jwt.encode({'user':data, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
                # print(token)
                return jsonify({'token' : token.decode('UTF-8'), 'name': data['name'], 'role': data['role'], 'id': data['id'],'username':username, 'email': data['email'], 'ph': data['ph']})

        else:
            return {'data': "incorrect credentials"},401


#getClasses

cls = api.namespace('allClasses')
@cls.route('/')
class Classes(Resource):


    def get(self):
        url = 'http://0.0.0.0:8000/api/allclasses/'
        s = requests.session()

        r = s.get(url, headers={"Content-Type": "application/json"})
        res = str(r.status_code)
        data = r.json()
        if res == '200':
            # print(r.json())
            return data,200
        else:
            return 404

#get users
ussModel = {
    "username": fields.String("username"),
    "password": fields.String("password")
}
uss = api.model('login', ussModel)
us = api.namespace('allUsers')
@us.route('/')
class AllUsers(Resource):


    def get(self):
        url = 'http://0.0.0.0:8000/api/users/'
        s = requests.session()

        r = s.get(url, headers={"Content-Type": "application/json"})
        res = str(r.status_code)
        data = r.json()
        if res == '200':
            # print(r.json())
            return data,200
        else:
            return 404


#all students

us = api.namespace('students')
@us.route('/')
class AllUsers(Resource):


    def get(self):
        url = 'http://0.0.0.0:8000/api/students/'
        s = requests.session()

        r = s.get(url, headers={"Content-Type": "application/json"})
        res = str(r.status_code)
        data = r.json()
        if res == '200':
            # print(r.json())
            return data,200
        else:
            return 404


@us.route('/borders')
class AllBorders(Resource):
    def get(self):
        url = 'http://0.0.0.0:8000/api/students/borders/'
        s = requests.session()
        r = s.get(url, headers={"Content-Type": "application/json"})
        res = str(r.status_code)
        data = r.json()
        if res == '200':
            # print(r.json())
            return data,200
        else:
            return 404







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
        print("got here",args)
        if args.file:

            imgname = args.file.filename
            file = args.file

            print(imgname)
            if imgname and allowed_file(imgname):
                imagename = secure_filename(imgname)
                # file.save(filename)
                print('here',imagename)
                destination = os.path.join(app.config['UPLOADS'], '')
                if not os.path.exists(destination):
                    os.makedirs(destination)
                ext = get_ext(imagename)
                print(ext)
                Iname = str(uuid.uuid4()) + '.' +  ext
                print(Iname)
                imageUpload = '%s%s' % (destination, Iname)
                Imageurl =  Iname
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

#logo
logoModel =  {
    "_id": fields.String(readonly=True,),

      "attachment": fields.List(fields.Raw),


    }
logo = api.model('logo', logoModel)

ps = api.namespace('logo')
@ps.route('/')
class Assignment(Resource):

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
                destination = os.path.join(app.config['UPLOADS']/logo, '')
                if not os.path.exists(destination):
                    os.makedirs(destination)
                ext = get_ext(filename)
                name = str(uuid.uuid4()) + '.' +  ext
                fileToUpload = '%s%s' % (destination, name)
                Docurl =  name
                file.save(fileToUpload)
                data['uri'] = Docurl
                data['name'] = name

        return 201


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
      "comments": fields.List(fields.Raw),

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
                destination = os.path.join(app.config['UPLOADS'], '')
                if not os.path.exists(destination):
                    os.makedirs(destination)
                ext = get_ext(filename)

                name = str(uuid.uuid4()) + '.' +  ext

                fileToUpload = '%s%s' % (destination, name)
                Docurl =  name
                file.save(fileToUpload)
                data['doc'] = {}
                data['doc']['uri'] = Docurl
                data['doc']['name'] = filename



        if args.file:

            image_name = args.file.filename
            file = args.file
            print('test ',file)
            # print(image_name)
            if image_name and allowed_file(image_name):
                imagename = secure_filename(image_name)
                # file.save(filename)
                # print(imagename)
                destination = os.path.join(app.config['UPLOADS'], '')
                if not os.path.exists(destination):
                    os.makedirs(destination)
                ext = get_ext(imagename)
                print(ext)
                Iname = str(uuid.uuid4()) + '.' +  ext
                print(Iname)
                imageUpload = '%s%s' % (destination, Iname)
                Imageurl =  Iname
                file.save(imageUpload)
                data['image'] = Imageurl
        print('show',data)
        post = mongo.db.post
        post.insert(data)
        data = post.find()
        pdata = []
        for i in data:
            ndata = json.dumps(i, default=my_handler)
            ldata = loads(ndata, object_hook=json_util.object_hook)
            # print('test  ',ldata)
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
            # print('test  ',ldata)
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

    # @api.expect(like)
    def post(self,id):
        print(api.payload)
        payload = api.payload['user_id']

        post = mongo.db.post
        check = post.find_one({'_id':id})

        if len(check['like']) == 0:
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
                destination = os.path.join(app.config['UPLOADS'], '')
                if not os.path.exists(destination):
                    os.makedirs(destination)
                ext = get_ext(filename)
                name = str(uuid.uuid4()) + '.' +  ext
                fileToUpload = '%s%s' % (destination, name)
                Docurl =  name
                file.save(fileToUpload)
                data['doc'] = {}
                data['doc']['uri'] = Docurl
                data['doc']['name'] = filename
        if args.file:

            image_name = args.file.filename
            file = args.file
            # print('test ',data)
            # print(image_name)
            if image_name and allowed_file(image_name):
                imagename = secure_filename(image_name)
                # file.save(filename)
                # print(imagename)
                destination = os.path.join(app.config['UPLOADS'], '')
                if not os.path.exists(destination):
                    os.makedirs(destination)
                ext = get_ext(imagename)
                print(ext)
                Iname = str(uuid.uuid4()) + '.' +  ext
                print(Iname)
                imageUpload = '%s%s' % (destination, Iname)
                Imageurl =  Iname
                file.save(imageUpload)
                data['image'] = Imageurl
        # print(data)
        post = mongo.db.post
        update = post.update({'_id':id},
                           {
                               '$push': {'comment': data}
                           },
                          upsert= True
                            )
        if update:

            data = post.find()
            posts = []
            for i in data:
                sdata = json.dumps(i, default=my_handler)
                jdata = loads(sdata, object_hook=json_util.object_hook)

                posts.append(jdata)
            return posts,200
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
                print('comment',posts)
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
                destination = os.path.join(app.config['UPLOADS'], '')
                if not os.path.exists(destination):
                    os.makedirs(destination)
                ext = get_ext(filename)
                name = str(uuid.uuid4()) + '.' +  ext
                fileToUpload = '%s%s' % (destination, name)
                Docurl =  name
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


@ps.route('/class/<int:id>')
class ClassAssignments(Resource):

    # @api.marshal_list_with(assignment)
    def get(self,id):
        assignment = mongo.db.assignment
        data = assignment.find({"classId":id})
        print(data)
        adata = []
        for i in data:
            ndata = json.dumps(i, default=my_handler)
            ldata = loads(ndata, object_hook=json_util.object_hook)
            adata.append(ldata)
            print(ndata)

        return adata,200


@ps.route('/form/<ObjectId:id>')
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
        print('outta',adata)
        adata[0]['form'][0]['duedate'] = adata[0]['duedate']

        return adata[0]['form'],200

    @api.expect(assignment)
    def post(self,id):
            assignment = mongo.db.assignment
            print('testing',api.payload)
            data=assignment.update({'_id': id},{'$set':{'form':api.payload['task_data']}},upsert=True)
            print(data)
            # print(api.payload['task_data'])
            return  api.payload,200


@ps.route('/answers/<aid>')
class AssignmentAnswers(Resource):


    def get(self,aid):
        answer = mongo.db.assignment_answer
        data = answer.find({'assignmentId':aid})
        adata = []
        for i in data:
            ndata = json.dumps(i, default=my_handler)
            ldata = loads(ndata, object_hook=json_util.object_hook)
            adata.append(ldata)


        return adata,200



@ps.route('/answer/<aid>/<cid>/<sid>')
class AssignmentAnswer(Resource):


    def get(self,aid,cid,sid):
        answer = mongo.db.assignment_answer
        data = answer.find_one({'assignmentId':aid,'classId':cid,'student':sid})


        if data == None:

            return [],200
        else:
            print('check',data['answer'])
            return data['answer'],200




    def put(self,aid,cid,sid):
        answer = mongo.db.assignment_answer
        answer.update({'assignmentId':aid,'classId':cid,'student':sid},
                             {'$set':{'grade':api.payload['grade']}},upsert=True)
        data = answer.find_one({'assignmentId':aid,'classId':cid,'student':sid})

        if data == None:
            # print('null')
            return [],200
        else:
            # print('check',data['answer'])
            return data['answer'],200

    # @api.expect(assignment)
    def post(self,aid,cid,sid):
            answer = mongo.db.assignment_answer
            # print(api.payload)
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
                print('inseterd')
                print(api.payload)
                return  api.payload,200
            else:
                payload = {}
                payload['assignmentId'] = aid
                payload['classId'] = cid
                payload['student'] = sid
                payload['answer'] = api.payload
                answer.update({'assignmentId':aid,'classId':cid,'student':sid},{'$set':{'answer':api.payload}},upsert=True)
                print('updated')
                print('lle',api.payload)
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
        folder.remove({'_id':id})
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
                destination = os.path.join(app.config['UPLOADS'], '')
                if not os.path.exists(destination):
                    os.makedirs(destination)
                ext = get_ext(filename)
                name = str(uuid.uuid4()) + ext
                fileToUpload = '%s%s' % (destination, name)
                Docurl =  name
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
        file.remove({'_id':id})
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
      "created": fields.String("Sun Apr 05 2020 21:16:01 GMT+0100 (West Africa Standard Time)"),
      "file": fields.List(fields.Raw,readonly=True),
      "form": fields.List(fields.Raw,readonly=True),
      "marks": fields.List(fields.Raw,readonly=True)

    }

quiz = api.model('quiz', quizModel)

ps = api.namespace('quiz')
@ps.route('/')
class Quiz(Resource):

    @api.expect(upload_parser)
    def post(self):
        add_quiz(upload_parser,mongo)


    @api.marshal_with(quiz)
    def get(self):
        get_quiz(mongo)


@ps.route('/class/<int:id>')
class OneClassQuiz(Resource):

    @api.marshal_with(quiz)
    def get(self,id):
        get_one_class_quiz(mongo,id)


@ps.route('/<ObjectId:id>')
class OneQuiz(Resource):

    @api.marshal_with(quiz)
    def get(self,id):
        get_one_quiz(mongo)

    def delete(self, id):
        delete_quiz(mongo,id)

@ps.route('/form/<ObjectId:id>')
class ClassQuizs(Resource):

    # @api.marshal_list_with(assignment)
    def get(self,id):
        get_quiz_form(mongo, id)

    @api.expect(assignment)
    def post(self,id):
            add_quiz_form(mongo, api, id)



@ps.route('/answer/<aid>/<cid>/<sid>')
class QuizAnswer(Resource):

    # @api.marshal_list_with(assignment)
    def get(self,aid,cid,sid):
        get_quiz_answer(mongo, aid, cid, sid)

    def put(self,aid,cid,sid):
        update_quiz_answer(mongo, api, aid, cid, sid)

    # @api.expect(assignment)
    def post(self,aid,cid,sid):
           add_quiz_answer(mongo, api, aid, cid, sid)


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
        data = msg.find({"user._id": user, "recepient": res}).sort("createdAt", -1)
        rdata = msg.find({"user._id": res, "recepient": user}).sort("createdAt", -1)
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



# acyModel =  {
#       # "_id": fields.String(readonly=True,),
#       "id":fields.String(),
#       "title"
#
#     }
#
#
# acyear = api.model('academic_year')

acy = api.namespace('academic_year')
@acy.route('/')
class AcademicYear(Resource):

    @api.expect(upload_parser)
    def get(self):
        url = 'http://0.0.0.0:8000/api/acy/'
        s = requests.session()

        r = s.get(url, headers={"Content-Type": "application/json"})
        res = str(r.status_code)
        data = r.json()
        if res == '200':
            print(r.json())
            return data,200
        else:
            return 404






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


transactionModel =  {
      "_id": fields.String(readonly=True,),
      "reciever": fields.String(),
      "payer": fields.String("message"),
      "type": fields.String(enum=['debit','credit','reversal']),
      "user_id": fields.String(),
      "createdAt": fields.String(),
      "created_by": fields.String(),
      "transaction_date": fields.String(),
      "reason": fields.String(required=True,enum=['Fee charge','Fee Payment','Event Charge','Event Charge','School Payment','School Charge','Misc Bills']),
      "description": fields.String('description'),
      "token": fields.String("token"),
      "amount": fields.Integer(),
      "status": fields.String(enum=['Active','Canceled','Reversed']),
      "reversed": fields.Boolean(),
      "reversed_by": fields.String('null'),
      "canceled_by": fields.String('null'),
      "canceled_on": fields.String('null'),
      "payment_method": fields.String(''),
      "action": fields.String("null")
    }


tt= api.model('transactions', transactionModel)

tc = api.namespace('transactions')

@tc.route('/')
class Transaction(Resource):
    @token_required
    @api.expect(tt)
    def post(self):
        add_transaction(mongo,api)


    # @api.doc(security=apikey)
    @token_required
    @api.marshal_with(tt)
    def get(self):
        e = get_transaction(mongo)
        return e

# @token_required
@tc.route('/<ObjectId:id>')
class TransactionItem(Resource):
    @token_required
    def put(self,id):
        e = update_transaction(mongo, api, id)
        return e



    def get(self,id):
        e = get_one_transaction(mongo, id)
        return e
    @token_required
    def delete(self, id):
        e = delete_transaction(mongo, id)
        return e


@tc.route('/user/<userId>')
class TransactionPerson(Resource):
    @token_required
    @api.marshal_with(tt)
    def get(self, userId):
        e = get_transaction_person(mongo, userId)
        return e



@tc.route('/bill_class/<id>')
class TransactionBill(Resource):
    @api.expect(tt)
    @token_required
    def post(self,id):
        e = bill_class(mongo,api,id)
        return e


classModel =  {
      "_id": fields.String(readonly=True,),
      "sectionName": fields.String("class Name"),
      "classId": fields.String("class Id"),
      "amount": fields.Integer(),
      "sectionId": fields.String(),
      "className": fields.String()

    }

cl= api.model('class_fees', classModel)

tc = api.namespace('class_fees')
# @token_required
@tc.route('/')
class ClassFees(Resource):
    @token_required
    @api.expect(cl)
    def post(self):
        e = set_fee(mongo,api)
        return e


    @token_required
    @api.marshal_with(cl)
    def get(self):
        e = get_fee(mongo)
        return e

@tc.route('/<ObjectId:id>')
class DeleteFee(Resource):
    # @api.marshal_with(py)
    def delete(self,id):
        e = delete_fee(mongo,id)
        return e


ttableModel =  {
      "_id": fields.String(readonly=True,),
      "event": fields.Raw()
    }

ttable= api.model('time_table', ttableModel)

ttb = api.namespace('time_table')
# @token_required
@ttb.route('/')
class TimeTable(Resource):

    @api.expect(ttable)
    def post(self):

            t = mongo.db.timetable
            data = t.find({})
            print(data)
            if data == None:
                t.insert(api.payload)
                print(api.payload)
                data = t.find()
                all_tranx =[]
                for i in data:
                    sdata = json.dumps(i, default=my_handler)
                    jdata = loads(sdata, object_hook=json_util.object_hook)

                    all_tranx.append(jdata)
                return all_tranx,201
            else:
                print('here')
                t.update({},{'$set':{'event':api.payload['event']}},upsert=True)
                data = t.find()
                all_tranx =[]
                for i in data:
                    sdata = json.dumps(i, default=my_handler)
                    jdata = loads(sdata, object_hook=json_util.object_hook)
                    all_tranx.append(jdata)
                return all_tranx,200


    @api.marshal_with(ttable)
    def get(self):
        t = mongo.db.timetable
        data = t.find()
        all_tranx =[]
        for i in data:
            sdata = json.dumps(i, default=my_handler)
            jdata = loads(sdata, object_hook=json_util.object_hook)

            all_tranx.append(jdata)
        return all_tranx,200


payModel =  {
      "_id": fields.String(readonly=True,),
      "name": fields.String("name"),
    }

py= api.model('payment_config', payModel)

pc = api.namespace('payment_config')
@pc.route('/')
class Payment(Resource):

    @api.expect(py)
    def post(self):
        e = payment_config(mongo,api)
        return e


    @token_required
    @api.marshal_with(py)
    def get(self):
        e = get_payment_config(mongo,api)
        return e


@pc.route('/<ObjectId:id>')
class PaymentAction(Resource):
    # @api.marshal_with(py)
    @token_required
    def delete(self,id):
        delete_payment_config(mongo,id)


reasonModel =  {
      "_id": fields.String(readonly=True,),
      "name": fields.String("name"),
      "head": fields.String("head")
    }

r= api.model('payment_reason', reasonModel)

r = api.namespace('payment_reason')
@r.route('/')
class Payment(Resource):

    @api.expect(py)
    def post(self):
        e = payment_reason(mongo,api)
        return e

    @token_required
    @api.marshal_with(py)
    def get(self):
        e = get_payment_reason(mongo,api)
        return e


@r.route('/<ObjectId:id>')
class PaymentAction(Resource):
    # @api.marshal_with(py)
    @token_required
    def delete(self,id):
        e = delete_payment_reason(mongo,id)
        return e


warehouseModel =  {
      "_id": fields.String(readonly=True,),
      "location": fields.String("name"),
      "tag": fields.String("tag"),
      "created": fields.String("name"),
      "createdBy": fields.String("name"),
    }

wh= api.model('warehouse', warehouseModel)

w = api.namespace('warehouse')
@w.route('/')
class Warehouse(Resource):
    @token_required
    @api.expect(wh)

    def post(self):

        e = add_location(mongo,api)
        return e

    @api.marshal_with(wh)
    @token_required
    def get(self):

        e = get_location(mongo,api)
        return e


@w.route('/<ObjectId:id>')
class DeleteWarehouse(Resource):
    @token_required
    def delete(self, id):
        # if current_user.role == 'Accountant' or current_user.role == 'Admin':
        e = delete_location(mongo,id)
        return e


warehouseItemModel =  {
      "_id": fields.String(readonly=True,),
      "name": fields.String("name"),
      "expires": fields.String("name"),
      "createdBy": fields.String("name"),
      "created": fields.String(),
      "category": fields.String("category"),
      "type": fields.String("type"),
      "purchased":fields.String("purchased"),
      "quantity": fields.Integer(),
      "batch": fields.String('Batch Number'),
      "location_id": fields.String('Location Id'),
      "vendor": fields.String('Vendor'),
    }

wa= api.model('item', warehouseItemModel)


VendorModel =  {
      "_id": fields.String(readonly=True,),
      "name": fields.String("name"),
      "contact": fields.String("contact"),
      "address": fields.String("address"),
      "created": fields.String("created"),
      "createdBy": fields.String("createdby"),
    }

v= api.model('warehouse', VendorModel)


@w.route('/vendor')
class Warehouse(Resource):
    @token_required
    @api.expect(v)

    def post(self):

        e = add_vendor(mongo,api)
        return e

    @api.marshal_with(v)
    @token_required
    def get(self):

        e = get_vendor(mongo,api)
        return e



@w.route('/item')
class WarehouseOptions(Resource):
    @api.expect(wa)
    def post(self):
        e = add_item(mongo,api)
        return e


    @api.marshal_with(wa)
    def get(self):
        e = get_item(mongo,api)
        return e


warehouseItemModel = {
      "_id": fields.String(readonly=True,),
      "from": fields.Raw(),
      "created": fields.String("name"),
      "createdBy": fields.String("name"),
      "category": fields.String("category"),
      "batch": fields.String(""),
      "purchased": fields.String("procured"),
      "expires": fields.String("null"),
      "name": fields.String('item'),
      "quantity": fields.Integer(),
      "to": fields.Raw(),
      "status": fields.String(''),
      "fromBal": fields.String('')

    }

wd= api.model('dispensery', warehouseItemModel)
@w.route('/dispense')
class WarehouseDispensery(Resource):
    @api.expect(wd)
    def post(self):
        e = add_dispensed(mongo,api)
        return e

    @api.marshal_with(wd)
    def get(self):
        e = get_dispensed(mongo,api)
        return e


@w.route('/return/<ObjectId:id>')
class Return(Resource):
    @api.expect(wd)
    def put(self,id):
        e = update_dispensed(mongo,api,id)
        return e

waModel = {
      "_id": fields.String(readonly=True,),
      "name": fields.String("name"),
      "expires": fields.String("name"),
      "createdBy": fields.String("name"),
      "created": fields.String(),
      "category": fields.String(),
      "type": fields.String(),
      "purchased": fields.String(),
      "quantity": fields.Integer(),
      "batch": fields.String('Batch Number'),
      "location_id": fields.String('Location Id'),
      "from": fields.Raw(),
      "to": fields.Raw(),
      "adjusted": fields.String(''),
      "toBal": fields.String(''),
      "fromBal": fields.String('')
    }


adj= api.model('warehouse', waModel)
@w.route('/adjustment')
class WarehouseAdjustment(Resource):
    @api.expect(adj)
    def post(self):
        e  = add_adjustment(mongo,api)
        return e



    @api.marshal_with(adj)
    def get(self):
        e = get_adjustment(mongo)
        return e


    @token_required
    @api.expect(adj)
    def put(self):
        e = update_adjustment(mongo)
        return e


receiptModel = {
      "_id": fields.String(readonly=True,),
      "name": fields.String("null"),
      "expires": fields.String("null"),
      "createdBy": fields.String("null"),
      "created": fields.String("null"),
      "purchased": fields.String('null'),
      "quantity": fields.Integer(),
      "batch": fields.String('Batch Number'),
      "location_id": fields.String('Location Id'),
      "category": fields.String('Category'),
      "type": fields.String('Type'),
      "vendor": fields.String('Vendor'),
      "amount": fields.String(),
      "to": fields.String('location'),
      "description": fields.String('description')
    }

receipt= api.model('warehouse', receiptModel)


@w.route('/receipt')
class WarehouseReceipts(Resource):
    @api.expect(receipt)
    def post(self):
        e = add_receipt(mongo,api)
        return e

    @api.marshal_with(receipt)
    def get(self):
        e = get_receipt(mongo,api)
        return e


itemModel = {
      "_id": fields.String(readonly=True,),
      "name": fields.String("class Name"),
      "type": fields.String("class Id"),
      "amount": fields.Integer(),
      "category": fields.String(),


    }

item= api.model('sales_item', itemModel)

si = api.namespace('sales_item')
# @token_required
@si.route('/')
class ItemSale(Resource):
    @token_required
    @api.expect(item)
    def post(self):
        e = add_sales_item(mongo,api)
        return e

    @token_required
    @api.marshal_with(item)
    def get(self):
        e = get_sales_item(mongo)
        return e


@tc.route('/<ObjectId:id>')
class DeleteItem(Resource):
    # @api.marshal_with(py)
    def delete(self, id):
        delete_sales_item(mongo,api,id)


attributeModel = {
      "_id": fields.String(readonly=True,),
      "name": fields.String("name"),
      "description": fields.String("description")
    }

at= api.model('item_attribute', attributeModel)

attribute = api.namespace('item_attribute')


@attribute.route('/')
class Attribute(Resource):

    @api.expect(at)
    def post(self):
        e = add_attribute(mongo,api)
        return e

    @token_required
    @api.marshal_with(at)
    def get(self):
        e = get_attribute(mongo,api)
        return e


@r.route('/<ObjectId:id>')
class AttributeAction(Resource):
    # @api.marshal_with(py)
    @token_required
    def delete(self, id):
        e = delete_attribute(mongo,api)
        return e


tagModel = {
      "_id": fields.String(readonly=True,),
      "name": fields.String("name"),
    }

tg = api.model('tag', tagModel)

tag = api.namespace('tag')


@tag.route('/')
class Tags(Resource):

    @token_required
    @api.marshal_with(tg)
    def get(self):
        # if current_user.role == 'Accountant' or current_user.role == 'Admin':
        pay = mongo.db.tag

        print(api.payload)
        data = pay.find()
        mthd = []
        for i in data:
            sdata = json.dumps(i, default=my_handler)
            jdata = loads(sdata, object_hook=json_util.object_hook)

            mthd.append(jdata)
        return mthd, 200

    @api.expect(tg)
    def post(self):
        # if current_user.role == 'Accountant' or current_user.role == 'Admin':
            print('dsdfs',api.payload)
            pay = mongo.db.tag
            pay.insert(api.payload)
            # print(api.payload)
            data = pay.find()
            mthd = []
            for i in data:
                sdata = json.dumps(i, default=my_handler)
                jdata = loads(sdata, object_hook=json_util.object_hook)

                mthd.append(jdata)
            return mthd, 201


@tag.route('/<ObjectId:id>')
class DeleteTag(Resource):
    @token_required
    def delete(self, id):
        # if current_user.role == 'Accountant' or current_user.role == 'Admin':
        pay = mongo.db.tag
        pay.remove({"_id": id})
        data = pay.find()
        mthd = []
        for i in data:
            sdata = json.dumps(i, default=my_handler)
            jdata = loads(sdata, object_hook=json_util.object_hook)

            mthd.append(jdata)
        return mthd, 200
        # else:
        #     return 401


shelfModel = {
      "_id": fields.String(readonly=True,),
      "name": fields.String("name"),
    }

sh = api.model('shelf', tagModel)

shlf = api.namespace('shelf')


@shlf.route('/')
class Shelves(Resource):

    # @token_required
    @api.marshal_with(tg)
    def get(self):
        e = get_shelf(mongo,api)
        return e



    @api.expect(tg)
    def post(self):
        e = add_shelf(mongo,api)
        return e



@shlf.route('/<ObjectId:id>')
class ShelvesTag(Resource):
    @token_required
    def delete(self, id):
        delete_shelf(mongo, id)


LibraryItemModel = {
      "_id": fields.String(readonly=True,),
      "from": fields.Raw(),
      "created": fields.String("name"),
      "createdBy": fields.String("name"),
      "category": fields.String("category"),
      "batch": fields.String(""),
      "purchased": fields.String("procured"),
      "expires": fields.String("null"),
      "name": fields.String('item'),
      "quantity": fields.Integer(),
      "to": fields.Raw(),
      "status": fields.String(''),
      "fromBal": fields.String(''),
      "returnDate": fields.String('return date')

    }


ls = api.namespace('library')
ld = api.model('library', LibraryItemModel)


@ls.route('/lent')
class LibraryDispensery(Resource):
    @api.expect(ld)
    def post(self):
        library_dispensary(mongo,api)

    @api.marshal_with(wd)
    def get(self):
        e = get_library_dispense(mongo,api)
        return e


@ls.route('/lent/<ObjectId:id>')
class Return(Resource):
    @api.expect(wd)
    def put(self, id):
        update_dispensed(mongo,api,id)


laModel = {
      "_id": fields.String(readonly=True,),
      "name": fields.String("name"),
      "expires": fields.String("name"),
      "createdBy": fields.String("name"),
      "created": fields.String(),
      "category": fields.String(),
      "type": fields.String(),
      "purchased": fields.String(),
      "quantity": fields.Integer(),
      "batch": fields.String('Batch Number'),
      "location_id": fields.String('Location Id'),
      "from": fields.Raw(),
      "to": fields.Raw(),
      "adjusted": fields.String(''),
      "toBal": fields.String(''),
      "fromBal": fields.String('')
    }


ladj= api.model('library', laModel)
@ls.route('/adjustment')
class WarehouseAdjustment(Resource):
    @api.expect(ladj)
    def post(self):
        library_adjustment(mongo,api)


    @api.marshal_with(ladj)
    def get(self):
        e = get_library_adjustment(mongo)
        return e


    @token_required
    @api.expect(ladj)
    def put(self):
        update_library_adjustment(mongo,api)


hostelModel = {
      "_id": fields.String(readonly=True,),
      "name": fields.String("name"),
      "description": fields.String("tag"),
      "created": fields.String("name"),
      "createdBy": fields.String("name"),
    }

h= api.model('hostel', hostelModel)

w = api.namespace('hostel')
@w.route('/')
class Hostel(Resource):
    @api.expect(h)
    @token_required
    def post(self):

        e = add_building(mongo,api)
        return e

    @api.marshal_with(h)
    @token_required
    def get(self):

        e = get_building(mongo,api)
        return e


@w.route('/<ObjectId:id>')
class Deletehostel(Resource):
    @token_required
    def delete(self, id):
        # if current_user.role == 'Accountant' or current_user.role == 'Admin':
        e = delete_building(mongo, id)
        return e
    @token_required
    @api.expect(ladj)
    def put(self,id):
        update_building(mongo, api, id)


hostelRoomModel =  {
      "_id": fields.String(readonly=True,),
      "name": fields.String("name"),
      "capacity": fields.String('"capacity'),
      "mix": fields.String('mix'),
      "status": fields.String('status'),
      "description": fields.String("tag"),
      "building": fields.String("building id"),
      "created": fields.String("name"),
      "createdBy": fields.String("name"),
    }

hostel= api.model('hostel_room', hostelRoomModel)


@w.route('/room')
class HostelRoom(Resource):
    @token_required
    @api.expect(hostel)
    def post(self):
        e = add_to_room(mongo,api)
        return e

    @api.marshal_with(hostel)
    @token_required
    def get(self):

        e = get_hostel_rooms(mongo,api)
        return e


@w.route('/room/<ObjectId:id>')
class DeletehostelRoom(Resource):
    @token_required
    def delete(self, id):

        # if current_user.role == 'Accountant' or current_user.role == 'Admin':
        e = delete_hostel_room(mongo,api,id)
        return e

    @token_required
    @api.expect(ladj)
    def put(self,id):
        update_hostel_room(mongo,api,id)

assgnedModel =  {
      "_id": fields.String(readonly=True,),
      "student": fields.Raw(""),
      "hostel": fields.Raw(''),
      "room": fields.Raw(''),
      "capacity": fields.Raw(''),
      "created": fields.String("name"),
      "createdBy": fields.String("name"),
    }

assgned= api.model('assignedhostel', assgnedModel)


@w.route('/assign/room')
class AssignedHostel(Resource):
    @api.expect(assgned)
    @token_required
    def post(self):
        e = add_assigned(mongo, api)
        return e

    @api.marshal_with(assgned)
    @token_required
    def get(self):

        e = get_assigned(mongo)
        return e


@w.route('/assign/room/<ObjectId:id>')
class Deletehostel(Resource):
    @token_required
    def delete(self, id):
        # if current_user.role == 'Accountant' or current_user.role == 'Admin':
        e = delete_assigned(mongo,id)
        return e

    @token_required
    @api.expect(assgned)
    def put(self,id):
        update_assigned(mongo,api,id)


sessionAttendanceModel = {
      "_id": fields.String(readonly=True,),
      "id": fields.String("Assigned id"),
      "student": fields.Raw(""),
      "hostel": fields.Raw(''),
      "room": fields.Raw(''),
      "capacity": fields.Raw(''),
      "created": fields.String("name"),
      "createdBy": fields.String("name"),
      "status": fields.String("status"),
      "exit": fields.String("exit")
    }

sattendance = api.model('hostel_session', sessionAttendanceModel)

hsa = api.namespace('hostel_session')


@hsa.route('/')
class SessionHostel(Resource):
    @api.expect(sattendance)
    @token_required
    def post(self):
        e = add_session_attendance(mongo, api)
        return e

    @api.marshal_with(sattendance)
    @token_required
    def get(self):

        e = get_session_attendance(mongo)
        # print(e)
        return e


@hsa.route('/<ObjectId:id>')
class ModSession(Resource):
    @token_required
    def delete(self, id):
        # if current_user.role == 'Accountant' or current_user.role == 'Admin':
        e = delete_session_attendance(mongo,id)
        return e

    @token_required
    @api.expect(sattendance)
    def put(self, id):
        update_session_attendance(mongo, api, id)


hostelAttendanceModel = {
      "_id": fields.String(readonly=True,),
      "id": fields.String("Assigned id"),
      "student": fields.Raw(""),
      "hostel": fields.Raw(''),
      "room": fields.Raw(''),
      "capacity": fields.Raw(''),
      "created": fields.String("name"),
      "createdBy": fields.String("name"),
      "status": fields.String("status"),
      "exit": fields.String("exit")
    }

attendance = api.model('attendance', hostelAttendanceModel)



@hsa.route('/attendance')
class HostelAttendance(Resource):
    @api.expect(attendance)
    @token_required
    def post(self):
        e = add_attendance(mongo, api)
        return e

    @api.marshal_with(attendance)
    @token_required
    def get(self):

        e = get_attendance(mongo)
        return e


@hsa.route('/attendance/<ObjectId:id>')
class DeletehostelAttendance(Resource):
    @token_required
    def delete(self, id):
        # if current_user.role == 'Accountant' or current_user.role == 'Admin':
        e = delete_attendance(mongo,id)
        return e

    @token_required
    @api.expect(attendance)
    def put(self,id):
        update_attendance(mongo,api,id)




if __name__ == '__main__':
  app.run(host='0.0.0.0',port='5000',debug=True)
