"""Health-check helpers."""

import logging

from django.db import DatabaseError, connections

logger = logging.getLogger(__name__)


def database_is_available(alias: str = "default") -> bool:
    """Return True if a real round-trip query to the database succeeds."""
    try:
        with connections[alias].cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
    except DatabaseError:
        logger.exception("Health check: database '%s' is unavailable", alias)
        return False
    return True
