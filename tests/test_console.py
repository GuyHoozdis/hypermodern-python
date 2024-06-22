import click.testing
import pytest

from hypermodern_python import console


@pytest.fixture
def runner():
    return click.testing.CliRunner()


@pytest.fixture
def mock_reqeusts_get(mocker):
    mock = mocker.patch("requests.get")
    mock.return_value.__enter__.return_value.json.return_value = {
        "title": "Guy Hoozdis",
        "extract": "Who is this guy?",
    }
    return mock


def test_main_succeeds(runner, mock_reqeusts_get):
    result = runner.invoke(console.main)
    assert result.exit_code == 0


def test_main_prints_title(runner, mock_reqeusts_get):
    result = runner.invoke(console.main)
    assert "Guy Hoozdis" in result.output


def test_main_invokes_requests_get(runner, mock_reqeusts_get):
    result = runner.invoke(console.main)
    assert mock_reqeusts_get.called
