"""Client for the Wikipedia REST API, version 1."""

from dataclasses import dataclass

import click
import desert
import marshmallow
import requests


API_URL: str = "https://{language}.wikipedia.org/api/rest_v1/page/random/summary"


@dataclass
class Page:
    """Page resource.

    Attributes:
        title: The title of the Wikipedia page article.
        extract: A plain text summary.
    """

    title: str
    extract: str


schema = desert.schema(Page, meta={"unknown": marshmallow.EXCLUDE})


def get_api_url_for(language: str) -> str:
    """Return the url.

    Formats the Wikipedia API url to include the language subdomain.  Wikipedia supports language
    codes defined in ISO 693-1 and ISO 693-3.  This function does not validate the input is a
    legitimate value - it only constructs the URL using the value provided.

    Args:
        language: The Wikipedia language edition.

    Returns:
        A URL to the Wikipedia API.

    Example:
        >>> from hypermodern_guyhoozdis import wikipedia
        >>> from urllib.parse import urlparse
        >>> language = "de"
        >>> url = wikipedia.get_api_url_for(language)
        >>> isinstance(url, str)
        True
        >>> parsed_url = urlparse(url)
        >>> parsed_url.netloc.startswith(language)
        True
    """
    return API_URL.format(language=language)


# TODO: Use the locale module to detect the language configured on the user's system.
def random_page(language: str = "en") -> Page:
    """Return a random page.

    Performs a GET request to the /page/random/summary endpoint.

    Args:
        language: The Wikipedia language edition.  By default, the English
            Wikipedia is used ("en").

    Returns:
        A page resource.

    Raises:
        ClickException: The HTTP request failed or the HTTP response contained an invalid body.

    Example:
        >>> from hypermodern_guyhoozdis import wikipedia
        >>> page = wikipedia.random_page(language="en")
        >>> bool(page.title)
        True
    """
    url = get_api_url_for(language=language)
    try:
        with requests.get(url, timeout=10) as response:
            response.raise_for_status()
            data = response.json()
            return schema.load(data)
    except (requests.RequestException, marshmallow.ValidationError) as error:
        message = str(error)
        raise click.ClickException(message) from error
