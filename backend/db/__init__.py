import os
from peewee import PostgresqlDatabase
import urllib.parse as urlparse

db_url = urlparse.urlparse(os.getenv('DATABASE_URL'))

db_params = {
    'database': db_url.path[1:],  # remove leading slash
    'user': db_url.username,
    'password': db_url.password,
    'host': db_url.hostname,
    'port': db_url.port,
}

if os.getenv("ENVIRONMENT", "development") != "development":
    db_params['sslmode'] = 'require'

db = PostgresqlDatabase(**db_params)