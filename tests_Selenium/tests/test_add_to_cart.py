from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


def test_add_to_cart(product_list_page):
    product_list_page.open_store()
    product_list_page.add_first_in_stock()

    # Wait for ANY quantity span to become visible with text "1"
    quantity_selector = (By.CSS_SELECTOR, "span[id^='quantity-']")

    element = product_list_page.wait.until(
        EC.text_to_be_present_in_element(quantity_selector, "1")
    )

    assert element is True
