from .imports import page, local_url

def test_auth_page_loads(page):
    page.goto(local_url + "login/")
    assert page.title() != ""