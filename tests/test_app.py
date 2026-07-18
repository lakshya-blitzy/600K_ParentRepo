"""Golden-output test for the Flask GET "/" endpoint.

Asserts the HTTP response reproduces the original console stdout byte-for-byte.
"""
from app import create_app


def test_index_returns_exact_original_output():
    client = create_app().test_client()
    response = client.get("/")

    assert response.status_code == 200
    assert response.mimetype == "text/plain"
    assert response.data == b"Total: 100\n10\n20\n30\n40\nApplication completed\n"
