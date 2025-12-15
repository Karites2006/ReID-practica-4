from marshmallow import Schema, fields

class MessageSchema(Schema):
    sentence = fields.String(required=True)

class UserSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)
