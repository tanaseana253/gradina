from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .base_page import BasePage


class ProductListPage(BasePage):

    # -------------------------------
    # LOCATORS
    # -------------------------------

    IN_STOCK_CHECKBOX = (By.ID, "filtru_in_stoc")
    IN_STOCK_LABEL = (By.CSS_SELECTOR, "label[for='filtru_in_stoc']")

    PRODUCT_CARD = (By.CSS_SELECTOR, ".card-enabled-gc")
    STOCK_VALUE = (By.CSS_SELECTOR, ".product-stock")

    # Favorite locators
    FAVORITE_CHECKBOX = (By.ID, "filtru_favorite")
    FAVORITE_LABEL = (By.CSS_SELECTOR, "label[for='filtru_favorite']")
    FAVORITE_ICON = (By.CSS_SELECTOR, ".icon-favorite-selected")

    # -------------------------------
    # NAVIGATION
    # -------------------------------

    def open_store(self):
        self.open("/store/")

    # -------------------------------
    # IN-STOCK FILTER
    # -------------------------------

    def click_in_stock_filter(self):
        label = self.wait.until(EC.element_to_be_clickable(self.IN_STOCK_LABEL))
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", label
        )
        label.click()

    # -------------------------------
    # FAVORITE FILTER
    # -------------------------------

    def click_favorite_filter(self):
        """Clicks the 'Favorite' filter checkbox (only visible for logged-in users)."""
        label = self.wait.until(EC.element_to_be_clickable(self.FAVORITE_LABEL))
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", label
        )
        label.click()

    def is_favorited(self, product_card):
        """Returns True if a product card contains the filled-heart icon."""
        return len(product_card.find_elements(*self.FAVORITE_ICON)) > 0

    # -------------------------------
    # PRODUCT VISIBILITY + STOCK
    # -------------------------------

    def get_visible_products(self):
        all_cards = self.find_elements(self.PRODUCT_CARD)
        return [c for c in all_cards if c.is_displayed()]

    def get_stock_value(self, product):
        text = product.find_element(*self.STOCK_VALUE).get_attribute("textContent")
        return int(text.strip())
