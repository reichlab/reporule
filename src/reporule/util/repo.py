"""Functions to get information about GitHub repositories."""

import requests


def _get_all_repos(org_name: str, session: requests.Session) -> list[dict]:
    """
    Retrieve all repositories from a GitHub organization, handling pagination.

    :param org_name: Name of the GitHub organization
    :param session: Requests session for interacting with the GitHub API
    :return: List of repositories
    """
    repos = []
    repos_url = f"https://api.github.com/orgs/{org_name}/repos"
    while repos_url:
        response = session.get(repos_url)
        response.raise_for_status()
        repos.extend(response.json())
        repos_url = response.links.get("next", {}).get("url")
    return repos
