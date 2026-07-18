# Total & Listing Service (Flask)

A minimal Python 3 [Flask](https://flask.palletsprojects.com/) application that
exposes, over HTTP, the total-and-listing computation that was originally printed
to standard output by a small console script. A single endpoint computes the sum
of a fixed list of numbers and returns the total followed by each number, exactly
reproducing the original program's output. The app is built with the
**application-factory** pattern (`create_app()`), keeps the pure computation logic
in a separate module (`service.py`), and ships with a WSGI entry point for
deployment.

## Requirements

- **Python 3.9+** (developed and verified on Python 3.12)
- **Flask 3.1.3** (see [`requirements.txt`](requirements.txt))

## Installation

Create and activate a virtual environment, then install the dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running (development)

The application exposes an application factory, `create_app()`, in
[`app.py`](app.py). You can start the built-in Flask development server in either
of two ways.

**Option A — factory via the Flask CLI:**

```bash
flask --app app run
```

**Option B — run the script directly:**

```bash
python3 app.py
```

Either option starts the development server at:

```
http://127.0.0.1:5000/
```

> The development server is intended for local use only. For production, use a
> WSGI server (see below).

## Running (production / WSGI)

[`wsgi.py`](wsgi.py) exposes a ready-to-serve application object,
`app = create_app()`, for any WSGI server. For example, using
[gunicorn](https://gunicorn.org/):

```bash
gunicorn wsgi:app
```

Other WSGI servers such as [waitress](https://docs.pylonsproject.org/projects/waitress/)
work equally well (e.g. `waitress-serve --call wsgi:create_app`). These servers are
mentioned only as examples and are **not** included in `requirements.txt`; install
your chosen server separately.

## Configuration

[`config.py`](config.py) provides a `Config` class that the application factory
loads via:

```python
app.config.from_object("config.Config")
```

`Config` reads its values from the environment:

- `FLASK_DEBUG` — enables Flask's debug mode. Set it to one of `1`, `true`,
  `yes`, or `on` (case-insensitive; surrounding whitespace is ignored) to turn
  debug mode on. When the variable is unset, empty, or set to any other value,
  debug mode stays **off** (the default).
- `SECRET_KEY` — the secret key Flask uses to sign the session cookie and other
  security-sensitive tokens. When it is unset, the configuration falls back to
  the non-secret placeholder `"dev"`, which is intended for **local development
  only**. In production you **must** set `SECRET_KEY` to a strong, unpredictable
  (randomly generated) value.

## Endpoint

| Method | Path | Status | Content-Type |
| ------ | ---- | ------ | ------------ |
| `GET`  | `/`  | `200 OK` | `text/plain; charset=utf-8` |

`GET /` computes `calculate_total([10, 20, 30, 40])` and returns the result as
plain text, byte-for-byte identical to the original console output. The response
body is:

```
Total: 100
10
20
30
40
Application completed
```

Notes on the response:

- The body ends with a trailing newline — the exact bytes are
  `Total: 100\n10\n20\n30\n40\nApplication completed\n`.
- The input list is fixed at `[10, 20, 30, 40]`, so the output is deterministic.
- The numbers are listed in input order.

## Testing

Parity tests live in the [`tests/`](tests) directory:

- `tests/test_service.py` — verifies the computation functions in `service.py`
  (`calculate_total` and `calculate_average`).
- `tests/test_app.py` — uses the Flask test client to assert that `GET /` returns
  the exact response body shown above.

Install [pytest](https://docs.pytest.org/) and run the suite from the project root:

```bash
pip install pytest
pytest
```
