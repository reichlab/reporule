"""Test reporule cli."""

from unittest.mock import patch

from typer.testing import CliRunner

from reporule.main import app

runner = CliRunner()


def test_ruleset_command_all_repos():
    """Test ruleset command with --all option and no --ruleset option."""
    mocked_repos = [
        {"name": "enterprise", "full_name": "starfleet/enterprise", "archived": False},
        {"name": "voyager", "full_name": "starfleet/voyager", "archived": False},
        {"name": "cerritos", "full_name": "starfleet/cerritos", "archived": False},
        {"name": "titan", "full_name": "starfleet/titan", "archived": True},
    ]
    mocked_exceptions = {"starfleet/enterprise"}

    with (
        patch("reporule.repo.ruleset._verify_org_or_user", return_value="org") as mock_verify_org_or_user,
        patch("reporule.repo.ruleset._load_branch_ruleset", return_value={}) as mock_load_branch_ruleset,
        patch("reporule.repo.ruleset._get_repo", return_value=mocked_repos) as mock_get_repo,
        patch("reporule.repo.ruleset._get_repo_exceptions", return_value=mocked_exceptions) as mock_get_exceptions,
        patch("reporule.repo.ruleset.apply_branch_ruleset") as mock_apply_ruleset,
    ):
        expected_ruleset_repos = [
            r["full_name"] for r in mocked_repos if r["full_name"] not in mocked_exceptions and not r["archived"]
        ]

        # Run the CLI command
        result = runner.invoke(app, ["--verbose", "ruleset", "starfleet", "--all"])
        assert result.exit_code == 0

        # --ruleset option not passed via cli command, so its default value
        # should be used to call _load_branch_ruleset
        mock_load_branch_ruleset.assert_called_once_with("default_branch_protections")

        # other supporting util functions should be called with
        # the cli's org argument
        mock_verify_org_or_user.assert_called_once_with("starfleet")
        mock_get_repo.assert_called_once_with("starfleet")
        mock_get_exceptions.assert_called_once_with("starfleet")

        # apply_branch_rulesets is called once, and the first parameter
        # is repo_list, which should be a list of the mocked_repos that
        # are eligible to have rulesets applied (i.e., are not archived
        # or not on the exception list)
        mock_apply_ruleset.assert_called_once

        # because apply_branch_rulesets is only called once, grab the first
        # (and only) call object from the mock_apply_ruleset's call_args_list;
        # a call object is a tuple that represents args and kwargs used to call the mock
        # function, and we unpack it accordingly
        call_args, call_kwargs = mock_apply_ruleset.call_args_list[0]
        # repo_list is the first argument passed to apply_branch_ruleset
        repo_list = call_args[0]
        assert set(repo_list) == set(expected_ruleset_repos)
