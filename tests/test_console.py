import click.testing
import pytest
import requests

from hypermodern_python import console, wikipedia


@pytest.fixture
def runner():
    return click.testing.CliRunner()


@pytest.fixture
def mock_wikipedia_random_page(mocker):
    return mocker.patch("hypermodern_python.wikipedia.random_page")


def test_main_succeeds(runner, mock_requests_get):
    result = runner.invoke(console.main)
    assert result.exit_code == 0


def test_main_prints_title(runner, mock_requests_get):
    result = runner.invoke(console.main)
    assert "Guy Hoozdis" in result.output


# TODO: This test should be moved into test_wikipedia.py and modified appropriately for the new context.
def test_main_fails_on_request_error(runner, mock_requests_get):
    mock_requests_get.side_effect = Exception("Boom")
    result = runner.invoke(console.main)
    assert result.exit_code == 1
    assert "Boom" == str(result.exception)


# TODO: This is an integration test, not a unit test.
def test_main_prints_message_on_request_error(runner, mock_requests_get):
    mock_requests_get.side_effect = requests.RequestException
    result = runner.invoke(console.main)
    assert "Error" in result.output


# TODO: This is an integration test, not a unit test.
def test_main_uses_specified_language(runner, mock_wikipedia_random_page):
    language = "pl"
    runner.invoke(console.main, [f"--language={language}"])
    mock_wikipedia_random_page.assert_called_once_with(language=language)


@pytest.mark.e2e
def test_main_succeeds_in_production_env(runner):
    result = runner.invoke(console.main)
    assert result.exit_code == 0
