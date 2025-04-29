import os
import importlib
import pathlib

def run_migrations():
    migrations_path = pathlib.Path(__file__).parent / "migrations"
    migration_files = sorted([
        f.stem for f in migrations_path.glob("*.py")
        if f.name != "__init__.py"
    ])

    print(f"Found migrations: {migration_files}")

    for migration_name in migration_files:
        print(f"Running migration: {migration_name}")
        module = importlib.import_module(f"db.migrations.{migration_name}")
        if hasattr(module, "migrate"):
            module.migrate()
        else:
            print(f"Warning: {migration_name} has no migrate() function, skipping.")

if __name__ == "__main__":
    run_migrations()
