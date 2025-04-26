"""Command for adding recommended security settings to a repo."""

import typer
from typing_extensions import Annotated

app = typer.Typer()


@app.command(no_args_is_help=True)
def security(
    repo: Annotated[str, typer.Option()],
    org: Annotated[str, typer.Option()] = "reichlab",
):
    print(f"Adding security settings to {org}/{repo}...")
