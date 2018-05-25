import urlparse

import pytest
import querystringsafe_base64

from pages.download import Download


def breakout_utm_param_values(generated_url):
    parts = urlparse.urlparse(generated_url)
    scheme, netloc, path, params, query, fragment = parts

    key_value_dict = urlparse.parse_qs(query)

    # The thing is an array -- I don't know why. But there's only one element, so
    # just pick the first item off (ie ...[0])
    attribution_code = key_value_dict['attribution_code'][0].encode('utf-8')
    attribution_code = querystringsafe_base64.decode(attribution_code)

    # split on '&', into an array
    equal_pieces = attribution_code.split('&')

    # Now split up the bunch of strings with 'a=b' in them, into tuples, of (a, b)
    equal_pieces_as_dict = {}
    for equal_piece in equal_pieces:
        key, value = equal_piece.split('=')
        equal_pieces_as_dict[key] = value
    del equal_pieces_as_dict['content']
    del equal_pieces_as_dict['timestamp']

    return equal_pieces_as_dict


def assert_good(new_dict, source, medium, campaign, term):
    old_dict = {'source': source, 'medium': medium, 'campaign': campaign, 'term': term}
    del old_dict['term']
    assert new_dict == old_dict


@pytest.mark.nondestructive
@pytest.mark.parametrize('source, medium, campaign, term', [
    ('google', 'paidsearch', 'Brand-US-GGL-Exact', 'download%20firefox')])
def test_search_flow_param_values(base_url, selenium, source, medium, campaign, term):
    generated_url = '{base_url}/en-US/firefox/new/?utm_source={source}&utm_medium={medium}&utm_campaign={campaign}&utm_term={term}'.format(
        base_url=base_url,
        source=source,
        medium=medium,
        campaign=campaign,
        term=term)
    selenium.get(generated_url)
    page = Download(selenium)
    page.click_download()
    derived_url = page.download_link_location
    new_dict = breakout_utm_param_values(derived_url)
    assert_good(new_dict, source, medium, campaign, term)
