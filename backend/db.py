import os
from peewee import PostgresqlDatabase, Model, AutoField, CharField
from urllib.parse import urlparse

# Local docker for dev, Railway hosted for prod
DATABASE_URL = os.environ.get('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set.")

url = urlparse(DATABASE_URL)

# Determine if we should require SSL
use_ssl = os.getenv("ENVIRONMENT", "development") != "development"

# Database connection params
db_params = {
    'database': url.path[1:],  # remove leading /
    'user': url.username,
    'password': url.password,
    'host': url.hostname,
    'port': url.port,
}

# Only add SSL options in production
if use_ssl:
    db_params['sslmode'] = 'require'

db = PostgresqlDatabase(**db_params)


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