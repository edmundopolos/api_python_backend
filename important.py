# import firebase_admin
# from firebase_admin import credentials, firestore
# from google.cloud import firestore
from flask import Flask, request, send_from_directory, Blueprint, jsonify
from werkzeug.contrib.fixers import ProxyFix
from bson.json_util import dumps,loads
from bson import json_util
import json
from werkzeug.utils import secure_filename
from flask.json import JSONEncoder
from flask_pymongo import PyMongo
from flask_cors import CORS
from werkzeug.datastructures import FileStorage
import datetime
from flask_restplus import Api, Resource, fields
import bson.objectid
# from flask_jwt import JWT, jwt_required, current_identity
from functools import wraps
import os
import uuid
import jwt
import  requests
blueprint = Blueprint('Mschool', __name__)
# api = Api(blueprint) #,doc=False
import json
from base64 import b64decode
from nacl.secret import SecretBox
from bson.objectid import ObjectId


ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','mp4','webm','avi','mkv'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_ext(name):
    return name.rsplit('.', 1)[1].lower()

def my_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    elif isinstance(x, bson.objectid.ObjectId):
        return str(x)
    else:
        raise TypeError(x)



def authenticate(username,password):

    if username and password:
        url = 'http://0.0.0.0:8000/api/user'
        s = requests.session()
        payload = {
            "username": "edmund",
            "password": "edmund123"

        }
        r = s.post(url, headers={"Content-Type": "application/json"}, data=json.dumps(payload))
        res = str(r.status_code)
        print(res)
        if res == '200':
            print(r.json())
            return r.json()





# def identity(payload):
#     user = payload['identity']
#     print(payload)
#     return user


