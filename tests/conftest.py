"""Global test configuration enhancements."""

from unittest.mock import Mock

import pytest
from pytest_mock import MockerFixture


def pytest_configure(config: pytest.Config) -> None:
    """Add custom configuration to pytest command-line arguments."""
    config.addinivalue_line("markers", "e2e: mark as end-to-end test.")


@pytest.fixture
def mock_requests_get(mocker: MockerFixture) -> Mock:
    """Fixture for mocking Wikipedia API responses."""
    mock = mocker.patch("requests.get")
    mock.return_value.__enter__.return_value.json.return_value = {
        "title": "Guy Hoozdis",
        "extract": "Who is this guy?",
    }
    return mock
