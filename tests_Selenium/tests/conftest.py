import sys, os

# Absolute path to the folder containing manage.py
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

# If Jenkins workspace has another root level, fix it:
if not os.path.exists(os.path.join(PROJECT_ROOT, "manage.py")):
    PROJECT_ROOT = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "..")
    )

sys.path.insert(0, PROJECT_ROOT)

print(">>> PYTHONPATH SET TO:", PROJECT_ROOT)


import warnings
import pytest
from selenium import webdriver
from tests_Selenium.pages.login_page import LoginPage
from tests_Selenium.pages.product_list_page import ProductListPage

BASE_URL = "https://gradina-craciun-668739da08cd.herokuapp.com"
warnings.filterwarnings("ignore", category=DeprecationWarning, module="pkg_resources")


@pytest.fixture
def driver():
    driver = webdriver.Chrome()  # start Chrome
    driver.maximize_window()
    yield driver
    driver.quit()  # close Chrome after test


@pytest.fixture
def login_page(driver):
    return LoginPage(driver, BASE_URL)


@pytest.fixture
def product_list_page(driver):
    return ProductListPage(driver, BASE_URL)


@pytest.fixture(scope="function", autouse=True)
def ensure_stock(db):
    from store.models import Product
    for product in Product.objects.all():
        product.stock = 10
        product.save()

