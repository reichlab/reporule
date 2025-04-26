"""Create the reporule CLI."""

import structlog
import typer

from reporule.repo.ruleset import app as list_app
from reporule.repo.ruleset import app as ruleset_app
from reporule.repo.security import app as security_app

logger = structlog.get_logger()

app = typer.Typer(no_args_is_help=True, pretty_exceptions_short=False)

app.add_typer(list_app, name="list")
app.add_typer(ruleset_app, name="ruleset")
app.add_typer(security_app, name="security")
