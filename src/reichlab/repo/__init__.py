import typer

from .ruleset import app as ruleset_app
from .security import app as security_app

app = typer.Typer()

app.add_typer(ruleset_app)
app.add_typer(security_app)
