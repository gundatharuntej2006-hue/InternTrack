from unittest import mock

from django.db import OperationalError, connections
from django.test import SimpleTestCase, TestCase
from django.urls import reverse


class HealthEndpointTests(TestCase):
    """Runs against the real PostgreSQL test database."""

    def test_health_ok_when_database_reachable(self):
        response = self.client.get(reverse("core:health"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok", "database": "ok"})

    def test_health_url_is_slash_health(self):
        self.assertEqual(reverse("core:health"), "/health/")

    def test_health_is_not_cacheable(self):
        response = self.client.get(reverse("core:health"))

        self.assertIn("no-cache", response["Cache-Control"])

    def test_health_rejects_post(self):
        response = self.client.post(reverse("core:health"))

        self.assertEqual(response.status_code, 405)

    def test_database_backend_is_postgresql(self):
        self.assertEqual(connections["default"].vendor, "postgresql")


class HealthEndpointDatabaseDownTests(SimpleTestCase):
    """Simulates an unreachable database (no real DB access needed)."""

    def test_health_returns_503_when_database_unavailable(self):
        with mock.patch.object(
            connections["default"],
            "cursor",
            side_effect=OperationalError("connection refused"),
        ), self.assertLogs("apps.core.health", level="ERROR"):
            response = self.client.get(reverse("core:health"))

        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json(), {"status": "error", "database": "unavailable"})

    def test_error_details_are_not_leaked(self):
        with mock.patch.object(
            connections["default"],
            "cursor",
            side_effect=OperationalError("password authentication failed for user x"),
        ), self.assertLogs("apps.core.health", level="ERROR"):
            response = self.client.get(reverse("core:health"))

        self.assertNotIn("password", response.content.decode())
