from hypermodern_python import wikipedia


def test_random_page_uses_given_language(mock_requests_get):
    language = 'de'
    wikipedia.random_page(language=language)
    url = wikipedia.get_api_url_for(language=language)
    mock_requests_get.assert_called_once_with(url)
