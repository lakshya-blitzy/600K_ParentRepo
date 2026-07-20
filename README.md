# 600K_ParentRepo

A minimal Flask web application that serves, over HTTP, the same output the original console program printed to stdout.

This is the parent repository of the project. It runs standalone: the computation is fully deterministic, operating on the fixed, hard-coded input `[10, 20, 30, 40]`, and takes no configuration, environment variables, or request parameters.

## Requirements

- **Python 3.9+** (this project targets Python 3.12)
- **Flask 3.1.3** — installed via the dependency manifest (`requirements.txt`)

## Installation

Create and activate a virtual environment, then install the pinned dependency:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

> **Clean-environment note.** On some hosts `python -m venv .venv` fails while
> bootstrapping pip (an `ensurepip`/pip error). If that happens, create the
> environment without pip, bootstrap the tooling explicitly, and then install
> the dependency:
>
> ```bash
> python -m venv .venv --without-pip
> python -m pip --python .venv/bin/python install pip setuptools wheel
> .venv/bin/python -m pip install -r requirements.txt
> ```

## Running

Start the development server in either of the two supported ways:

```bash
python app.py
# or
flask run
```

Both commands launch Flask's built-in development server, which listens on `http://127.0.0.1:5000/` by default.

## Usage

The application exposes a single endpoint:

| Method | Path | Response |
|--------|------|----------------------------------------------------------|
| `GET`  | `/`  | `text/plain` body reproducing the original program output |

`GET /` returns the following plain-text body, line for line:

```text
Total: 100
10
20
30
40
Application completed
```

For example, with the server running:

```bash
curl http://127.0.0.1:5000/
```

yields exactly the six lines shown above.
