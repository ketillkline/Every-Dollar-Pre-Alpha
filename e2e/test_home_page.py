from .conftest import page, test_user, url

def test_clear_all_no_crash(page):

    page.goto(url + "login/")
    page.fill("input[name='username']", "testuser")
    page.fill("input[name='password']", "testpassword")
    page.click("button[type='submit']")

    clear_button = page.locator("button[value='clear_all_incomes']")

    assert clear_button.is_visible()