import pytest

from chatovod.utils.parsers import patch_ban_info


@pytest.fixture
def ban_info():
    return {"duration": "10,000"}


@pytest.fixture
def ban_data():
    return {"value": 1}


@pytest.fixture
def transformed_ban():
    return {"id": 1, "duration": "10000"}


def test_patch_ban_info(ban_info, ban_data, transformed_ban):
    assert patch_ban_info(ban_info, ban_data) == transformed_ban
