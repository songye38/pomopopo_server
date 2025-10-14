# alembic/env.py
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.db.database import Base  # 네 Base 위치
from app.db.models import models  # 모델 import (자동 인식 위해)

# Alembic Config
config = context.config
fileConfig(config.config_file_name)
target_metadata = Base.metadata  # 중요

def run_migrations_offline():
    url = os.getenv("DATABASE_PUBLIC_URL")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        url=os.getenv("DATABASE_PUBLIC_URL")  # Railway DB URL
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
