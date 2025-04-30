"""Command for listing a GitHub organization's repos."""

import typer
from typing_extensions import Annotated

from reporule.core import list_repos
from reporule.util import _get_repo

app = typer.Typer(
    add_completion=False,
    help="List public repositories belonging to a GitHub organization or user.",
)


@app.command(no_args_is_help=True)
def list(
    org: Annotated[str, typer.Argument()],
):
    """
    Display a list of public repositories and their selected attributes for a
    specific GitHub organization or user.

    EXAMPLE: reporule list hubverse-org
    """
    print(f"Getting public repos for {org}...")
    repos = _get_repo(org)
    list_repos(org, repos)


if __name__ == "__main__":
    typer.run(list)
