import time
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


def test_quantity_increase_and_decrease(product_list_page):
    product_list_page.open_store()

    # click "+" → quantity = 1
    product_list_page.add_first_in_stock()
    time.sleep(2)
    assert product_list_page.get_quantity() == 1

    # click "+" again → quantity = 2
    product_list_page.add_first_in_stock()
    time.sleep(2)
    assert product_list_page.get_quantity() == 2

    # click "-" → quantity = 1
    product_list_page.decrease_first_in_stock()
    time.sleep(2)
    assert product_list_page.get_quantity() == 1
