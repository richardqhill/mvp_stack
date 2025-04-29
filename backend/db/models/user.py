from peewee import CharField
from playhouse.postgres_ext import JSONField
from db import db
from peewee import Model

class User(Model):
    name = CharField()
    avatar = CharField(null=True)
    preferences = JSONField(default=dict)

    class Meta:
        database = db
        table_name = "user"  # Important since "user" is a reserved word in SQL
