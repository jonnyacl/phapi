#!/usr/bin/env python

from flask import Flask, request
from flask_restful import Resource, Api
from flask import jsonify
from flask import request
import datetime

from phapienv.hasher import hash
from phapienv.db_talker import query_db, insert_item, remove_item, exec_sql

import phapienv.tokens as tokens
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
    resp = app.response_class(response=data, status=code, mimetype='application/json')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return resp

@app.route('/users')
def get_users():
    # schema = UserSchema(many=True)
    user = authenticate(request.headers.get('authorization'))
    if user is None:
        return jsonify("Invalid user")
    r = query_db("select * from user")
    return jsonify(r)

@app.route('/register', methods=['POST', 'OPTIONS'])
def register():
    resp = build_response("", 200)
    req = request.json
    if req is not None:
        pwHash = hash(req['password'])
        uName = req['username']
        fName = req['firstName']
        lName = req['lastName']
        email = req['email']
        users = query_db("select * from user where userName='" + uName + "'")
        if len(users) != 0:
            return build_response("User already exists", 401)
        now = datetime.datetime.utcnow()
        insert_item('user', userName=uName, firstName=fName, lastName=lName, email=email, pwHash=pwHash, created=now, lastLogon=now)
        users = query_db("select * from user where userName='" + uName + "'")
        if len(users) != 1:
            return build_response("User not created correctly", 404)
        user = users[0]
        token = {
            'jwt' : tokens.make_token(user, 'w')
        }

        # logged in, return jwt containing user details
        return build_response(jsonify(token).data, 200)

    # sends pre request OPTIONS
    return resp

@app.route('/login', methods=['POST', 'OPTIONS'])
def login():
    resp = build_response("", 200)
    req = request.json
    if req is not None:
        users = query_db("select * from user where userName='" + req['username'] + "'")
        if len(users) != 1:
            return build_response("Invalid", 401)
        user = users[0]
        pwHash = hash(req['password'])
        realHash = user['pwHash']
        if pwHash != realHash:
            return build_response("Invalid password", 401)

        token = {
            'jwt' : tokens.make_token(user, 'w')
        }

        #update lastlogon
        now = datetime.datetime.utcnow()
        exec_sql("UPDATE user SET lastLogon=" + "'" + str(now) +"'")

        # logged in, return jwt containing user details
        return build_response(jsonify(token).data, 200)

    # sends pre request OPTIONS
    return resp

@app.route('/logout', methods=['POST', 'OPTIONS'])
def logout():
    resp = build_response("", 200)
    req = request.json
    if req is not None:
        u = authenticate(req)
        uId = u['userId']
        remove_item("usertoken", userId=uId)

    # sends pre request OPTIONS
    return resp


if __name__ == '__main__':
    app.run(port=8082)
