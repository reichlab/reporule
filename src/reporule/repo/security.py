"""Command for adding recommended security settings to a repo."""

import typer
from typing_extensions import Annotated

app = typer.Typer()


@app.command(no_args_is_help=True)
def security(
    org: Annotated[str, typer.Argument(help="GitHub organization or user name.")],
):
    print("Not yet implemented")
    print("See https://hubverse.io/en/latest/developer/security.html for more information")
    print("about applying security settings to a GitHub organization")
