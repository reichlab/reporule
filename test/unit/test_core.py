"""Unit tests for core.py"""

import pytest
import requests

from reporule.core import apply_branch_ruleset, list_repos
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


def test_apply_branch_ruleset(default_branch_ruleset, repo_list, mocker, mock_session):
    """Test apply_branch_ruleset function."""
    mocker.patch("reporule.core._get_branch_rulesets", return_value=["klingon_ruleset"])

    rulesets_applied = apply_branch_ruleset(repo_list, default_branch_ruleset, mock_session)
    assert rulesets_applied == 4


def test_apply_branch_ruleset_skip(mocker, mock_session, repo_list):
    """Only apply branch ruleset to repos that don't already have a ruleset of the same name."""
    mocker.patch("reporule.core._get_branch_rulesets", return_value=["vulcan_ruleset", "klingon_ruleset"])

    rulesets_applied = apply_branch_ruleset(repo_list, {"name": "vulcan_ruleset"})
    assert rulesets_applied == 0
