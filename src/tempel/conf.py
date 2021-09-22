"""This module contains the application configuration object."""

from typing import Dict, Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    """The application-specific configuration object."""

    database_url: Optional[str]
    database_args: Optional[Dict] = dict()
    unit_of_work_factory: Optional[str]