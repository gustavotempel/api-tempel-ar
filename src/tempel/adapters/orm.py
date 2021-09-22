"""
Database Schemas for models.
"""
from sqlalchemy import Table, Column, Integer, String, DateTime, Boolean, MetaData, create_engine, inspect
from sqlalchemy.exc import NoInspectionAvailable
from sqlalchemy.orm import sessionmaker, registry

from tempel.domain import models
from tempel.conf import Settings


mapper_registry = registry()

metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("user_id", Integer(), primary_key=True, autoincrement=True),
    Column("username", String(50), nullable=False, unique=True),
    Column("email", String(50), nullable=False, unique=True),
    Column("password", String(255), nullable=False),
    Column("created_at", DateTime()),
    Column("verified", Boolean, nullable=False),
    Column("is_active", Boolean, nullable=False),
    Column("verify_code", String(50), nullable=False),
    Column("expires_on", Integer(), nullable=False),
)


def start_mappers():
    """Mapping domain entities to database tables."""
    try:
        inspect(models.User)
    except NoInspectionAvailable:
        mapper_registry.map_imperatively(models.User, users)


class SessionFactory:
    """Database session factory.

    Args:
        config: a Pydantic settings object.

    """
    def __init__(self, config: Settings):
        self.database_url = config.database_url
        self.database_args = config.database_args
        self.engine = create_engine(self.database_url, connect_args=self.database_args)
        self.session_factory = sessionmaker(bind=self.engine, autocommit=False, autoflush=False)
        metadata.create_all(self.engine, checkfirst=True)
        start_mappers()

    def __call__(self, **kwargs):
        return self.session_factory(**kwargs)