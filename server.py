#!/usr/bin/env python

from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask import jsonify

import config as cnf

import MySQLdb

db = MySQLdb.connect(cnf.db_host, cnf.db_user, cnf.db_pw, cnf.db_name)
cursor = db.cursor()
app = Flask(__name__)
api = Api(app)

class UserTokens(Resource):
    def get(self):
        query = cursor.execute("select * from usertoken")
        return {'tokens': [i[1] for i in cursor.fetchall()]}

api.add_resource(UserTokens, '/tokens')

if __name__ == '__main__':
    app.run(port=8082)


