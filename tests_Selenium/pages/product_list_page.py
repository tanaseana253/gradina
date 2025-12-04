from selenium.webdriver.common.by import By
from .base_page import BasePage


class ProductListPage(BasePage):
    FIRST_IN_STOCK_ADD = (By.CSS_SELECTOR, "button[id^='increment-btn']")
    FIRST_DECREMENT = (By.CSS_SELECTOR, "button[id^='decrement-btn']")
    FIRST_QUANTITY = (By.CSS_SELECTOR, "span[id^='quantity-']")

    def open_store(self):
        self.open("/store/")

    def add_first_in_stock(self):
        btn = self.find(self.FIRST_IN_STOCK_ADD)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", btn)
        btn.click()

    def decrease_first_in_stock(self):
        btn = self.find(self.FIRST_DECREMENT)
        btn.click()

    def get_quantity(self):
        quantity_el = self.find(self.FIRST_QUANTITY)
        return int(quantity_el.text.strip())
