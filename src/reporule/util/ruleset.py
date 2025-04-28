"""Load branch ruleset from a JSON file."""

import json

import requests
import structlog
import yaml

import reporule
from reporule import REPORULE_PATH
from reporule.util.session import _get_session

logger = structlog.get_logger()


def _load_branch_ruleset(branchset_name: str = "default_branch_protections") -> dict:
    """
    Return a dictionary that represents the requested branch ruleset.

    Parameters:
    ------------
    branchset_name : str
         Name of the .json branch ruleset to load from the data directory
         Defaults to "default_branch_protections"

    Returns:
    ----------
    dict
        A dictionary that represents the requested branch ruleset

    Raises:
    -------
    ValueError:
        If the requested branch ruleset does not exist
    """
    try:
        file_name = f"{branchset_name}.json"
        with open(REPORULE_PATH / "data" / file_name, "r") as file:
            branch_ruleset = json.load(file)
            logger.debug("Branch ruleset loaded", ruleset_name=branchset_name, branch_ruleset=branch_ruleset)
    except FileNotFoundError:
        raise ValueError(f"Branch ruleset '{branchset_name}' not found.") from None

    return branch_ruleset


def _get_branch_rulesets(repo_name: str, session: requests.Session | None = None) -> list:
    """
    Return a list of existing rulesets for a specified GitHub repository.

    Parameters:
        repo_name : str
            Name of the GitHub repository in the format "org/repo"

    Returns:
        list
            A list of ruleset names applied to the repository

    Raises:
        requests.HTTPError
            If the request to the GitHub API fails
    """
    if session is None:
        session = _get_session(reporule.TOKEN)

    ruleset_url = f"https://api.github.com/repos/{repo_name}/rulesets"
    response = session.get(ruleset_url)
    response.raise_for_status()

    rulesets = [r.get("name") for r in response.json()]
    logger.debug("Existing rulesets", repo=repo_name, rulesets=rulesets)
    return rulesets


def _get_repo_exceptions(org_name: str) -> set[str]:
    """
    Retrieve all repos on the exception list for a given organization or user.

    Parameters:
    ------------
    org_name : str
        Name of a GitHub organization or user
    session: requests.Session
        An optional requests session for using the GitHub API. If not
        passed, a new session will be created.

    Returns:
    ----------
    set
        A set of repositories on the organization's exception_list
        (as defined in data/repos_exception.yml)

    Raises:
    -------
    ValueError
        If the repo_exception.yml file is not found or if it cannot
        be parsed.
    """
    try:
        file_name = REPORULE_PATH / "data" / "repos_exception.yml"
        with open(file_name, "r") as file:
            repo_exceptions = yaml.safe_load(file)
        logger.debug("Repo exceptions loaded", repo_exceptions=repo_exceptions)
        repos = set()
        for org in repo_exceptions.get("organizations", []):
            if org.get("name") == org_name:
                repos = set(org.get("repos", []))

        return repos

    except FileNotFoundError:
        raise ValueError(f"Unable to retrieve repo exceptions list from {file_name}.") from None
