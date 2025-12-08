from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .base_page import BasePage


class ProductListPage(BasePage):
    FIRST_IN_STOCK_ADD = (By.CSS_SELECTOR, "button[id^='increment-btn']")
    FIRST_DECREMENT = (By.CSS_SELECTOR, "button[id^='decrement-btn']")
    FIRST_QUANTITY = (By.CSS_SELECTOR, "span[id^='quantity-']")

    def open_store(self):
        self.open("/store/")

    def add_first_in_stock(self):
        btn = self.driver.find_element(By.CSS_SELECTOR, ".add-to-cart-btn")

        # Scroll the button into view (centered avoids navbars)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)

        # Wait until Selenium thinks it's clickable
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".add-to-cart-btn"))
        )

        # Try normal click, fallback to JS click if intercepted
        try:
            btn.click()
        except:
            # Guaranteed click (bypasses overlays, works in Jenkins)
            self.driver.execute_script("arguments[0].click();", btn)

    def decrease_first_in_stock(self):
        btn = self.find(self.FIRST_DECREMENT)
        btn.click()

    def get_quantity(self):
        quantity_el = self.find(self.FIRST_QUANTITY)
        return int(quantity_el.text.strip())
