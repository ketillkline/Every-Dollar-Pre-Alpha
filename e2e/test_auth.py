from .conftest import page, test_user, url

def test_auth_page_loads(page, live_server):
    page.goto(url + "login/")
    assert page.title() != ""

def test_login_form_exists(page, live_server):
    page.goto(url + "login/")

    assert page.locator("input[name='username']").is_visible()
    assert page.locator("input[name='password']").is_visible()
    assert page.locator("button[type='submit']").is_visible()

def test_login_success(page, test_user, live_server):
    page.goto(url + "login/")

    page.fill("input[name='username']", "testuser")
    page.fill("input[name='password']", "testpassword")
    page.click("button[type='submit']")

    page.wait_for_url(url, timeout=5000)

    assert "login" not in page.url

def test_wrong_credentials(page, test_user):
    page.goto(url + "login/")

    page.fill("input[name='username']", "testuser")
    page.fill("input[name='password']", "wrongpassword")
    page.click("button[type='submit']")

    assert "login" in page.url



