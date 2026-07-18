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
"""

from flask import Flask, Response

from service import calculate_total


def create_app():
    """Create and configure the Flask application (application-factory pattern).

    Constructing the application inside a factory keeps import-time side effects
    out of the module and allows tests (and WSGI servers) to build an isolated
    application instance on demand.

    Returns:
        flask.Flask: A fully configured application instance with the single
        ``GET /`` route registered.
    """
    app = Flask(__name__)

    # Load configuration (DEBUG, SECRET_KEY) from the dedicated config object.
    # Flask copies only the UPPERCASE attributes of ``config.Config`` into
    # ``app.config``; see config.py for the externalized, environment-driven
    # values. Config is loaded via the string reference so app.py does not need
    # to import the Config class directly.
    app.config.from_object("config.Config")

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
    create_app().run()
