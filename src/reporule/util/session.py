"""Code to handle requests sessions."""

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry  # type: ignore


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
