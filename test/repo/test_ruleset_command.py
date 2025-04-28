"""Test reporule cli."""

from unittest.mock import patch

from typer.testing import CliRunner

from reporule.main import app

runner = CliRunner()


def test_ruleset_command_all_repos(setenvvar):
    mocked_repos = [
        {"name": "enterprise", "full_name": "starfleet/enterprise", "archived": False},
        {"name": "voyager", "full_name": "starfleet/voyager", "archived": False},
        {"name": "cerritos", "full_name": "starfleet/cerritos", "archived": False},
        {"name": "titan", "full_name": "starfleet/titan", "archived": True},
    ]
    mocked_exceptions = {"starfleet/enterprise"}

    # Mock _get_repo to return mocked_repos
    with (
        patch("reporule.repo.ruleset._verify_org_or_user", return_value="org") as mock_verify_org_or_user,
        patch("reporule.repo.ruleset._get_repo", return_value=mocked_repos) as mock_get_repo,
        patch("reporule.repo.ruleset._get_repo_exceptions", return_value=mocked_exceptions) as mock_get_exceptions,
        patch("reporule.repo.ruleset.apply_branch_ruleset") as mock_apply_ruleset,
    ):
        expected_ruleset_repos = [
            r["full_name"] for r in mocked_repos if r["full_name"] not in mocked_exceptions and not r["archived"]
        ]

        # Run the CLI command
        result = runner.invoke(app, ["--verbose", "ruleset", "starfleet", "--all"])
        actual_calls = mock_apply_ruleset.call_args_list

        assert result.exit_code == 0
        mock_verify_org_or_user.assert_called_once_with("starfleet")
        mock_get_repo.assert_called_once_with("starfleet")
        mock_get_exceptions.assert_called_once_with("starfleet")

        # the number of calls to apply_branch_ruleset should equal
        # the number of repos we're applying the ruleset to
        assert len(actual_calls[0].args) == len(expected_ruleset_repos)

        # repo_name args passed to apply_branch_ruleset should match names
        # in the expected_ruleset_repos
        # (this is some weird parsing of the mocked objects calls because
        # using assert_has_calls intermittently failed due to the
        # ordering of lists, even when using any_order=True)
        actual_repo_list = actual_calls[0].args[0]
        assert set(actual_repo_list) == set(expected_ruleset_repos)
