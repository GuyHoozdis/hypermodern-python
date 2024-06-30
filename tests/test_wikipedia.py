"""Test cases for the wikipedia module."""

from unittest import mock

import click
import pytest
import requests

from hypermodern_python import wikipedia


def test_random_page_uses_given_language(mock_requests_get: mock.Mock) -> None:
    """It selects the specified Wikipedia language edition."""
    language = "de"
    wikipedia.random_page(language=language)
    url = wikipedia.get_api_url_for(language=language)
    mock_requests_get.assert_called_once_with(url, timeout=mock.ANY)


def test_random_page_returns_page(mock_requests_get: mock.Mock) -> None:
    """It returns an object of type Page."""
    page = wikipedia.random_page()
    assert isinstance(page, wikipedia.Page)


def test_random_page_handles_validation_errors(mock_requests_get: mock.Mock) -> None:
    """It raises `ClickException` when validation fails."""
    mock_requests_get.return_value.__enter__.return_value.json.return_value = None
    with pytest.raises(click.ClickException):
        wikipedia.random_page()


# XXX: For demonstration purposes.
# def test_trigger_typeguard(mock_requests_get):
#     import json
#     data = json.loads('{ "language": 1 }')
#     wikipedia.random_page(language=data["language"])
