"""Application configuration for the Flask migration.

This module defines the configuration object consumed by the Flask
application factory (``create_app`` in :mod:`app`) through the call
``app.config.from_object("config.Config")``.

Flask's ``Config.from_object`` copies only the **UPPERCASE** attributes of the
referenced object into the application configuration. Every setting exposed
here is therefore declared in uppercase on :class:`Config`. Values are sourced
from environment variables (12-factor style) with safe local-development
defaults, so no environment-specific value is hard-coded into the deployment.

The configuration is intentionally minimal: it externalizes only the two
settings the application actually needs (``DEBUG`` and ``SECRET_KEY``) and
introduces no additional infrastructure (no database, cache, or similar),
consistent with the behavior-preserving migration mandate.

Importing this module has no side effects: it performs only pure attribute
declarations and read-only ``os.environ`` lookups (no I/O, network, or
printing).
"""

import os


class Config:
    """Base Flask configuration loaded via ``app.config.from_object``.

    Only attributes whose names are fully uppercase are read by Flask when the
    object is loaded, so the public configuration surface is exactly the
    uppercase class attributes declared below.
    """

    #: Enable Flask's debug mode. Disabled by default; set the ``FLASK_DEBUG``
    #: environment variable to one of ``1`` / ``true`` / ``yes`` / ``on`` (any
    #: case, surrounding whitespace ignored) to turn it on. Any other value, or
    #: an unset variable, leaves debug mode off. The expression evaluates to a
    #: genuine ``bool``.
    DEBUG = os.environ.get("FLASK_DEBUG", "").strip().lower() in (
        "1",
        "true",
        "yes",
        "on",
    )

    #: Secret key used by Flask to sign the session cookie and other
    #: security-sensitive tokens. Sourced from the ``SECRET_KEY`` environment
    #: variable; the ``"dev"`` fallback is a non-secret placeholder intended
    #: only for local development and MUST be overridden in production by
    #: setting ``SECRET_KEY`` in the environment.
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev")
