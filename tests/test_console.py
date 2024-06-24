from unittest.mock import Mock

import pytest
import requests
from click.testing import CliRunner
from pytest_mock import MockerFixture

from hypermodern_python import console


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


@pytest.fixture
def mock_wikipedia_random_page(mocker: MockerFixture) -> Mock:
    return mocker.patch("hypermodern_python.wikipedia.random_page")


# TODO: This is an integration test, not a unit test.
def test_main_succeeds(runner: CliRunner) -> None:
    result = runner.invoke(console.main)
    assert result.exit_code == 0


# TODO: This is an integration test, not a unit test.
def test_main_prints_title(runner: CliRunner) -> None:
    result = runner.invoke(console.main)
    assert "Guy Hoozdis" in result.output


# TODO: This is an integration test, not a unit test.
def test_main_prints_message_on_request_error(runner: CliRunner, mock_requests_get: Mock) -> None:
    mock_requests_get.side_effect = requests.RequestException
    result = runner.invoke(console.main)
    assert "Error" in result.output


# TODO: This is an integration test, not a unit test.
def test_main_uses_specified_language(runner: CliRunner, mock_wikipedia_random_page: Mock) -> None:
    language = "pl"
    runner.invoke(console.main, [f"--language={language}"])
    mock_wikipedia_random_page.assert_called_once_with(language=language)


@pytest.mark.e2e
def test_main_succeeds_in_production_env(runner: CliRunner) -> None:
    result = runner.invoke(console.main)
    assert result.exit_code == 0
