from .conftest import page, test_user, url

def login(page):
    page.goto(url + "login/")
    page.fill("input[name='username']", "testuser")
    page.fill("input[name='password']", "testpassword")
    page.click("button[type='submit']")

def test_clear_all(page):

    login(page)

    clear_button = page.locator("button[value='clear_all_incomes']")

    page.wait_for_load_state("networkidle")
    assert page.url == url

def test_income_submit(page):
    login(page)