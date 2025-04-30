import pytest


@pytest.fixture
def repo_list():
    """Test GitHub repo data."""
    repos = [
        {
            "id": 123,
            "name": "enterprise",
            "full_name": "starfleet/enterprise",
            "archived": False,
            "fork": False,
            "visibility": "public",
            "created_at": "2340-01-01T00:00:00Z",
        },
        {
            "id": 456,
            "name": "cerritos",
            "full_name": "starfleet/cerritos",
            "archived": False,
            "fork": True,
            "visibility": "public",
            "created_at": "2340-03-01T00:00:00Z",
        },
        {
            "id": 789,
            "name": "discovery",
            "full_name": "starfleet/discovery",
            "archived": True,
            "fork": False,
            "visibility": "public",
            "created_at": "2210-01-01T00:00:00Z",
        },
        {
            "id": 321,
            "name": "voyager",
            "full_name": "starfleet/voyager",
            "archived": False,
            "fork": False,
            "visibility": "private",
            "created_at": "2340-05-01T00:00:00Z",
        },
        {
            "id": 654,
            "name": "excelsior",
            "full_name": "starfleet/excelsior",
            "archived": False,
            "fork": False,
            "visibility": "public",
            "created_at": "2340-05-01T00:00:00Z",
        },
    ]

    return repos


@pytest.fixture()
def ruleset_list():
    rulesets = [
        {
            "id": 123,
            "name": "default-branch-protections",
            "target": "branch",
            "source_type": "Repository",
            "enforcement": "active",
        },
        {"id": 456, "name": "vulcan_ruleset", "target": "branch", "source_type": "Repository", "enforcement": "active"},
        {
            "id": 789,
            "name": "klingon_ruleset",
            "target": "branch",
            "source_type": "Repository",
            "enforcement": "active",
        },
    ]

    return rulesets
