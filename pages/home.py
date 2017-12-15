from pypom import Page
from selenium.webdriver.common.by import By


class Home(Page):

    _firefox_locator = (By.CSS_SELECTOR, 'a[data-link-type=nav][data-link-name=Firefox]')

    def open_firefox(self):
        self.find_element(*self._firefox_locator).click()
        from pages.firefox import Firefox
        return Firefox(self.selenium, self.base_url).wait_for_page_to_load()
