from dataclasses import dataclass
from typing import Any

import click
import desert
import marshmallow
import requests


API_URL: str = "https://{language}.wikipedia.org/api/rest_v1/page/random/summary"


@dataclass
class Page:
    title: str
    extract: str


schema = desert.schema(Page, meta={"unknown": marshmallow.EXCLUDE})


def get_api_url_for(language: str) -> str:
    return API_URL.format(language=language)


def random_page(language: str = "en") -> Page:
    url = get_api_url_for(language=language)
    try:
        with requests.get(url, timeout=10) as response:
            response.raise_for_status()
            data = response.json()
            return schema.load(data)
    except requests.RequestException as error:
        message = str(error)
        raise click.ClickException(message) from error
