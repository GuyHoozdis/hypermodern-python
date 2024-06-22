import click.testing
import pytest
import requests

from hypermodern_python import console, wikipedia


@pytest.fixture
def runner():
    return click.testing.CliRunner()


@pytest.fixture
def mock_requests_get(mocker):
    mock = mocker.patch("requests.get")
    mock.return_value.__enter__.return_value.json.return_value = {
        "title": "Guy Hoozdis",
        "extract": "Who is this guy?",
    }
    return mock


def test_main_succeeds(runner, mock_requests_get):
    result = runner.invoke(console.main)
    assert result.exit_code == 0


def test_main_prints_title(runner, mock_requests_get):
    result = runner.invoke(console.main)
    assert "Guy Hoozdis" in result.output


# TODO: This test should be moved into test_wikipedia.py and modified appropriately for the new context.
def test_main_uses_en_wikipedia_org(runner, mock_requests_get):
    _ = runner.invoke(console.main)
    mock_requests_get.assert_called_once_with(wikipedia.API_URL)


# TODO: This test should be moved into test_wikipedia.py and modified appropriately for the new context.
def test_main_fails_on_request_error(runner, mock_requests_get):
    mock_requests_get.side_effect = Exception("Boom")
    result = runner.invoke(console.main)
    assert result.exit_code == 1
    assert "Boom" == str(result.exception)


def test_main_prints_message_on_request_error(runner, mock_requests_get):
    mock_requests_get.side_effect = requests.RequestException
    result = runner.invoke(console.main)
    assert "Error" in result.output
