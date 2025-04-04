from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from app.database.postgres.models import *
from app.database.postgres.models.base import Base
from app.database.postgres.sessions import DB_URI

# Set up the Alembic Config object
config = context.config
fileConfig(config.config_file_name)

# Define the target metadata
target_metadata = Base.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=DB_URI,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = DB_URI
    connectable = engine_from_config(
        configuration, prefix="sqlalchemy.", poolclass=pool.NullPool
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

# Determine the mode and run migrations accordingly
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()