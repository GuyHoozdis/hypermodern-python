"""The test cases for the console module."""

from unittest.mock import Mock

# TODO: The configurations for black and flake8-black are inconsistent.  Also, I hate this choice
# for import ordering.  Fix it.
from click.testing import CliRunner
import pytest
from pytest_mock import MockerFixture
import requests

from hypermodern_guyhoozdis import console


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


@pytest.fixture
def mock_wikipedia_random_page(mocker: MockerFixture) -> Mock:
    """Fixture for mocking wikipedia.random_page."""
    return mocker.patch("hypermodern_guyhoozdis.wikipedia.random_page")


# TODO: This is an integration test, not a unit test.
def test_main_succeeds(runner: CliRunner) -> None:
    """It exists with a status code of zero."""
    result = runner.invoke(console.main)
    assert result.exit_code == 0


# TODO: This is an integration test, not a unit test.
def test_main_prints_title(runner: CliRunner, mock_requests_get: Mock) -> None:
    """It prints the title of the Wikipedia page."""
    result = runner.invoke(console.main)
    assert "Guy Hoozdis" in result.output


# TODO: This is an integration test, not a unit test.
def test_main_fails_on_request_error(
    runner: CliRunner, mock_requests_get: Mock
) -> None:
    """It exits with non-zero status code if the request fails."""
    mock_requests_get.side_effect = requests.RequestException
    result = runner.invoke(console.main)
    assert result.exit_code == 1


# TODO: This is an integration test, not a unit test.
def test_main_prints_message_on_request_error(
    runner: CliRunner, mock_requests_get: Mock
) -> None:
    """It prints an error message if the request fails."""
    mock_requests_get.side_effect = requests.RequestException
    result = runner.invoke(console.main)
    assert "Error" in result.output


# TODO: This is an integration test, not a unit test.
def test_main_uses_specified_language(
    runner: CliRunner, mock_wikipedia_random_page: Mock
) -> None:
    """It uses the specified langage edition of the Wikipedia API."""
    language = "pl"
    runner.invoke(console.main, [f"--language={language}"])
    mock_wikipedia_random_page.assert_called_once_with(language=language)


@pytest.mark.e2e
def test_main_succeeds_in_production_env(runner: CliRunner) -> None:
    """It exists with a status code of zero (end-to-end)."""
    result = runner.invoke(console.main)
    assert result.exit_code == 0
