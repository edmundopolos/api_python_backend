import MySQLdb
import requests
import MySQLdb.cursors
import json
from time import gmtime, strftime, sleep
import datetime
db = MySQLdb.connect(host="", user="ed", passwd="", db="Mschool",charset='utf8',use_unicode=True,autocommit=True,
                     cursorclass=MySQLdb.cursors.DictCursor)
# mdcur = db.



def get_user(username,password,role):

    query="select u.id as Id,u.name as Name,u.username as username,u.password as password,u.phone_no as PhoneNumber, r.name as Role from users u left join user_roles ur on ur.user_id = u.id left join roles r on r.id = ur.role_id where u.username = '%s' and r.name ='%s'" % (username,role)
    # print(query)
    cur = db.cursor()
    cur.execute(query)
    result = cur.fetchall()
    # print(result)
    da =cur.description
    a = []
    d={}
    for l in result:
        for i in range(len(da)):
         for j in range(len(l)):
             d[da[i][0]] = l[i]
    a.append(d)
    print(d)
    return a

#
# def get_user(username,password):
#
#     query="select u.id as Id,u.name as Name,u.username as username,u.password as password,u.phone_no as PhoneNumber, r.name as Role from users u left join user_roles ur on ur.user_id = u.id left join roles r on r.id = ur.role_id where username = '%s' and  username = '%s'" % (username,password)
#     # print(query)
#     cur = db.cursor()
#     cur.execute(query)
#     result = cur.fetchall()
#     # print(result)
#     da =cur.description
#     d={}
#     a = []
#     for l in result:
#
#
#
#         # print(l)
#         for i in range(len(da)):
#          for j in range(len(l)):
#              d[da[i][0]] = l[i]
#     a.append(d)
#     print(d)
#     return a







def add_post(data):
    try:
        query="insert into post (username,teacher_id,message,groupId,classId,feed,userType,created) values ('%s','%s','%s','%s','%s','%s','%s','%s')"%(data['username'],data['teacher_id'],data['message'],data['group'],data['classId'],data['feed'],data['userType'],data['created'])
        cur = db.cursor()
        result = cur.execute(query)
        if result == 1:
            id="select * from post order by id desc limit 1"
            cur.execute(id)
            nresult = cur.fetchone()
            print(nresult)
            if data['image'] == []:
                nuri =[]
                for l in data['image']:
                    query="insert into postfile (doc,docUri,uri,postId,name,created) values ('%s','%s','%s','%s','%s','%s')"% ('','',l,nresult[0],data['name'],data['created'])
                    cur =db.cursor()
            if data['docUri'] == []:
                duri =[]
                for n in data['image']:

                    query="insert into postfile (doc,docUri,uri,postId,name,created) values ('%s','%s','%s','%s','%s','%s')"% ('',n,'',nresult[0],data['name'],data['created'])
                    cur =db.cursor()
        posts =[]
        nquery="select * from post order by id desc"
        cur.execute(nquery)
        nresult = cur.fetchall()
        for n in nresult:

            nquery = "select * from postfile where postId = %s;" %(n['id'])
            cur.execute(nquery)
            mresult = cur.fetchall()
            n['files'] = mresult
            posts.append(n)
        print(posts)
        return  {'post': posts}
    except db.Error as e:

        return {"error":e}


def get_posts():
    try:
        posts =[]
        nquery="select * from post order by id desc;"
        cur = db.cursor()
        cur.execute(nquery)
        nresult = cur.fetchall()
        for n in nresult:

            nquery = "select * from postfile where postId = %s;" %(n['id'])
            cur.execute(nquery)
            mresult = cur.fetchall()
            n['files'] = mresult
            posts.append(n)
        print(posts)
        return   posts
    except db.Error as e:

        return {"error":e},400


def get_allposts():
    try:
        posts =[]
        nquery="select * from post order by id desc;"
        cur = db.cursor()
        cur.execute(nquery)
        nresult = cur.fetchall()
        for n in nresult:

            nquery = "select * from postfile where postId = %s;" %(n['id'])
            cur.execute(nquery)
            mresult = cur.fetchall()
            n['files'] = mresult
            posts.append(n)
        print(posts)
        return  {'post': posts}
    except db.Error as e:

        return {"error":e}



def delete_post(id):
    try:
        query = "delete from post where id = '%s'"%(id)
        cur = db.cursor()
        cur.execute(query)
        #delete files
        dquery = "delete from postfile where id = '%s'"%(id)
        cur.execute(dquery)
        return True
    except db.Error as e:

        return {"error":e}



def add_assignment(data):
    # try:
        query="insert into assignment (duedate,title,groupId,classId,guide,created) values ('%s','%s','%s','%s','%s','%s')"%(data['DueDate'],data['title'],data['groupId'],data['classId'],data['guide'],data['created'])
        cur = db.cursor()
        result = cur.execute(query)
        print(result)
        if result == 1:
            id="select * from assignment order by id desc limit 1"
            cur.execute(id)
            nresult = cur.fetchone()
            print(nresult)

            if data['attachment'] == []:
                duri =[]
                for n in data['attachment']:

                    query="insert into assignmentfile (name,assignmentId,uri,created) values ('%s','%s','%s','%s')"% (data['name'],nresult[0],n,data['created'])
                    cur =db.cursor()
                    cur.execute(query)
        posts =[]
        nquery="select * from assignment order by id desc"
        cur.execute(nquery)
        nresult = cur.fetchall()
        for n in nresult:

            nquery = "select * from assignmentfile where assignmentId = %s;" %(n['id'])
            cur.execute(nquery)
            mresult = cur.fetchall()
            n['files'] = mresult
            posts.append(n)
        print(posts)
        return  posts
    # except db.Error as e:
    #
    #     return {"error":e}


def get_assignments():
    # try:
        posts =[]
        nquery="select * from assignment order by id desc;"
        cur = db.cursor()
        cur.execute(nquery)
        nresult = cur.fetchall()
        for n in nresult:
            print(n)
            nquery = "select * from assignmentfile where assignmentId = %s;" %(n['id'])
            cur.execute(nquery)
            mresult = cur.fetchall()
            n['file']=mresult
            posts.append(n)
            print(posts)
        return  posts
    # except db.Error as e:
    #
    #     return {"error":e}
def get_assignment(id):
    # try:
        posts =[]
        nquery="select * from assignment where id = %s order by id desc;"%id
        cur = db.cursor()
        cur.execute(nquery)
        nresult = cur.fetchone()
        print(nresult)
        nquery = "select * from assignmentfile where assignmentId = %s;" %(nresult['id'])
        cur.execute(nquery)
        mresult = cur.fetchall()
        nresult['file']=mresult
        print(nresult)
        return  nresult
    # except db.Error as e:
    #
    #     return {"error":e}


def delete_assignment(id):
    try:
        query = "delete from assignment where id = '%s'"%(id)
        cur = db.cursor()
        cur.execute(query)
        #delete files
        dquery = "delete from assignmentfile where id = '%s'"%(id)
        cur.execute(dquery)
        return True
    except db.Error as e:

        return {"error":e}

data =  {
      "message": "message",
      "title": "title",
      "image": ['rt'],
      "screen": "this.props.screen",
      "username": "username",
      "group": "0",
      "classId": "3",
      "doc": "",
      "docUri": "",
      "feed":"feed",
      "userType": "userType",
      "created": "Sun Apr 05 2020 21:16:01 GMT+0100 (West Africa Standard Time)"
    }


class DictCursor(object):
    pass
#student

def get_student(id):
    query= 'select u.name as student, st.id as StudentId from users u left join students st on st.user_id = u.id left join registrations rg on rg.student_id = st.id where u.id = %s;'%(id)
    cur = db.cursor()
    cur.execute(query)
    student = cur.fetchone()
    if student != None:
        print(student)
        cquery = 'select rg.id as Id, rg.student_id as StudentId, rg.class_id as ClassId, rg.section_id as SectionId, rg.status as Status, rg.house as House, ic.name as ClassName, sc.name as Section, e.name as FormTeacher, e.user_id FROM `registrations` rg left join i_classes ic on ic.id = rg.class_id left join sections sc on sc.id = rg.section_id left join employees e on e.id = sc.teacher_id where rg.student_id = %s;'%(student['StudentId'])
        cur.execute(cquery)
        sclass = cur.fetchone()
        # print(sclass)
        squery = "select sb.id as Id,sb.name as Name,sb.code as Code, ic.name as ClassName, ic.id as ClassId, ic.group as Dept, e.name as Teacher from subjects sb left join i_classes ic on ic.id = sb.class_id left join employees e on e.id = sb.teacher_id where sb.class_id = %s;"%(sclass['ClassId'])
        cur.execute(squery)
        subjects = cur.fetchone()
        data = {"student": student,"class":sclass,"subject":subjects}
        print(data)
        return data
    else:
        return {"error":'Not found', "status": 404}





#teacher
def get_teacher(id):
    query = "select sb.id as Id,sb.name as Name,sb.code as Code, e.id as TeacherId,e.name as TeacherName, ic.id as ClassId, ic.name as ClassName, r.name as role,e.designation as Designation, e.phone_no as PhoneNumber from subjects sb left join employees e on e.id = sb.teacher_id left join roles r on r.id = e.role_id left join i_classes ic on ic.id = sb.class_id where e.id = '%s' and e.role_id= 2;"%(id)
    cur = db.cursor()
    cur.execute(query)
    subjects = cur.fetchall()

    ftquery = 'select ic.id as Id,ic.name as ClassName,ic.status as Status,sc.name as SectionName, sc.status as Section, sc.teacher_id,e.name from sections sc left join i_classes ic on ic.id = sc.class_id left join employees e on e.id = sc.teacher_id where sc.teacher_id = %s;'%id
    cur.execute(ftquery)
    formTeacher = cur.fetchone()
    tquery ="select e.name as Name,e.id as Id,r.name as Role from employees e left join roles r on r.id = e.role_id where e.id = %s;"%id
    cur.execute(tquery)
    teacher = cur.fetchone()
    data = {"subject": list(subjects),"teacher":teacher,"classes":formTeacher}
    print(data)
    # print(tquery)

    return data


def add_student_group(data):
    query = "insert into studentGroup (title,classId,studentId,purpose) value ('%s','%s','%s','%s')"%(data['title'],data['classId'],data['studentId'],data['purpose'])
    cur = db.cursor()
    cur.execute(query)
    result = cur.fetchone()
    squery = "select * from studentGroup;"
    cur =db.cursor()
    cur.execute(squery)
    data = cur.fetchall()
    print(data)
    if data != None:
        return list(data),200
    else:
        return False

#classgroup
def add_class_group(data):
    query = "insert into classGroup (max,classId,purpose,created, name, class) value ('%s','%s','%s','%s','%s','%s')"%(data['max'],data['classId'],data['purpose'],data['created'],data['name'],data['class'])
    cur = db.cursor()
    cur.execute(query)
    result = cur.fetchone()
    cquery = "select * from classGroup;"
    cur =db.cursor()
    cur.execute(cquery)
    data = cur.fetchall()

    if data != None:
        return list(data),200
    else:
        return False



def get_student_groups():
    query = "select * from studentGroup;"
    cur =db.cursor()
    cur.execute(query)
    data = cur.fetchall()
    return list(data)


def delete_student_group(id):
    query = "delete from studentGroup where id = %s;"%id
    cur =db.cursor()
    cur.execute(query)
    group =cur.fetchone
    if group:
        return True
    else:
        return False


def get_class_groups():
    query = "select * from classGroup;"
    cur =db.cursor()
    cur.execute(query)
    data = cur.fetchall()
    return list(data)


def delete_class_group(id):
    query = "delete from classGroup where id = %s;"%id
    cur =db.cursor()
    cur.execute(query)
    group =cur.fetchone
    if group:
        return True
    else:
        return False



def add_folder(data):
    query="insert into folder (name,class,groups) values ('%s','%s','%s')"%(data['name'],data['class'],data['groups'])
    cur = db.cursor()
    cur.execute(query)
    result = cur.fetchone()
    fquery = "select * from folder;"
    cur =db.cursor()
    cur.execute(fquery)
    data = cur.fetchall()

    if data !=None:
        return list(data)
    else:
        return  False


def add_file(data):
    query="insert into files (name,class,groups,uri,size,folder) values ('%s','%s','%s','%s','%s','%s')"%(data['name'],data['class'],data['groups'],data['uri'],data['size'],data['folder'])
    cur = db.cursor()
    cur.execute(query)
    result = cur.fetchone()
    fiquery = "select * from folder;"
    cur =db.cursor()
    cur.execute(fiquery)
    data = cur.fetchall()
    print(data)

    if result ==None:
        return list(data)
    else:
        return  False


def get_folder():
    query = "select * from folder;"
    cur =db.cursor()
    cur.execute(query)
    data = cur.fetchall()
    print(data)
    return list(data)

def delete_folder(id):
    query = "delete from folder where id = %s;"%id
    cur =db.cursor()
    cur.execute(query)
    group =cur.fetchone
    if group:
        return True
    else:
        return False

def get_file():
    query = "select * from files;"
    cur =db.cursor()
    cur.execute(query)
    data = cur.fetchall()
    return data


def delete_file(id):
    query = "delete from files where id = %s;"%id
    cur =db.cursor()
    cur.execute(query)
    group =cur.fetchone
    if group:
        return True
    else:
        return False


def add_quiz(data):
    # try:
        query="insert into quiz (duedate,title,groupId,classId,guide,created) values ('%s','%s','%s','%s','%s','%s')"%(data['DueDate'],data['title'],data['groupId'],data['classId'],data['guide'],data['created'])
        cur = db.cursor()
        result = cur.execute(query)
        print(result)
        if result == 1:
            id="select * from quiz order by id desc limit 1"
            cur.execute(id)
            nresult = cur.fetchone()
            print(nresult)

            if data['attachment'] == []:
                duri =[]
                for n in data['attachment']:

                    query="insert into quizfile (name,quizId,uri,created) values ('%s','%s','%s','%s')"% (data['name'],nresult[0],n,data['created'])
                    cur =db.cursor()
                    cur.execute(query)
        posts =[]
        nquery="select * from quiz order by id desc"
        cur.execute(nquery)
        nresult = cur.fetchall()
        for n in nresult:

            nquery = "select * from quizfile where quizId = %s;" %(n['id'])
            cur.execute(nquery)
            mresult = cur.fetchall()
            n['files'] = mresult
            posts.append(n)
        print(posts)
        return  posts
    # except db.Error as e:
    #
    #     return {"error":e}


def get_allquiz():
    # try:
        posts =[]
        nquery="select * from quiz order by id desc;"
        cur = db.cursor()
        cur.execute(nquery)
        nresult = cur.fetchall()
        for n in nresult:
            print(n)
            nquery = "select * from quizfile where quizId = %s;" %(n['id'])
            cur.execute(nquery)
            mresult = cur.fetchall()
            n['file']=mresult
            posts.append(n)
        print(posts)
        return  posts
    # except db.Error as e:
    #
    #     return {"error":e}

def get_quiz(id):
    try:
        posts =[]
        nquery="select * from quiz order by id desc where id = %s;"%id
        cur = db.cursor()
        cur.execute(nquery)
        nresult = cur.fetchall()
        for n in nresult:
            print(n)
            nquery = "select * from quizfile where postId = %s;" %(n['id'])
            cur.execute(nquery)
            mresult = cur.fetchall()
            n['file']=mresult
            posts.append(n)
        print(posts)
        return  posts
    except db.Error as e:

        return {"error":e}


def delete_quiz(id):
    try:
        query = "delete from quiz where id = '%s'"%(id)
        cur = db.cursor()
        cur.execute(query)
        #delete files
        dquery = "delete from quizfile where id = '%s'"%(id)
        cur.execute(dquery)
        return True
    except db.Error as e:

        return {"error":e}



def add_message(data):
    query="insert into messages (message,recepient,sender,token,read,createdAt) values('%s','%s','%s','%s','%s','%s')"%(data['message'],data['recepient'],data['sender'],data['token'],data['read'],data['createdAt'])
    cur = db.cursor()
    cur.execute(query)


def get_messages():
    query="select * from messages where recipent;"
    cur=db.cursor()
    cur.execute(query)
    data = cur.fetchall()

    return  data


# get_teacher(8)
# add_post(data)
# get_student(8)
