from flask_peewee.rest import RestAPI, UserAuthentication, RestrictOwnerResource
from flask import g
from app import app
from auth import auth
from models import Note, User

user_auth = UserAuthentication(auth, protected_methods=['POST', 'PUT', 'DELETE', 'GET'])

api = RestAPI(app, default_auth=user_auth)


class UserResource(RestrictOwnerResource):
    exclude = ('password', 'email',)

    def get_query(self):
        return User.select().where(User.id == g.user.id)


class NoteResource(RestrictOwnerResource):
    owner_field = 'user'

    def get_query(self):
        return Note.select().where(Note.user == g.user)


api.register(User, UserResource)
api.register(Note, NoteResource)
