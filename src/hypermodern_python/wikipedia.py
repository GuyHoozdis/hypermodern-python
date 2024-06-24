from typing import Any

import click
import requests


API_URL: str = "https://{language}.wikipedia.org/api/rest_v1/page/random/summary"


def get_api_url_for(language: str) -> str:
    return API_URL.format(language=language)


def random_page(language: str = "en") -> Any:
    url = get_api_url_for(language=language)
    try:
        with requests.get(url, timeout=10) as response:
            response.raise_for_status()
            return response.json()
    except requests.RequestException as error:
        message = str(error)
        raise click.ClickException(message) from error
