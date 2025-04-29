#!/bin/sh

DB_HOST=$(echo $DATABASE_URL | sed -E 's/^.*\/\/[^@]*@([^:]+):([0-9]+)\/.*$/\1/')
DB_PORT=$(echo $DATABASE_URL | sed -E 's/^.*\/\/[^@]*@([^:]+):([0-9]+)\/.*$/\2/')

echo "Parsed DB_HOST=$DB_HOST, DB_PORT=$DB_PORT"

MAX_RETRIES=30
RETRY_COUNT=0

while true; do
  echo "Checking connection to $DB_HOST:$DB_PORT..."
  
  python3 -c "
import socket
try:
    sock = socket.create_connection(('${DB_HOST}', ${DB_PORT}), timeout=2)
    sock.close()
except (socket.timeout, socket.error):
    exit(1)
  "
  
  if [ $? -eq 0 ]; then
    echo "Postgres is reachable - starting backend"
    break
  fi
  
  echo "Postgres at $DB_HOST:$DB_PORT not reachable yet - sleeping"
  sleep 2
  RETRY_COUNT=$((RETRY_COUNT + 1))
  
  if [ "$RETRY_COUNT" -ge "$MAX_RETRIES" ]; then
    echo "Failed to connect to Postgres after $MAX_RETRIES retries. Exiting."
    exit 1
  fi
done

echo "Running database migrations..."
python3 -m db.migrate

echo "Starting backend server..."
exec gunicorn -b 0.0.0.0:"${PORT:-5000}" app:app
