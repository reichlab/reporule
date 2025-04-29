"""Unit tests for util.py."""

import pytest
import requests

from reporule.util import _get_branch_rulesets, _get_repo


@pytest.fixture
def mock_session(mocker):
    """
    Pytest fixture to provide a mocked requests.Session object.
    """
    response = mocker.MagicMock(spec=requests.Response)
    response.status_code = 200
    session = mocker.MagicMock(spec=requests.Session)
    return session, response


def test__get_branch_rulesets(mocker, mock_session, ruleset_list):
    "Test data returned by _get_branch_rulesets function."
    # mock a requests.Session and response
    session, response = mock_session
    mocker.patch.object(response, "json", return_value=ruleset_list)
    mocker.patch.object(session, "get", return_value=response)

    # function should return a list of ruleset names
    expected_rulesets = [r.get("name") for r in ruleset_list]
    returned_rulesets = _get_branch_rulesets("starfleet/enterprise", session=session)
    assert set(expected_rulesets) == set(returned_rulesets)


@pytest.mark.parametrize("org_user_value", ["org", "user"])
def test__get_repo(mocker, mock_session, org_user_value, repo_list):
    """Test that _get_repo calls the correct GitHub API endpoint when getting repo list."""
    mocker.patch("reporule.util._verify_org_or_user", return_value=org_user_value)
    # mock a requests.Session and response
    session, response = mock_session
    mocker.patch.object(response, "json", return_value=repo_list[0])
    mocker.patch.object(session, "get", return_value=response)

    _get_repo("starfleet", session=session)

    # mocked response doesn't paginate, so we expect only one call to the GitHub API
    calls = session.get.call_args_list
    assert len(calls) == 1

    # confirm that the GitHub API endpoint called is org/ or user/, depending
    # on the result of the _verify_org_or_user utility function
    expected_route = "orgs" if org_user_value == "org" else "users"
    call_args = session.get.call_args_list[0].args
    assert f"https://api.github.com/{expected_route}/starfleet/repos" in call_args


@pytest.mark.parametrize("org_user_value", ["org", "user"])
def test__get_repo_single_repo(mocker, mock_session, org_user_value, repo_list):
    """Test that _get_repo calls the correct GitHub API endpoint when getting single repo."""
    mocker.patch("reporule.util._verify_org_or_user", return_value=org_user_value)
    # mock a requests.Session and response
    session, response = mock_session
    mocker.patch.object(response, "json", return_value=repo_list[0])
    mocker.patch.object(session, "get", return_value=response)

    _get_repo("starfleet", "enterprise", session=session)

    # no pagination for a single repo, so we expect only one call to the GitHub API
    calls = session.get.call_args_list
    assert len(calls) == 1

    call_args = session.get.call_args_list[0].args
    assert "https://api.github.com/repos/starfleet/enterprise" in call_args
