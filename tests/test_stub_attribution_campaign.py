import urlparse

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import querystringsafe_base64


def generate_url(base_url, source, medium, campaign, term):
    generated_url = '{base_url}/en-US/firefox/new/?utm_source={}&utm_medium={}&utm_campaign={}&utm_term={}'.format(
        base_url, source, medium, campaign, term)
    return generated_url


def derive_url(selenium, generated_url):
    selenium.get(generated_url)

    downloadButton = WebDriverWait(selenium, 10).until(
        EC.element_to_be_clickable((By.ID, "download-button-desktop-release")))
    downloadButton.click()
    downloadLink = selenium.find_element_by_id("direct-download-link").get_attribute("href")
    print('Stub Attribution download link is:\n{}'.format(downloadLink))

    return downloadLink


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
    del equal_pieces_as_dict['content']
    del equal_pieces_as_dict['timestamp']

    return equal_pieces_as_dict


def assert_good(new_dict, source, medium, campaign, term):
    old_dict = {'source': source, 'medium': medium, 'campaign': campaign, 'term': term}
    del old_dict['term']
    print(old_dict)
    print(new_dict)
    assert new_dict == old_dict


@pytest.mark.nondestructive
@pytest.mark.parametrize('source, medium, campaign, term', [
    ('google', 'paidsearch', 'Fake%20campaign', 'test term')])
def test_campaign_flow_param_values(base_url, selenium, source, medium, campaign, term):
    # here, we build our "generated" (i.e. expected) URL from our utm_* parameter values
    generated_url = '{base_url}/en-US/firefox/new/?utm_source={source}&utm_medium={medium}&utm_campaign={campaign}&utm_term={term}'.format(
        base_url=base_url,
        source=source,
        medium=medium,
        campaign=campaign,
        term=term)
    derived_url = derive_url(selenium, generated_url)
    new_dict = breakout_utm_param_values(derived_url)
    assert_good(new_dict, source, medium, campaign, term)
