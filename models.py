import datetime
from flask_peewee.auth import BaseUser
from peewee import *
from app import db


class User(db.Model, BaseUser):
    username = CharField()
    password = CharField()
    email = CharField()
    join_date = DateTimeField(default=datetime.datetime.now)
    active = BooleanField(default=True)
    admin = BooleanField(default=False)

    def __str__(self):
        return self.username


class Note(db.Model):
    user = ForeignKeyField(User, backref='note')
    content = TextField()
    created_date = DateTimeField(default=datetime.datetime.now)


if __name__ == '__main__':
    User.create_table()
    Note.create_table()
