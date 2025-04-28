import os
from peewee import PostgresqlDatabase, Model, AutoField, CharField
from urllib.parse import urlparse

# Local docker for dev, Railway hosted for prod
DATABASE_URL = os.environ.get('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set.")

parsed = urlparse(DATABASE_URL)
db = PostgresqlDatabase(
    parsed.path.lstrip('/'),
    user=parsed.username,
    password=parsed.password,
    host=parsed.hostname,
    port=parsed.port or 5432
)


class BaseModel(Model):
    class Meta:
        database = db

class Test(BaseModel):
    id = AutoField()
    name = CharField()


def initialize_db():
    """Create tables and seed initial data if needed."""
    db.connect(reuse_if_open=True)
    db.create_tables([Test])

    if Test.select().count() == 0:
        Test.create(name='Hello World')