"""Utility functions for reporules."""

import json
from pathlib import Path

import requests
import structlog
import yaml
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry  # type: ignore

import reporule
from reporule import REPORULE_PATH

logger = structlog.get_logger()


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


def _get_repo(org_name: str, repo_name: str | None = None, session: requests.Session | None = None) -> list[dict]:
    """
    Retrieve information about public GitHub repositories.

    Parameters:
    ------------
    org_name : str
        Name of a GitHub organization or user
    repo_name : str
        An optional name of the public GitHub repo to retrieve. If not specified,
        all repositories for the org_name will be returned.
    session: requests.Session
        An optional requests session for using the GitHub API. If not
        passed, a new session will be created.

    Returns:
    ----------
    list
        A list of dictionaries that represents the org/user repositories

    Raises:
    -------
    ValueError
        If org_name is not a valid GitHub organization or user
    """
    if session is None:
        session = _get_session(reporule.TOKEN)
    github_type = _verify_org_or_user(org_name, session)
    if github_type == "org":
        repos_url = f"https://api.github.com/orgs/{org_name}/repos"
    elif github_type == "user":
        repos_url = f"https://api.github.com/users/{org_name}/repos"
    else:
        raise ValueError(f"Organization or user '{org_name}' not found.") from None

    # if we want a specific repo, use the repos route
    if repo_name:
        repos_url = f"https://api.github.com/repos/{org_name}/{repo_name}"

    repos = []
    while repos_url:
        response = session.get(repos_url)
        response.raise_for_status()
        if isinstance(response.json(), dict):
            # we only requested a single repo
            repos.append(response.json())
            break
        repos.extend(response.json())
        repos_url = response.links.get("next", {}).get("url")
    return repos


def _get_repo_exceptions(org_name: str, file_name: Path) -> set[str]:
    """
    Retrieve all repos on the exception list for a given organization or user.

    Parameters:
    ------------
    org_name : str
        Name of a GitHub organization or user
    file_name : Path
        Optional full path to the yaml file containing the exceptions list.
        Defaults to "data/repos_exception.yml".
    session: requests.Session
        An optional requests session for using the GitHub API. If not
        passed, a new session will be created.

    Returns:
    ----------
    set
        A set of repositories on the organization's exception_list
        (as defined in data/repos_exception.yml). Repositories in the
        reflect their full name (i.e., org/repo or user/repo).

    Raises:
    -------
    ValueError
        If the repo_exception.yml file is not found or if it cannot
        be parsed.
    """
    try:
        if file_name is None:
            file_name = REPORULE_PATH / "data" / "repos_exception.yml"
        with open(file_name, "r") as file:
            repo_exceptions = yaml.safe_load(file)
        logger.debug("Repo exceptions loaded", repo_exceptions=repo_exceptions)
        repos = set()
        for org in repo_exceptions.get("organizations", []):
            if org.get("name") == org_name:
                repos = set(org.get("repos", []))

        # return the full name of each repo on the exception list
        repo_full_name = set()
        for repo in repos:
            repo_full_name.add(f"{org_name}/{repo}")
        return repo_full_name

    except FileNotFoundError:
        raise ValueError(f"Unable to retrieve repo exceptions list from {file_name}.") from None


def _get_session(token: str) -> requests.Session:
    """Return a requests session with retry logic."""

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    session = requests.Session()

    # attach a urllib3 retry adapter to the requests session
    # https://urllib3.readthedocs.io/en/latest/reference/urllib3.util.html#urllib3.util.retry.Retry
    retries = Retry(
        total=5,
        allowed_methods=frozenset(["GET", "POST", "PATCH"]),
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    session.mount("https://", HTTPAdapter(max_retries=retries))
    session.headers.update(headers)

    return session


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


def _verify_org_or_user(org_name: str, session: requests.Session | None = None) -> str | None:
    """
    Determines whether the specified org_name represents a GitHub organization,
    a GitHub user, or neither.

    Parameters:
    ------------
    org_name : str
        Name of a GitHub organization or user
    session: requests.Session
        An optional requests session for using the GitHub API. If not
        passed, a new session will be created.

    Returns:
    ----------
    str
        Returns 'org' if org_name is a GitHub organization, 'user' if
        org_name is a GitHub user, or None if neither.
    """
    if session is None:
        session = _get_session(reporule.TOKEN)
    response = session.get(f"https://api.github.com/orgs/{org_name}")
    if response.ok:
        logger.debug("GitHub organization found", org_name=org_name, org_info=response.json())
        return "org"
    response = session.get(f"https://api.github.com/users/{org_name}")
    if response.ok:
        logger.debug("GitHub user found", user_name=org_name, user_info=response.json())
        return "user"
    return None
