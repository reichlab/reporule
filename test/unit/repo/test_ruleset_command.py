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
        "load_branch_ruleset": mocker.patch(
            "reporule.repo.ruleset._load_branch_ruleset", return_value={"name": "vulcan_ruleset"}
        ),
        "get_repo": mocker.patch("reporule.repo.ruleset._get_repo", return_value=[]),
        "get_ruleset_repo_status": mocker.patch("reporule.repo.ruleset.get_ruleset_repo_status"),
        "apply_branch_ruleset": mocker.patch("reporule.repo.ruleset.apply_branch_ruleset"),
    }
    return mocks


@pytest.fixture
def repo_status():
    """Mocked repo status for testing.

    This fixture returns a dictionary that mocks the return
    value of core.get_ruleset_repo_status. "eligible_repos" is the
    only key used by ruleset.py when calling the apply_branch_ruleset,
    so the individual tests will set this value. The other keys are
    here for completeness but aren't used.
    """
    repo_status = {
        "archived": set(),
        "exceptions": set(),
        "existing_ruleset": set(),
        "eligible_repos": {"placeholder/replaced_by_test"},
    }
    return repo_status


@pytest.mark.parametrize(
    "cli_args,eligible_repo_set,ruleset_file_name",
    [
        (["ruleset", "starfleet", "--all"], {"starfleet/enterprise", "starfleet/cerritos"}, None),
        (["ruleset", "starfleet", "--all", "--ruleset", "vulcan_ruleset"], {"starfleet/cerritos"}, "vulcan_ruleset"),
    ],
)
def test_ruleset_commands_all(mock_functions, repo_status, cli_args, eligible_repo_set, ruleset_file_name):
    """Test the ruleset CLI command when used with --all option."""
    repo_status["eligible_repos"] = eligible_repo_set
    mock_functions["get_ruleset_repo_status"].return_value = repo_status

    result = runner.invoke(app, cli_args)
    assert result.exit_code == 0

    # _load_branch_ruleset should be called with --ruleset value if passed as cli arg,
    # or with its default value of default_branch_protections
    expected_ruleset_name = ruleset_file_name or "default_branch_protections"
    mock_functions["load_branch_ruleset"].assert_called_once_with(expected_ruleset_name)

    mock_functions["verify_org_or_user"].assert_called_once_with("starfleet")
    mock_functions["get_repo"].assert_called_once_with("starfleet")
    mock_functions["apply_branch_ruleset"].assert_called_once

    # first parameter passed to apply_branch_ruleset should match repo_set["eligible_repos"]
    expected_ruleset_repos = repo_status["eligible_repos"]
    call_args, call_kwargs = mock_functions["apply_branch_ruleset"].call_args_list[0]
    repo_list = call_args[0]

    assert set(repo_list) == set(expected_ruleset_repos)


def test_ruleset_commands_repo(mock_functions, repo_status):
    """Test the ruleset CLI command when used with --repo option."""
    repo_status["eligible_repos"] = {"starfleet/cerritos"}
    mock_functions["get_ruleset_repo_status"].return_value = repo_status

    result = runner.invoke(
        app,
        ["ruleset", "starfleet", "--repo", "cerritos"],
    )
    assert result.exit_code == 0

    mock_functions["verify_org_or_user"].assert_called_once_with("starfleet")
    mock_functions["get_repo"].assert_called_once_with("starfleet", "cerritos")
    mock_functions["apply_branch_ruleset"].assert_called_once

    # first parameter passed to apply_branch_ruleset should match repo_set["eligible_repos"]
    expected_ruleset_repos = repo_status["eligible_repos"]
    call_args, call_kwargs = mock_functions["apply_branch_ruleset"].call_args_list[0]
    repo_list = call_args[0]

    assert set(repo_list) == set(expected_ruleset_repos)


def test_ruleset_commands_no_eligible_repos(mock_functions, repo_status):
    """Test the ruleset CLI command when no repos are eligible for ruleset update."""
    mock_functions["get_ruleset_repo_status"].return_value = repo_status

    result = runner.invoke(
        app,
        ["ruleset", "starfleet", "--all"],
    )
    assert result.exit_code == 0

    mock_functions["apply_branch_ruleset"].assert_not_called


def test_ruleset_commands_dryrun(mock_functions, repo_status):
    """Test the ruleset CLI command --dryrun option."""
    repo_status["eligible_repos"] = {"starfleet/enterprise", "starfleet/cerritos"}
    mock_functions["get_ruleset_repo_status"].return_value = repo_status

    result = runner.invoke(
        app,
        ["ruleset", "starfleet", "--all", "--dryrun"],
    )
    assert result.exit_code == 0
    assert "DRY RUN" in result.output.upper()

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
