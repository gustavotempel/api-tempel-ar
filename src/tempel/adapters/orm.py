"""
Database Schemas for models.
"""
import os

from sqlalchemy import Table, Column, Integer, String, DateTime, Boolean, MetaData, create_engine, inspect
from sqlalchemy.exc import NoInspectionAvailable
from sqlalchemy.orm import sessionmaker, registry

from tempel.domain import models

DATABASE_URL = os.environ["DATABASE_URL"]

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
    Column("verify_code", String(50), nullable=False),
    Column("verified", Boolean, nullable=False),
    Column("is_active", Boolean, nullable=False),
)


def start_mappers():
    """Mapping domain entities to database tables."""
    try:
        inspect(models.User)
    except NoInspectionAvailable:
        user_mapper = mapper_registry.map_imperatively(models.User, users)


def create_session():
    engine = create_engine(DATABASE_URL)
    session_factory = sessionmaker(bind=engine)
    metadata.create_all(engine)
    start_mappers()