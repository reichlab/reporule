"""reporule initialization."""

import os
from importlib.util import find_spec
from pathlib import Path

TOKEN = os.environ.get("GITHUB_TOKEN", "")

if find_spec("reporule") is not None:
    REPORULE_PATH = Path(find_spec("reporule").origin).parent  # type: ignore
else:
    REPORULE_PATH = Path(__file__).parent.parent
