"""Command for adding standard Reichlab ruleset to a repo."""

import typer
from typing_extensions import Annotated

app = typer.Typer()


@app.command(no_args_is_help=True)
def ruleset(
    repo: Annotated[str, typer.Option()],
    org: Annotated[str, typer.Option()] = "reichlab",
):
    print(f"Adding default branch ruleset to {org}/{repo}...")
