"""Command for listing a GitHub organization's repos."""

import typer
from typing_extensions import Annotated

app = typer.Typer()


@app.command(no_args_is_help=True)
def security(
    org: Annotated[str, typer.Option()] = "reichlab",
):
    print(f"List repos for {org}...")
