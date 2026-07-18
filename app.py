"""Flask application exposing the total-and-listing computation over HTTP.

This module is the Flask migration of the original procedural console driver.
The original program computed the sum of a fixed list of numbers and printed,
to standard output, the total followed by each number and a completion line::

    Total: 100
    10
    20
    30
    40
    Application completed

The migration preserves that behavior **exactly**: a single ``GET /`` endpoint
reproduces the original standard-output text byte-for-byte (including the
trailing newline) as a ``text/plain`` response. The pure computation logic is
kept untouched in :mod:`service` and merely consumed here, mirroring the
original separation between computation and I/O -- only the delivery mechanism
changes from ``print`` to an HTTP response.

The application is built with the *application-factory* pattern
(:func:`create_app`), so configuration can be injected and a test client can be
created without any side effects at import time (importing this module neither
starts a server nor binds a socket). Configuration is loaded from
:class:`config.Config` via ``app.config.from_object``.

Every HTTP response additionally carries two contract-safe security headers --
``X-Content-Type-Options: nosniff`` and ``X-Frame-Options: DENY`` -- and the
built-in development server is configured to emit a generic, versionless
``Server`` header so that neither the Werkzeug nor the Python version is
disclosed on either development entry point (``python3 app.py`` and
``flask --app app run``). None of this hardening alters the response body,
status code, or content type, so the byte-for-byte output contract is preserved.
"""

from flask import Flask, Response

from service import calculate_total


def _versionless_server_header(self):
    """Return a generic, versionless HTTP ``Server`` header value.

    Installed as :meth:`werkzeug.serving.WSGIRequestHandler.version_string` by
    :func:`_harden_dev_server_version_disclosure`. Werkzeug's development server
    derives the ``Server`` response header solely from ``version_string()``,
    which by default returns ``"Werkzeug/<ver> Python/<ver>"`` and thereby
    discloses the exact framework and interpreter versions. Returning a fixed,
    versionless identifier removes that disclosure while leaving every other
    behavior -- including the response body, status code, and content type --
    unchanged.

    The ``self`` parameter is required because this function is bound as an
    instance method on the request-handler class.
    """
    return "WSGIServer"


def _harden_dev_server_version_disclosure():
    """Suppress dev-server ``Server``-header version disclosure on all entry points.

    Both development entry points -- ``python3 app.py`` (via ``app.run()``) and
    ``flask --app app run`` -- serve requests through Werkzeug's default
    :class:`~werkzeug.serving.WSGIRequestHandler`. Because ``flask run`` offers
    no hook to inject a custom request handler, the only way to harden *both*
    paths from a single place is to replace the handler's ``version_string``
    method, which is the sole source of the ``Server`` header value. The override
    is idempotent (safe to apply on every :func:`create_app` call) and inert for
    production WSGI servers (gunicorn, waitress, etc.), which supply their own
    ``Server`` header and never use this development handler.

    The ``werkzeug.serving`` import is performed here rather than at module top
    level so that merely importing :mod:`app` remains free of any side effect on
    the ``werkzeug`` package; the override is applied only when an application is
    actually constructed via :func:`create_app`.
    """
    from werkzeug.serving import WSGIRequestHandler

    WSGIRequestHandler.version_string = _versionless_server_header


def create_app():
    """Create and configure the Flask application (application-factory pattern).

    Constructing the application inside a factory keeps import-time side effects
    out of the module and allows tests (and WSGI servers) to build an isolated
    application instance on demand.

    Returns:
        flask.Flask: A fully configured application instance with the single
        ``GET /`` route registered.
    """
    # ``static_folder=None`` disables Flask's default static handling so that no
    # ``/static/<path:filename>`` rule is registered. The migration contract
    # requires exactly one route -- the single ``GET /`` behavior surface -- with
    # no extra endpoints (AAP 0.8.1 "no feature creep"; single-root-route/no-static
    # requirement). The original console program served no files, so the automatic
    # static route would be an unauthorized surface with nothing to serve.
    app = Flask(__name__, static_folder=None)

    # Load configuration (DEBUG, SECRET_KEY) from the dedicated config object.
    # Flask copies only the UPPERCASE attributes of ``config.Config`` into
    # ``app.config``; see config.py for the externalized, environment-driven
    # values. Config is loaded via the string reference so app.py does not need
    # to import the Config class directly.
    app.config.from_object("config.Config")

    # --- Runtime security hardening (contract-safe) ----------------------------
    # The controls below harden the HTTP surface WITHOUT changing the response
    # body, status code, or Content-Type, so the byte-for-byte output contract
    # with the original console program is preserved intact.

    # SEC-F3: suppress dev-server framework/Python version disclosure in the
    # ``Server`` header for BOTH development entry points (``python3 app.py`` and
    # ``flask --app app run``); see _harden_dev_server_version_disclosure. Applied
    # here so the Flask CLI path -- which auto-invokes this factory but never runs
    # the ``__main__`` block -- is hardened identically to the direct-script path.
    _harden_dev_server_version_disclosure()

    @app.after_request
    def _set_security_headers(response):
        """Attach contract-safe security headers to every response.

        Registered on the application so it runs for all responses the app
        produces -- including 404 (not found) and 405 (method not allowed) error
        responses -- ensuring the headers are present across the whole surface.
        Only headers are added; the body, status code, and Content-Type are left
        untouched, so the exact output contract is preserved.
        """
        # SEC-F1: instruct clients not to MIME-sniff the response away from its
        # declared ``text/plain`` content type.
        response.headers["X-Content-Type-Options"] = "nosniff"
        # SEC-F2: forbid embedding any response in a frame/iframe (clickjacking
        # protection). This is an API-only ``text/plain`` endpoint never intended
        # to be framed, so denying all framing is the correct, strictest choice.
        response.headers["X-Frame-Options"] = "DENY"
        return response

    @app.route("/", methods=["GET"])
    def index():
        """Return the original console output verbatim as ``text/plain``.

        Reproduces the source program's standard output byte-for-byte: the
        total line, each number in input order, and the completion line,
        terminated by a single trailing newline (matching the newline that
        :func:`print` appended after the final line).

        The view is stateless, deterministic and side-effect-free: it operates
        only on the fixed input and returns the computed response.

        Returns:
            flask.Response: A ``200 OK`` ``text/plain`` response whose body is
            exactly ``b"Total: 100\\n10\\n20\\n30\\n40\\nApplication completed\\n"``.
        """
        # Fixed, deterministic input -- retained exactly from the original
        # driver so the rendered output is constant across runs. Defined locally
        # to keep the view self-contained and free of shared mutable state.
        numbers = [10, 20, 30, 40]

        # Pure computation delegated to the unchanged service module.
        total = calculate_total(numbers)

        # Reconstruct the original stdout line by line. ``print`` emitted one
        # line per call (each terminated by "\n"); joining the lines with "\n"
        # and appending a single trailing "\n" reproduces those exact bytes:
        #   b"Total: 100\n10\n20\n30\n40\nApplication completed\n"
        lines = [f"Total: {total}"]
        lines.extend(str(number) for number in numbers)  # numbers in input order
        lines.append("Application completed")
        body = "\n".join(lines) + "\n"  # trailing newline matches print()

        # ``text/plain`` preserves the original rendered form; Flask defaults to
        # UTF-8, yielding "Content-Type: text/plain; charset=utf-8". HTTP 200
        # mirrors the original successful process exit code (0).
        return Response(body, status=200, mimetype="text/plain")

    return app


if __name__ == "__main__":
    # Launch the Flask development server through the factory. Debug behavior is
    # governed by configuration (config.Config.DEBUG); no host/port is hardcoded,
    # so Flask's defaults (http://127.0.0.1:5000/) apply.
    #
    # create_app() installs the versionless ``Server``-header hardening (see
    # _harden_dev_server_version_disclosure), so this direct ``python3 app.py``
    # entry point emits a generic ``Server: WSGIServer`` header with no framework
    # or interpreter version disclosure -- identical to the ``flask --app app
    # run`` path. Only the ``Server`` header value changes; the host, port, debug
    # behavior, routing, and response bytes all remain exactly as before, and no
    # per-call request handler needs to be wired here.
    create_app().run()
