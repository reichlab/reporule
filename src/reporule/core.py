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
from reporule.util import _get_branch_rulesets, _get_repo_exceptions, _get_session

logger = structlog.get_logger()


class OutputColumns(NamedTuple):
    name: str
    created_at: str
    archived: str
    fork: str
    gh_id: str


def list_repos(org_name: str, repo_list: list[dict]) -> Table:
    """
    Display a rich-formatted table of GitHub repositories.

    Parameters:
    ------------
    org_name : str
        Name of a GitHub organization or user
    repo_list : list
        A list of dictionaries that represent repository objects as returned by
        GitHub's API.
    """

    # Settings for the output columns when listing repo information
    output_column_list = list(OutputColumns._fields)
    output_column_colors = ["green", "magenta", "cyan", "blue", "yellow"]

    # Create the output table and columns
    console = Console()
    table = Table(
        title=f"Public repositories in the {org_name} GitHub organization",
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

    repo_dict = {}
    for repo in repos:
        r = OutputColumns(
            name=f"[link={repo.get('html_url')}]{repo.get('name')}[/link]",
            created_at=str(repo.get("created_at", "")),
            archived=str(repo.get("archived", "")),
            fork=str(repo.get("fork", "")),
            gh_id=str(repo.get("id", "")),
        )
        repo_dict[repo["name"]] = r
    sorted_repo_names = sorted(repo_dict)

    # use sorted repo names to add repo data to the
    # table object in alphabetical order
    try:
        for repo_name in sorted_repo_names:
            r = repo_dict[repo_name]
            table.add_row(*r)
    except Exception as e:
        logger.error(f"Error adding row for repo {r.name}: {e}")

    logger.info("Repository report complete", count=repo_count)

    console.print(table)
    return table


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

        # Apply the branch ruleset
        response = session.post(branch_protection_url, json=ruleset)
        if response.ok:
            print(f"  • {repo}: applied ruleset")
            update_count += 1
        else:
            logger.error("Failed to apply branch ruleset", repo=repo, ruleset=ruleset_name, response=response.json())

    return update_count


def get_ruleset_repo_status(org: str, repo_list: list[dict], ruleset: dict) -> dict[str, set[str]]:
    """
    Determine the ruleset eligibiility status for GitHub repository on the incoming repos list.

    Parameters:
    ------------
    org : str
        The GitHub organization or user name.
    repo_list : list
        A list of dictionaries that represent repository objects as returned by
        GitHub's API.
    ruleset : dict
        The ruleset to check against the repositories

    Returns:
    ---------
    dict[str, str]
        A dictionary mapping repository names to their ruleset status.
    """
    repo_status = {}
    ruleset_name = ruleset["name"]

    all_repos = {r["full_name"] for r in repo_list}
    archived_repos = {r["full_name"] for r in repo_list if r.get("archived")}
    exceptions = _get_repo_exceptions(org)
    eligible_repos = all_repos - archived_repos - exceptions
    existing_ruleset = {repo for repo in eligible_repos if ruleset_name in _get_branch_rulesets(repo)}

    repo_status["archived"] = archived_repos
    repo_status["exceptions"] = exceptions
    repo_status["existing_ruleset"] = existing_ruleset
    repo_status["eligible_repos"] = eligible_repos - existing_ruleset

    logger.debug("Repo eligibility for ruleset", ruleset_name=ruleset_name, repo_status=repo_status)

    return repo_status
