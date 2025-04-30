"""Unit tests for core.py"""

import pytest
import requests

from reporule.core import apply_branch_ruleset, get_ruleset_repo_status, list_repos
from reporule.util import _load_branch_ruleset


@pytest.fixture
def default_branch_ruleset():
    """Return the default branch ruleset for use in tests."""
    return _load_branch_ruleset()


@pytest.fixture
def mock_session(mocker):
    """
    Pytest fixture to provide a mocked requests.Session object.
    """
    session = mocker.MagicMock(spec=requests.Session)
    return session


def test_list_repos(repo_list):
    table = list_repos("starfleet", repo_list)
    assert table.row_count == len(repo_list)


def test_apply_branch_ruleset(default_branch_ruleset, mock_session):
    """Test apply_branch_ruleset function."""
    repo_list = ["starfleet/enterprise", "starfleet/cerritos", "starfleet/voyager"]
    rulesets_applied = apply_branch_ruleset(repo_list, default_branch_ruleset, mock_session)
    assert rulesets_applied == 3


def test_get_ruleset_repo_status(mocker, repo_list):
    """Test get_ruleset_repo_status function when no existing rulesets and no exceptions."""
    mocker.patch("reporule.core._get_repo_exceptions", return_value=set())
    mocker.patch("reporule.core._get_branch_rulesets", return_value=[])

    ruleset = {"name": "vulcan_ruleset"}
    repo_status = get_ruleset_repo_status("startfleet", repo_list, ruleset)

    eligible_repos = repo_status["eligible_repos"]
    # repo_list fixture has 5 repos, but one is archived so is not eligible for a ruleset
    assert len(eligible_repos) == 4
    assert eligible_repos == {"starfleet/enterprise", "starfleet/cerritos", "starfleet/voyager", "starfleet/excelsior"}


def test_get_ruleset_repo_status_exceptions(mocker, repo_list):
    """Repos are not eligible for a ruleset if they're on the exception list."""
    mocker.patch("reporule.core._get_repo_exceptions", return_value={"starfleet/enterprise", "starfleet/cerritos"})
    mocker.patch("reporule.core._get_branch_rulesets", return_value=[])

    ruleset = {"name": "vulcan_ruleset"}
    repo_status = get_ruleset_repo_status("startfleet", repo_list, ruleset)

    eligible_repos = repo_status["eligible_repos"]
    assert len(eligible_repos) == 2
    assert eligible_repos == {"starfleet/voyager", "starfleet/excelsior"}


def test_get_ruleset_repo_status_existing_rulesets(mocker, repo_list):
    """Repos are not eligible for a ruleset if they already have a one with the same name."""
    mocker.patch("reporule.core._get_repo_exceptions", return_value={"starfleet/cerritos"})
    mocker.patch("reporule.core._get_branch_rulesets", return_value=["vulcan_ruleset"])

    ruleset = {"name": "vulcan_ruleset"}
    repo_status = get_ruleset_repo_status("startfleet", repo_list, ruleset)

    eligible_repos = repo_status["eligible_repos"]
    assert len(eligible_repos) == 0
