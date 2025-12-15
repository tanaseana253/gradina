import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pytest

from tests_Selenium.pages.login_page import LoginPage
from tests_Selenium.pages.product_list_page import ProductListPage

# --------------------------
# Global test URL
# --------------------------
BASE_URL = "https://gradina-craciun-668739da08cd.herokuapp.com"


@pytest.fixture
def driver():
    options = Options()

    # Run headless only when Jenkins sets the env variable
    if os.getenv("SELENIUM_HEADLESS") == "1":
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture
def login_page(driver):
    return LoginPage(driver, BASE_URL)


@pytest.fixture
def product_list_page(driver):
    return ProductListPage(driver, BASE_URL)
