"""Map legacy apps.console.api.v1 imports to current API modules."""

import os


_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
_APPS_DIR = os.path.abspath(os.path.join(_CURRENT_DIR, "..", "..", ".."))

__path__ = [
    os.path.join(_APPS_DIR, "api", "v1"),
    _APPS_DIR,
]