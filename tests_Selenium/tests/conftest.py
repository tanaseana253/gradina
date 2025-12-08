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