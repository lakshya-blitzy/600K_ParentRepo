"""Flask web application entry point for the parent repository.

Migrated from a standard-library console program to a Flask WSGI web
application. The application serves, over HTTP, the exact content the original
``main()`` routine wrote to stdout: the computed total, each of the fixed input
numbers, and a completion line. Only the I/O channel changes
(stdout -> HTTP response body); the input, computation, and output ordering are
preserved verbatim.
"""

from flask import Flask
from service import calculate_total


def create_app():
    """Application factory: build and return the configured Flask app.

    Using a factory avoids import-time global side effects and keeps the
    application testable (for example, via ``app.test_client()``).
    """
    app = Flask(__name__)

    @app.route("/")
    def index():
        """Reproduce the original ``main()`` workflow as an HTTP response.

        Builds the response body line-for-line so the served content equals the
        former stdout output exactly, then returns it as plain text.
        """
        # Fixed, deterministic input (unchanged from the original program).
        numbers = [10, 20, 30, 40]

        # Business logic preserved in the service layer (running-sum total).
        total = calculate_total(numbers)

        # Assemble the response body in the exact order the console printed it:
        # "Total: {total}", then each number, then the completion line.
        lines = [f"Total: {total}"]
        lines += [str(number) for number in numbers]
        lines.append("Application completed")
        body = "\n".join(lines)

        # Return plain text so the raw lines appear verbatim (no HTML wrapper).
        return body, 200, {"Content-Type": "text/plain; charset=utf-8"}

    return app


# Module-level WSGI application instance so that ``flask run`` and external WSGI
# servers can discover ``app`` while ``python app.py`` still works below.
app = create_app()


if __name__ == "__main__":
    # Retain the direct-run affordance: launch the Flask development server.
    app.run()
