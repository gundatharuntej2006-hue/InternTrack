from django.apps import AppConfig


class CoreConfig(AppConfig):
    """Project-wide infrastructure (health checks, shared utilities)."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.core"
    label = "core"
