"""Create the reichlab CLI."""

import structlog
import typer

from reichlab.greeting import app as greeting_app
from reichlab.repo import app as repo_app

logger = structlog.get_logger()

app = typer.Typer(no_args_is_help=True, pretty_exceptions_short=False)

app.add_typer(greeting_app)
app.add_typer(repo_app, name="repo")
