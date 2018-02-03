-*- coding: utf-8 -*-

import urlparse

import pytest
import querystringsafe_base64

from pages.home import Home


def breakout_utm_param_values(generated_url):
    parts = urlparse.urlparse(generated_url)
    scheme, netloc, path, params, query, fragment = parts

    key_value_dict = urlparse.parse_qs(query)

    # The thing is an array -- I don't know why. But there's only one element, so
    # just pick the first item off (ie ...[0])
    attribution_code = key_value_dict['attribution_code'][0]
    attribution_code = querystringsafe_base64.decode(attribution_code)

    # split on '&', into an array
    equal_pieces = attribution_code.split('&')

    # Now split up the bunch of strings with 'a=b' in them, into tuples, of (a, b)
    equal_pieces_as_dict = {}
    for equal_piece in equal_pieces:
        key, value = equal_piece.split('=')
        equal_pieces_as_dict[key] = value
    del equal_pieces_as_dict['timestamp']

    return equal_pieces_as_dict


@pytest.mark.nondestructive
def test_organic_flow_param_values(base_url, selenium):
    # we:
    # 1. compare the values we expect from breaking out downloadLink in derive_url()
    # 2. ...to the utm_param_values we expect to see for source, medium, campaign, and content
    page = Home(selenium, base_url).open().open_firefox()
    derived_url = page.click_download().download_link_location
    expected = {
        'source': urlparse.urlparse(base_url).hostname,
        'medium': 'referral',
        'campaign': '(not set)',
        'content': '(not set)'}
    actual = breakout_utm_param_values(derived_url)

    assert actual == expected
