import os
import urlparse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import querystringsafe_base64


desired_cap = {
    'platform': "Windows 10",
    'browserName': "chrome",
    'version': "54.0"
}


username = os.environ["SAUCE_USERNAME"]
key = os.environ["SAUCE_ACCESS_KEY"]
sauce_creds = ':'.join([username, key])


driver = webdriver.Remote(
    command_executor='http://%s@ondemand.saucelabs.com:80/wd/hub' % sauce_creds,
    desired_capabilities=desired_cap)


def generate_url():
    base_url = 'www.allizom.org'
    generated_url = "https://{}/en-US/".format(
        base_url)
    return generated_url


def derive_url(generated_url):
    driver.get(generated_url)

    getFirefoxTodayLink = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "fx-download-link")))
    getFirefoxTodayLink.click()
    downloadButton = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "download-button-desktop-release")))
    downloadButton.click()
    downloadLink = driver.find_element_by_id("direct-download-link").get_attribute("href")
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


def test_organic_flow_param_values(source, medium, campaign, content):
    # we:
    # 1. compare the values we expect from breaking out downloadLink in derive_url()
    # 2. ...to the utm_param_values we expect to see for source, medium, campaign, and content
    generated_url = generate_url()
    derived_url = derive_url(generated_url)
    new_dict = breakout_utm_param_values(derived_url)
    assert_good(new_dict, source, medium, campaign, content)


test_organic_flow_param_values("www-demo4.allizom.org", "referral", "(not set)", "(not set)")


driver.quit()
