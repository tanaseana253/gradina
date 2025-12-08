import sys, os

# Compute root of Jenkins workspace: .../gradina-pipeline
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

# Add project root to Python path
sys.path.insert(0, PROJECT_ROOT)

print("PYTHONPATH FIX APPLIED:", PROJECT_ROOT)


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


@pytest.fixture(scope="session", autouse=True)
def ensure_stock(db):
    from store.models import Product
    # Ensure all products have stock for Selenium tests
    for product in Product.objects.all():
        product.stock = 10
        product.save()
