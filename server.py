#!/usr/bin/env python

from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask import jsonify

import datetime

import config as cnf
from phapienv.models.user import UserSchema

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


@app.route('/users')
def get_users():
    # schema = UserSchema(many=True)
    r = query_db("select * from user")

    return jsonify(r)


if __name__ == '__main__':
    app.run(port=8082)
