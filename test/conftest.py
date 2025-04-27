import os
from unittest import mock

import pytest


@pytest.fixture()
def setenvvar(monkeypatch):
    with mock.patch.dict(os.environ, clear=True):
        envvars = {
            "GITHUB_TOKEN": "faketoken",
        }
        for k, v in envvars.items():
            monkeypatch.setenv(k, v)
        yield
