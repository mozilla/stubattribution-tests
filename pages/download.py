from pypom import Page
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as expected


class Download(Page):

    _download_button_locator = (By.ID, 'download-button-desktop-release')
    _download_link_locator = (By.ID, 'direct-download-link')

    def wait_for_page_to_load(self):
        self.wait.until(expected.element_to_be_clickable(
            self._download_button_locator))

    def click_download(self):
        self.find_element(*self._download_button_locator).click()

    @property
    def download_link_location(self):
        el = self.find_element(*self._download_link_locator)
        return el.get_attribute('href')
