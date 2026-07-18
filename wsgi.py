"""Production WSGI entry point for the Flask application.

This module exposes a ready-to-serve WSGI application object named ``app`` for
production WSGI servers (gunicorn, uWSGI, waitress, etc.). The application is
built exactly once, at import time, by delegating to the application factory
:func:`app.create_app`; this entry point adds no routing, configuration, or
behavior of its own -- routing lives in the factory in :mod:`app` and
configuration in :mod:`config`.

Typical production usage::

    gunicorn wsgi:app
    waitress-serve --call wsgi:create_app

Importing this module has no side effects beyond constructing the application
instance: it neither starts a server nor binds a socket. The development server
is deliberately not launched here -- that convenience lives behind the
``__main__`` guard in :mod:`app` (``python3 app.py``).
"""

from app import create_app

# Module-level WSGI application callable. Production servers reference it as
# ``wsgi:app`` (e.g. ``gunicorn wsgi:app``). Because ``create_app`` is imported
# into this module's namespace above, it is also reachable as
# ``wsgi:create_app`` for servers that prefer to call the factory directly
# (e.g. ``waitress-serve --call wsgi:create_app``).
app = create_app()
