import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    """Common reusable actions shared by all pages."""

    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, 10)

    def open(self, path=""):
        """Open a page by relative path."""
        self.driver.get(f"{self.base_url}{path}")

    def find(self, locator):
        """Wait until the element becomes visible and return it."""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def click(self, locator):
        element = self.find(locator)

        # highlight element
        self.driver.execute_script("arguments[0].style.border='3px solid red'", element)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        time.sleep(1)
        element.click()
        time.sleep(1)

    def type(self, locator, text):
        """Type into a field safely."""
        self.find(locator).send_keys(text)
