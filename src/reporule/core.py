"""Core functions for reporule operations."""

from itertools import zip_longest
from typing import NamedTuple

import requests
import structlog
from rich import print
from rich.console import Console
from rich.style import Style
from rich.table import Table

import reporule
from reporule.util import _get_branch_rulesets, _get_session

logger = structlog.get_logger()


class OutputColumns(NamedTuple):
    name: str
    created_at: str
    archived: str
    visibility: str
    id: str


def list_repos(org_name: str, repo_list: list[dict]) -> None:
    """
    Display a rich-formatted table of GitHub repositories.

    Parameters:
    ------------
    org_name : str
        Name of a GitHub organization or user
    repo_list : dict
        A list of dictionaries that represent repository objects as returned by
        GitHub's API.
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

    repos = repo_list
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


def apply_branch_ruleset(repo_list: list[str], ruleset: dict, session: requests.Session | None = None) -> int:
    """
    Apply a branch ruleset to every specified repository

    Parameters:
    ------------
    repo_list: list
        A list of repository names that will have the ruleset applied.
        List items are in the format "org/repo"
    ruleset: dict
        The GitHub ruleset to apply
    session: requests.Session
        An optional requests session for using the GitHub API. If not
        passed, a new session will be created.

    Returns:
    ---------
    int
        The number of repositories that were updated with the ruleset
    """
    if session is None:
        session = _get_session(reporule.TOKEN)

    update_count = 0
    ruleset_name = ruleset.get("name")
    print("Applying ruleset:", ruleset_name)
    for repo in repo_list:
        branch_protection_url = f"https://api.github.com/repos/{repo}/rulesets"

        # Get repo's existing rulesets
        existing_rulsets = _get_branch_rulesets(repo)
        if ruleset_name in existing_rulsets:
            print(f"  • {repo}: skipped, already has ruleset {ruleset.get('name')}")
            continue

        # Apply the branch ruleset
        response = session.post(branch_protection_url, json=ruleset)
        if response.ok:
            print(f"  • {repo}: applied ruleset")
            update_count += 1
        else:
            logger.error("Failed to apply branch ruleset", repo=repo, ruleset=ruleset_name, response=response.json())

    return update_count
