import datetime as dt

from marshmallow import Schema, fields

class User(object):
    def __init__(self, userId, userName, firstName, lastName, email, pwHash, created, lastLogon):
        self.userId = userId
        self.userName = userName
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.pwHash = pwHash
        self.created = created
        self.lastLogon = lastLogon

    def __repr__(self):
        return '<User(name={self.userName!r})>'.format(self)

class UserSchema(Schema):
    userId = fields.Integer()
    userName = fields.Str()
    firstName = fields.Str()
    lastName = fields.Str()
    email = fields.Str()
    pwHash = fields.Str()
    created = fields.Date()
    lastLogon = fields.Date()