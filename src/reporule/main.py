"""Create the reporule CLI."""

import logging

import structlog
import typer

from reporule.repo.list import app as list_app
from reporule.repo.ruleset import app as ruleset_app

logger = structlog.get_logger()

app = typer.Typer(no_args_is_help=True, pretty_exceptions_show_locals=False, add_completion=False)


@app.callback()
def main(verbose: bool = typer.Option(False, "--verbose", "-v")):
    lvl = logging.INFO
    if verbose:
        lvl = logging.DEBUG
    logging.basicConfig(level=lvl)


app.add_typer(list_app, no_args_is_help=True)
app.add_typer(ruleset_app, no_args_is_help=True)
