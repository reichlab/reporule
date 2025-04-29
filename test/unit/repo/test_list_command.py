"""Test reporule cli."""

from typer.testing import CliRunner

from reporule.main import app

runner = CliRunner()


def test_list_command(mocker):
    """Test reporule CLI list command."""
    get_repo = mocker.patch("reporule.repo.list._get_repo", return_value=[{"name": "enterprise"}, {"name": "cerritos"}])

    result = runner.invoke(app, ["list", "starfleet"])
    assert result.exit_code == 0
    get_repo.assert_called_once_with("starfleet")


def test_list_command_missing_param(mocker):
    """Test reporule CLI list command."""
    get_repo = mocker.patch("reporule.repo.list._get_repo", return_value=[{"name": "enterprise"}, {"name": "cerritos"}])

    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0
    get_repo.assert_not_called()
