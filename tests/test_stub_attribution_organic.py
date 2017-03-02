import urlparse

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import querystringsafe_base64


def derive_url(selenium, generated_url):
    selenium.get(generated_url)

    getFirefoxTodayLink = WebDriverWait(selenium, 10).until(
        EC.element_to_be_clickable((By.ID, "fx-download-link")))
    getFirefoxTodayLink.click()
    downloadButton = WebDriverWait(selenium, 10).until(
        EC.element_to_be_clickable((By.ID, "download-button-desktop-release")))
    downloadButton.click()
    downloadLink = selenium.find_element_by_id("direct-download-link").get_attribute("href")
    print "Stub Attribution download link is:\n %s" % downloadLink

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
    del equal_pieces_as_dict['timestamp']

    return equal_pieces_as_dict


@pytest.mark.nondestructive
def test_organic_flow_param_values(base_url, selenium):
    # we:
    # 1. compare the values we expect from breaking out downloadLink in derive_url()
    # 2. ...to the utm_param_values we expect to see for source, medium, campaign, and content
    derived_url = derive_url(selenium, '{0}/en-US/'.format(base_url))
    source = urlparse.urlparse(base_url).hostname
    medium = 'referral'
    campaign = '(not set)'
    content = '(not set)'
    actual = breakout_utm_param_values(derived_url)

    assert actual == {'source': source, 'medium': medium, 'campaign': campaign, 'content': content}
