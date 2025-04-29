"""Test reporule cli."""

import pytest
from typer.testing import CliRunner

from reporule.main import app

runner = CliRunner()


@pytest.fixture
def mock_functions(mocker):
    """Mocks for the ruleset command's supporting functions."""
    mocks = {
        "verify_org_or_user": mocker.patch("reporule.repo.ruleset._verify_org_or_user", return_value="user"),
        "load_branch_ruleset": mocker.patch("reporule.repo.ruleset._load_branch_ruleset", return_value={}),
        "get_repo": mocker.patch("reporule.repo.ruleset._get_repo"),
        "get_repo_exceptions": mocker.patch("reporule.repo.ruleset._get_repo_exceptions"),
        "apply_branch_ruleset": mocker.patch("reporule.repo.ruleset.apply_branch_ruleset"),
    }
    return mocks


def test_ruleset_command_all_repos(mock_functions):
    """Test ruleset command with --all option and no --ruleset option."""
    mocked_repos = [
        {"name": "enterprise", "full_name": "starfleet/enterprise", "archived": False},
        {"name": "voyager", "full_name": "starfleet/voyager", "archived": False},
        {"name": "cerritos", "full_name": "starfleet/cerritos", "archived": False},
        {"name": "titan", "full_name": "starfleet/titan", "archived": True},
    ]
    mocked_exceptions = {"starfleet/excelsior", "starfleet/enterprise"}
    mock_functions["get_repo"].return_value = mocked_repos
    mock_functions["get_repo_exceptions"].return_value = mocked_exceptions

    result = runner.invoke(app, ["--verbose", "ruleset", "starfleet", "--all"])
    assert result.exit_code == 0

    # --ruleset option not passed via cli command, so its default value
    # should be used to call _load_branch_ruleset
    mock_functions["load_branch_ruleset"].assert_called_once_with("default_branch_protections")

    # other supporting util functions should be called with
    # the cli's org argument
    mock_functions["verify_org_or_user"].assert_called_once_with("starfleet")
    mock_functions["get_repo"].assert_called_once_with("starfleet")
    mock_functions["get_repo_exceptions"].assert_called_once_with("starfleet")

    # apply_branch_rulesets is called once, and the first parameter
    # is repo_list, which should be a list of the mocked_repos that
    # are eligible to have rulesets applied (i.e., are not archived
    # or not on the exception list)
    mock_functions["apply_branch_ruleset"].assert_called_once

    # because apply_branch_rulesets is only called once, grab the first
    # (and only) call object from the mock_apply_ruleset's call_args_list;
    # a call object is a tuple that represents args and kwargs used to call the mock
    # function, and we unpack it accordingly
    call_args, call_kwargs = mock_functions["apply_branch_ruleset"].call_args_list[0]
    # repo_list is the first argument passed to apply_branch_ruleset
    repo_list = call_args[0]
    expected_ruleset_repos = [
        r["full_name"] for r in mocked_repos if r["full_name"] not in mocked_exceptions and not r["archived"]
    ]
    assert set(repo_list) == set(expected_ruleset_repos)


def test_ruleset_command_single_repos(mock_functions):
    """Test ruleset command with --repo and --ruleset options.

    See comments in test_ruleset_command_all_repos for explanation
    of the call objects associated with Python mocks and how they're used.
    """
    mocked_repos = [
        {"name": "cerritos", "full_name": "starfleet/cerritos", "archived": False},
    ]

    mock_functions["get_repo"].return_value = mocked_repos
    mock_functions["get_repo_exceptions"].return_value = set()

    result = runner.invoke(app, ["ruleset", "starfleet", "--repo", "cerritos", "--ruleset", "mock_ruleset"])
    assert result.exit_code == 0

    mock_functions["verify_org_or_user"].assert_called_once_with("starfleet")
    mock_functions["load_branch_ruleset"].assert_called_once_with("mock_ruleset")
    mock_functions["get_repo"].assert_called_once_with("starfleet", "cerritos")
    mock_functions["get_repo_exceptions"].assert_called_once_with("starfleet")
    mock_functions["apply_branch_ruleset"].assert_called_once

    call_args, call_kwargs = mock_functions["apply_branch_ruleset"].call_args_list[0]
    repo_list = call_args[0]
    assert repo_list == ["starfleet/cerritos"]


def test_ruleset_command_no_eligible_repo(mock_functions):
    """Test ruleset command with --all option and no repos eligible for ruleset."""
    mocked_repos = [
        {"name": "cerritos", "full_name": "starfleet/cerritos", "archived": True},
        {"name": "titan", "full_name": "starfleet/titan", "archived": True},
    ]
    mock_functions["get_repo"].return_value = mocked_repos
    mock_functions["get_repo_exceptions"].return_value = {"starfleet/excelsior"}

    # if all repos on the list are in archive status, don't try applying ruleset
    result = runner.invoke(app, ["ruleset", "starfleet", "--repo", "cerritos", "--ruleset", "mock_ruleset"])
    assert result.exit_code == 0
    mock_functions["apply_branch_ruleset"].assert_not_called

    # if all non-archived repos on the list are in the exception list, don't apply ruleset
    mocked_repos.append({"name": "excelsior", "full_name": "starfleet/excelsior", "archived": False})
    result = runner.invoke(app, ["ruleset", "starfleet", "--repo", "cerritos", "--ruleset", "mock_ruleset"])
    assert result.exit_code == 0
    mock_functions["apply_branch_ruleset"].assert_not_called


@pytest.mark.parametrize(
    "args",
    [
        (["ruleset", "starfleet", "--repo", "cerritos", "--all"]),
        (
            [
                "ruleset",
                "starfleet",
            ]
        ),
        (["ruleset", "--all"]),
    ],
)
def test_ruleset_command_bad_params(mocker, args):
    """Invalid CLI params should fail"""
    mocker.patch("reporule.repo.ruleset._verify_org_or_user", return_value="org")
    result = runner.invoke(app, args)
    assert result.exit_code != 0
