"""Core functions for reporule operations."""

from itertools import zip_longest
from typing import NamedTuple

import requests
import structlog
from rich.console import Console
from rich.style import Style
from rich.table import Table

from reporule.util.repo import _get_all_repos

logger = structlog.get_logger()


class OutputColumns(NamedTuple):
    name: str
    created_at: str
    archived: str
    visibility: str
    id: str


def list_repos(org_name: str, session: requests.Session) -> None:
    """
    List repositories in an organization.

    Parameters:
    ------------
    org_name : str
         Name of a GitHub organization
    session : requests.Session
         A requests session for using the GitHub API
    """
    # Settings for the output columns when listing repo information
    output_column_list = list(OutputColumns._fields)
    output_column_colors = ["green", "magenta", "cyan", "blue", "yellow"]

    # Create the output table and columns
    console = Console()
    table = Table(
        title=f"Repositories in the {org_name} GitHub organization",
    )
    for col, color in zip_longest(output_column_list, output_column_colors, fillvalue="cyan"):
        # add additional attributes, depending on the column
        style_kwargs = {}
        col_kwargs = {}
        if col == "name":
            col_kwargs = {"ratio": 4}
            style_kwargs = {"link": True}

        style = Style(color=color, **style_kwargs)  # type: ignore
        table.add_column(col, style=style, **col_kwargs)  # type: ignore

    repos = _get_all_repos(org_name, session)
    repo_count = len(repos)

    for repo in repos:
        r = OutputColumns(
            name=f"[link={repo.get('html_url')}]{repo.get('name')}[/link]",
            created_at=str(repo.get("created_at", "")),
            archived=str(repo.get("archived", "")),
            visibility=str(repo.get("visibility", "")),
            id=str(repo.get("id", "")),
        )
        try:
            table.add_row(*r)
        except Exception as e:
            logger.error(f"Error adding row for repo {r.name}: {e}")

    logger.info("Repository report complete", count=repo_count)

    console.print(table)
