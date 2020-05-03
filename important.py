# import firebase_admin
# from firebase_admin import credentials, firestore
# from google.cloud import firestore
from flask import Flask, session, send_from_directory, Blueprint, jsonify
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
import os
import uuid
blueprint = Blueprint('Mschool', __name__)
api = Api(blueprint) #,doc=False


upload_parser = api.parser()
upload_parser.add_argument('file', location='files',
                           type=FileStorage)
upload_parser.add_argument('message', location='form')
# upload_parser.add_argument('teacher_id', location='form')
upload_parser.add_argument('doc', location='files',
                           type=FileStorage)



ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


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






