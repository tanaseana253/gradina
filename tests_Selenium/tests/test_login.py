def test_valid_login(login_page):
    login_page.open_login()
    login_page.login("tanase.ana253@gmail.com", "americandream2808")
    assert "gradina-craciun" in login_page.driver.current_url


def test_invalid_login(login_page):
    login_page.open_login()
    login_page.login("wrong@example.com", "incorrect-password")

    error = login_page.get_error()
    assert "Autentificarea a eșuat" in error
