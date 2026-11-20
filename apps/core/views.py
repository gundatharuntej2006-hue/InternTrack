from django.http import JsonResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_GET

from .health import database_is_available


@never_cache
@require_GET
def health(request):
    """
    Liveness + database readiness check.

    200 {"status": "ok", "database": "ok"}             -> Django and PostgreSQL are up
    503 {"status": "error", "database": "unavailable"} -> PostgreSQL unreachable

    Error details are logged server-side, never returned to the client.
    """
    if database_is_available():
        return JsonResponse({"status": "ok", "database": "ok"})
    return JsonResponse({"status": "error", "database": "unavailable"}, status=503)
