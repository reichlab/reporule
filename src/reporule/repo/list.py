"""Command for listing a GitHub organization's repos."""

import typer
from typing_extensions import Annotated

import reporule
from reporule.core import list_repos
from reporule.util import _get_session

app = typer.Typer(
    add_completion=False,
    help="List the repositories in a GitHub organization.",
)


@app.command(no_args_is_help=True)
def list(
    org: Annotated[str, typer.Argument()],
):
    session = _get_session(reporule.TOKEN)
    list_repos(org, session)


if __name__ == "__main__":
    typer.run(list)
