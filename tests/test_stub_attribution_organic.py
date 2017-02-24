import urlparse

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import querystringsafe_base64


def generate_url(base_url):
    generated_url = '{base_url}/en-US/'.format(
        base_url)
    return generated_url


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


def assert_good(new_dict, source, medium, campaign, content):
    old_dict = {'source': source, 'medium': medium, 'campaign': campaign, 'content': content}
    print old_dict
    print new_dict
    assert new_dict == old_dict


@pytest.mark.parametriz('source, medium, campaign, content', [
    ('www.allizom.org', 'referral', '(not set)', '(not set)')])
def test_organic_flow_param_values(base_url, selenium, source, medium, campaign, content):
    # we:
    # 1. compare the values we expect from breaking out downloadLink in derive_url()
    # 2. ...to the utm_param_values we expect to see for source, medium, campaign, and content
    generated_url = generate_url(base_url)
    derived_url = derive_url(selenium, generated_url)
    new_dict = breakout_utm_param_values(derived_url)
    assert_good(new_dict, source, medium, campaign, content)
