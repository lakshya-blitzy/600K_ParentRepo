"""Behavior-parity tests for the Flask application (app.py).

These tests use the Flask test client to assert that the single ``GET /``
endpoint reproduces the original console program's standard output
byte-for-byte. They exist to *verify* behavior parity and must never alter
behavior.

The behavioral contract (verified against the original console program) is the
exact byte string::

    b"Total: 100\\n10\\n20\\n30\\n40\\nApplication completed\\n"

including the trailing newline that ``print`` appended after the final line.
"""
from app import create_app

# The exact bytes the original console program wrote to standard output,
# including the trailing newline after "Application completed".
EXPECTED_BODY = b"Total: 100\n10\n20\n30\n40\nApplication completed\n"


def _client():
    """Return a Flask test client backed by a fresh application instance."""
    return create_app().test_client()


def test_index_returns_http_200():
    """GET / responds with HTTP 200, mirroring the original exit code 0."""
    response = _client().get("/")
    assert response.status_code == 200


def test_index_mimetype_is_text_plain():
    """The response is served as text/plain, preserving the rendered form."""
    response = _client().get("/")
    assert response.mimetype == "text/plain"
    # Flask defaults to UTF-8, so the full Content-Type includes the charset.
    assert response.content_type == "text/plain; charset=utf-8"


def test_index_body_matches_original_output_byte_for_byte():
    """GET / body equals the original stdout exactly (including trailing \\n)."""
    response = _client().get("/")
    assert response.data == EXPECTED_BODY


def test_create_app_returns_flask_instance():
    """The factory returns a Flask application and does not run a server."""
    from flask import Flask

    application = create_app()
    assert isinstance(application, Flask)


def test_url_map_registers_only_the_root_route():
    """Exactly one route -- ``GET /`` -- is registered; no static route exists.

    The migration contract mandates a single behavior surface with no feature
    creep (AAP: single-root-route / no-static). Flask registers a
    ``/static/<path:filename>`` rule automatically unless static handling is
    disabled, so this test guards against that regression by asserting that the
    only registered rule is ``/`` and that no ``static`` endpoint is present.
    """
    app = create_app()

    # Collect the registered rules and endpoints from the URL map.
    rules = {rule.rule for rule in app.url_map.iter_rules()}
    endpoints = {rule.endpoint for rule in app.url_map.iter_rules()}

    # Only the root behavior surface must exist -- nothing else (no static route).
    assert rules == {"/"}
    assert "static" not in endpoints
    # No rule may target the static file-serving path pattern.
    assert not any(rule.startswith("/static") for rule in rules)


def test_root_rule_allows_only_get_and_implicit_methods():
    """The ``/`` rule exposes GET plus Flask's implicit HEAD/OPTIONS only.

    A ``methods=["GET"]`` rule automatically gains HEAD and OPTIONS from Flask;
    no other verbs (POST/PUT/DELETE/PATCH) may be registered on the route.
    """
    app = create_app()

    root_rule = next(
        rule for rule in app.url_map.iter_rules() if rule.rule == "/"
    )
    assert root_rule.methods == {"GET", "HEAD", "OPTIONS"}
