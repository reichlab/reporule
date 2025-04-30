"""Command for adding a ruleset to a repo or set of repos."""

import structlog
import typer
from rich import print
from typing_extensions import Annotated

from reporule.core import apply_branch_ruleset, get_ruleset_repo_status
from reporule.util import (
    _get_repo,
    _load_branch_ruleset,
    _verify_org_or_user,
)

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
        str,
        typer.Option(
            "--ruleset", help="Ruleset filename (from data dir) to apply. Defaults to default_branch_protections"
        ),
    ] = "default_branch_protections",
    all: Annotated[
        bool, typer.Option("--all", "-a", help="Apply ruleset to all org not on the exception list.")
    ] = False,
    dryrun: Annotated[bool, typer.Option("--dryrun", help="Display repos to update without apply changes.")] = False,
):
    # Either we're applying rulesets to a single repo or to all repos
    if repo is None and all is False:
        raise typer.BadParameter("Either --all or --repo must be specified")
    if repo is not None and all is True:
        raise typer.BadParameter("Cannot specify --repo when using --all")

    try:
        ruleset_dict = _load_branch_ruleset(ruleset)
        ruleset_name = ruleset_dict["name"]
    except Exception:
        raise typer.BadParameter(f"Unable to load ruleset name {ruleset}.")

    if all:
        repos = _get_repo(org)
    else:
        repos = _get_repo(org, repo)

    prefix = "DRY RUN:" if dryrun else ""
    print(f"{prefix} Getting list of eligible repositories...")
    repo_status = get_ruleset_repo_status(org, repos, ruleset_dict)
    if repo is not None:
        # User is applying ruleset to specific repo. Unless that single repo
        # is on the exception list, we don't care about the exceptions.
        repo_status["exceptions"] = repo_status["exceptions"].intersection({repo})
    repos_to_skip = repo_status["archived"].union(repo_status["exceptions"]).union(repo_status["existing_ruleset"])
    eligible_repos = repo_status["eligible_repos"]

    if len(repos_to_skip) > 0:
        print(
            f"\n{prefix} Skipping repositories because they are archived, on the exception list or already have a ruleset named {ruleset_name}:"
        )
        for repo in repos_to_skip:
            print(f"  • {repo}")
        print(f"{prefix} Total repositories skipped: {len(repos_to_skip)}")

    total_rulesets_applied = 0
    num_repos = len(eligible_repos)
    if dryrun:
        print(f"\n{prefix} would apply ruleset to {num_repos} repositories:")
        for repo in eligible_repos:
            print(f"  • {repo}")
    else:
        total_rulesets_applied = apply_branch_ruleset(list(eligible_repos), ruleset_dict)  # type: ignore
        print(f"\nApplied {ruleset} to {total_rulesets_applied} repositories.")
