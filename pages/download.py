from pypom import Page
from selenium.webdriver.common.by import By


class Download(Page):

    _download_button_locator = (By.ID, 'download-button-desktop-release')
    _download_link_locator = (By.ID, 'direct-download-link')

    def click_download(self):
        self.find_element(*self._download_button_locator).click()

    @property
    def download_link_location(self):
        el = self.find_element(*self._download_link_locator)
        return el.get_attribute('href')
