from .conftest import page, test_user, url

def test_clear_all_no_crash(page):
    page.goto(url)

    page.click("button[value='clear_all_incomes']")
    page.wait_for_load_state("networkidle", timeout=5000)


    assert page.url == url