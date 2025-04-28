#!/bin/sh

DB_HOST=$(echo $DATABASE_URL | sed -E 's/^.*\/\/[^@]*@([^:]+):([0-9]+)\/.*$/\1/')
DB_PORT=$(echo $DATABASE_URL | sed -E 's/^.*\/\/[^@]*@([^:]+):([0-9]+)\/.*$/\2/')

echo "Waiting for Postgres at $DB_HOST:$DB_PORT..."

MAX_RETRIES=30
RETRY_COUNT=0

while ! python3 -c "import socket; sock = socket.socket(); result = sock.connect_ex(('${DB_HOST}', int(${DB_PORT}))); exit(result);" ; do
  echo "Postgres at $DB_HOST:$DB_PORT is unavailable - sleeping"
  sleep 1
  RETRY_COUNT=$((RETRY_COUNT + 1))
  if [ "$RETRY_COUNT" -ge "$MAX_RETRIES" ]; then
    echo "Postgres did not become available after $MAX_RETRIES seconds. Exiting."
    exit 1
  fi
done

echo "Postgres is up after $RETRY_COUNT retries - starting backend"

exec gunicorn -b 0.0.0.0:"${PORT:-5000}" app:app