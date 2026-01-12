import pytest
import os
from playwright.sync_api import sync_playwright
from django.contrib.auth.models import User

url = "http://127.0.0.1:8000/"
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

@pytest.fixture(scope="session")
def test_user(django_db_setup, django_db_blocker):
    # Those parameteres create user before Playwright event loop
    with django_db_blocker.unblock():
        return User.objects.create_user(
            username="testuser",
            password="testpassword"
        )

@pytest.fixture(scope="session")
def browser(test_user):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()

@pytest.fixture
def page(browser):
    page = browser.new_page()
    yield page
    page.close()

