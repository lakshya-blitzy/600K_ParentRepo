"""Production WSGI entry point for the Flask application.

This module exposes a ready-to-serve WSGI application object named ``app`` that
production WSGI servers import and serve. It builds the application once via the
application factory defined in :mod:`app`.

Examples:
    Serve with gunicorn (the ``wsgi:app`` object)::

        gunicorn wsgi:app

    Serve with waitress (calling the factory ``wsgi:create_app``)::

        waitress-serve --call wsgi:create_app

    Run the development server directly::

        python3 wsgi.py
"""

from app import create_app

# The WSGI application object. WSGI servers look up this module-level ``app``
# (e.g. ``gunicorn wsgi:app``). ``create_app`` is also re-exported by virtue of
# the import above, so ``waitress-serve --call wsgi:create_app`` works too.
app = create_app()


if __name__ == "__main__":
    # Convenience for local development: ``python3 wsgi.py`` starts Flask's
    # built-in development server. Host/port default to Flask's values
    # (http://127.0.0.1:5000/); debug behavior is governed by config.Config.
    app.run()
