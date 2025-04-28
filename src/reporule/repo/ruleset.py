"""Command for adding a ruleset to a repo or set of repos."""

import structlog
import typer
from rich import print
from typing_extensions import Annotated

from reporule.core import apply_branch_ruleset
from reporule.util.repo import _get_repo, _verify_org_or_user
from reporule.util.ruleset import _get_repo_exceptions, _load_branch_ruleset

logger = structlog.get_logger()

app = typer.Typer()


def validate_org(org: str) -> str:
    """
    Validate the GitHub organization or user name.

    Parameters:
    ------------
    org : str
        The GitHub organization or user name.

    Returns:
    ---------
    str
        The validated organization name.
    """
    org_or_user = _verify_org_or_user(org)
    if not org_or_user:
        raise typer.BadParameter(f"{org} is not valid GitHub organization or user")
    return org


@app.command(no_args_is_help=True)
def ruleset(
    org: Annotated[str, typer.Argument(help="GitHub organization or user name.", callback=validate_org)],
    repo: Annotated[
        str | None,
        typer.Option(
            "--repo",
            "-r",
            help="GitHub repository name (must belong to the specified org). Ignored when --all is specified.",
        ),
    ] = None,
    ruleset: Annotated[
        str, typer.Option("--ruleset", help="Ruleset (from data dir) to apply. Defaults to default_branch_protections")
    ] = "default_branch_protections",
    all: Annotated[
        bool, typer.Option("--all", "-a", help="Apply ruleset to all org not on the exception list.")
    ] = False,
):
    # Either we're applying rulesets to a single repo or to all repos
    if repo is None and all is False:
        raise typer.BadParameter("Either --all or --repo must be specified")
    if repo is not None and all is True:
        raise typer.BadParameter("Cannot specify --repo when using --all")

    try:
        ruleset_dict = _load_branch_ruleset(ruleset)
    except Exception:
        raise typer.BadParameter(f"Unable to load ruleset name {ruleset}.")

    if all:
        # create a list of repos (in org/repo format) to apply the ruleset to
        # (exclude archived repos)
        repos = _get_repo(org)
        repo_set = {f"{org}/{r['name']}" for r in repos if not r.get("archived")}
    else:
        repos = _get_repo(org, repo)
        repo = repos[0]["name"]
        repo_set = {f"{org}/{repo}"}

    # remove repos on the exception list
    exception_set = _get_repo_exceptions(org)
    ruleset_repos = repo_set - exception_set
    repos_to_skip = set.intersection(exception_set, repo_set)

    logger.debug(
        "Calculated repo lists",
        exception_set=exception_set,
        ruleset_repos=ruleset_repos,
        repos_to_skip=repos_to_skip,
        repos_to_update=len(ruleset_repos),
    )

    if len(repos_to_skip) > 0:
        print(f"Skipping {len(repos_to_skip)} repositories on the exception list:")
        for repo in repos_to_skip:
            print(f"  • {repo}")

    total_rulesets_applied = 0
    if len(ruleset_repos) > 0:
        total_rulesets_applied = apply_branch_ruleset(list(ruleset_repos), ruleset_dict)  # type: ignore

    print(f"\nApplied {ruleset} to {total_rulesets_applied} repositories.")
