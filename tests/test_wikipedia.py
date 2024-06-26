from unittest import mock

import click
import pytest
import requests

from hypermodern_python import wikipedia


def test_random_page_raises_click_exception_on_requests_error(
    mock_requests_get: mock.Mock,
) -> None:
    mock_requests_get.side_effect = requests.RequestException
    with pytest.raises(click.ClickException):
        wikipedia.random_page()


def test_random_page_uses_given_language(mock_requests_get: mock.Mock) -> None:
    language = "de"
    wikipedia.random_page(language=language)
    url = wikipedia.get_api_url_for(language=language)
    mock_requests_get.assert_called_once_with(url, timeout=mock.ANY)


def test_random_page_returns_page(mock_requests_get: mock.Mock) -> None:
    page = wikipedia.random_page()
    assert isinstance(page, wikipedia.Page)


def test_random_page_handles_validation_errors(mock_requests_get: mock.Mock) -> None:
    mock_requests_get.return_value.__enter__.return_value.json.return_value = None
    with pytest.raises(click.ClickException):
        wikipedia.random_page()


# XXX: For demonstration purposes.
# def test_trigger_typeguard(mock_requests_get):
#     import json
#     data = json.loads('{ "language": 1 }')
#     wikipedia.random_page(language=data["language"])
