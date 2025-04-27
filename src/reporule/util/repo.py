"""Functions to get information about GitHub repositories."""

import requests


def _get_all_repos(org_name: str, session: requests.Session) -> list[dict]:
    """
    Retrieve all repositories from a GitHub organization or user.

    Parameters:
    ------------
    org_name : str
        Name of a GitHub organization or user
    session: requests.Session
        A requests session for using the GitHub API

    Returns:
    ----------
    list
        A list of dictionaries that represents the org/user repositories

    Raises:
    -------
    ValueError
        If org_name is not a valid GitHub organization or user
    """
    response = session.get(f"https://api.github.com/orgs/{org_name}")
    if response.ok:
        repos_url = f"https://api.github.com/orgs/{org_name}/repos"
    else:
        response = session.get(f"https://api.github.com/users/{org_name}")
        if response.ok:
            repos_url = f"https://api.github.com/users/{org_name}/repos"
        else:
            raise ValueError(f"Organization or user '{org_name}' not found.") from None

    repos = []
    while repos_url:
        response = session.get(repos_url)
        response.raise_for_status()
        repos.extend(response.json())
        repos_url = response.links.get("next", {}).get("url")
    return repos
