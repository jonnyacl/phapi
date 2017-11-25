#!/usr/bin/env python

from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask import jsonify
from flask import request
from flask import Response

import datetime

import config as cnf
from phapienv.models.user import UserSchema
from phapienv.hasher import hash

import MySQLdb

def db():
    return MySQLdb.connect(cnf.db_host, cnf.db_user, cnf.db_pw, cnf.db_name)

def query_db(query, args=(), one=False):
    cur = db().cursor()
    cur.execute(query, args)
    r = [dict((cur.description[i][0], value) \
               for i, value in enumerate(row)) for row in cur.fetchall()]
    cur.connection.close()
    return (r[0] if r else None) if one else r

app = Flask(__name__)
api = Api(app)

def authenticate(req):
    if req is None or req is '':
        return None
    usertoken = query_db("select * from usertoken where jwt = '" + req + "'")
    userid = usertoken[0].get('userId')
    user = query_db("select * from user where userId = '" + str(userid) + "'")
    if len(user) != 1:
        return None
    return user[0]

def build_response(data, code):
    resp = Response(data)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    resp.status_code = code
    return resp

@app.route('/users')
def get_users():
    # schema = UserSchema(many=True)
    user = authenticate(request.headers.get('authorization'))
    if user is None:
        return jsonify("Invalid user")
    r = query_db("select * from user")
    return jsonify(r)

@app.route('/login', methods=['POST', 'OPTIONS'])
def login():
    resp = build_response("", 200)
    req = request.json
    if req is not None:
        resp = build_response("Test", 200)
        users = query_db("select * from user where userName='" + req['username'] + "'")
        if len(users) != 1:
            return build_response("Invalid", 401)
        user = users[0]
        pwHash = hash(req['password'])
        realHash = user['pwHash']
        if pwHash != realHash:
            return build_response("Invalid password", 401)

        # logged in, return user details and jwt
        return resp

    # sends pre request OPTIONS
    return resp


if __name__ == '__main__':
    app.run(port=8082)
