from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.api.api import app, get_storage
from app.domain import AccountStorage


@pytest.fixture
def test_storage(tmp_path: Path):
    db_path = tmp_path / "test_bank.db"
    storage = AccountStorage(str(db_path))
    return storage


@pytest.fixture
def client(test_storage):
    app.dependency_overrides[get_storage] = lambda: test_storage
    with TestClient(app) as c:
        yield c
