"""Functions to get information about GitHub repositories."""

import requests
import structlog

import reporule
from reporule.util.session import _get_session

logger = structlog.get_logger()


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
