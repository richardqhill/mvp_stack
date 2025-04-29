from db import db

def migrate():
    print("Connecting to database...")
    db.connect()

    print("Creating 'user' table...")
    db.execute_sql("""
    CREATE TABLE IF NOT EXISTS "user" (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        avatar VARCHAR(512),
        preferences JSONB DEFAULT '{}'::jsonb
    );
    """)

    print("Seeding default user with ID 1 (if not exists)...")
    db.execute_sql("""
    INSERT INTO "user" (id, name, avatar, preferences)
    SELECT 1, 'Test User 1', 'https://example.com/avatar.png', '{}'::jsonb
    WHERE NOT EXISTS (
        SELECT 1 FROM "user" WHERE id = 1
    );
    """)

    print("Seeding default user with ID 2 (if not exists)...")
    db.execute_sql("""
    INSERT INTO "user" (id, name, avatar, preferences)
    SELECT 2, 'Test User 2', 'https://example.com/avatar.png', '{}'::jsonb
    WHERE NOT EXISTS (
        SELECT 2 FROM "user" WHERE id = 2
    );
    """)

    print("Migration complete.")
    db.close()
