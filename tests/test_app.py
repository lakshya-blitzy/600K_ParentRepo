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
