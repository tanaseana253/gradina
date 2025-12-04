from selenium.webdriver.common.by import By
from .base_page import BasePage


class LoginPage(BasePage):
    # Correct locators from your HTML template
    USERNAME = (By.ID, "exampleInputEmail1")
    PASSWORD = (By.ID, "exampleInputPassword1")
    SUBMIT = (By.CSS_SELECTOR, "form.login-form-primary button.gc-cta")

    def open_login(self):
        self.open("/store/login/")

    def login(self, username, password):
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)
        self.click(self.SUBMIT)

    def get_error(self):
        try:
            return self.find((By.CSS_SELECTOR, ".error-message")).text
        except:
            return None
