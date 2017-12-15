from pypom import Page
from selenium.webdriver.common.by import By


class Firefox(Page):

    _download_button_locator = (By.ID, 'download-intro')

    def click_download(self):
        els = self.find_elements(*self._download_button_locator)
        next(el for el in els if el.is_displayed()).click()
        from pages.download import Download
        return Download(self.selenium, self.base_url).wait_for_page_to_load()
