"""Command for listing a GitHub organization's repos."""

import typer
from typing_extensions import Annotated

from reporule.core import list_repos
from reporule.util import _get_repo

app = typer.Typer(
    add_completion=False,
    help="List the public repositories that belong to a GitHub organization or user.",
)


@app.command(no_args_is_help=True)
def list(
    org: Annotated[str, typer.Argument()],
):
    print(f"Getting public repos for {org}...")
    repos = _get_repo(org)
    list_repos(org, repos)


if __name__ == "__main__":
    typer.run(list)
