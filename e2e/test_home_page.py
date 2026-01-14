from .conftest import page, test_user, url


buttons = {
    "add_new_bill": "button[value='add_income']",
    "clear_all": "button[value='clear_all_incomes']",
    "cancel": "button[class='cancel-bill']",
    "save": "button[value='add_bill']",
    "add_income": "button[value='add_income']"
}

inputs = {
    "new_bill_name": "input[name='bill_name']",
    "new_bill_amount": "input[name='bill_amount']",
    "new_bill_payday": "input[name='bill_pay_day']",
    "paycheck": "input[name='paycheck']",
    "start_date": "input[name='start_date']",
    "end_date": "input[name='end_date']",
    "edit_bill_name": "input[name='edited_bill_name']",
    "edit_bill_amount": "input[name='edited_bill_amount']",
    "edit_bill_payday": "input[name='edited_bill_payday']"

}

def login(page):
    page.goto(url + "login/")
    page.fill("input[name='username']", "testuser")
    page.fill("input[name='password']", "testpassword")
    page.click("button[type='submit']")

def test_clear_all(page):

    login(page)

    clear_button = page.locator(buttons.get("clear_all"))
    clear_button.click()

    page.wait_for_load_state("networkidle")
    assert page.url == url

def test_income_submit(page):
    login(page)

    page.fill(inputs.get("paycheck"), "700")
    page.fill(inputs.get("start_date"), "2030-01-12")
    page.fill(inputs.get("end_date"), "2030-01-26")

    page.click(buttons.get("add_income"))

    assert page.url == url
'''

TODO: Finish tests

def test_add_bill(page):
    login(page)

    page.click(buttons["add_new_bill"])

    assert page.locator(inputs["new_bill_name"]).is_visible()
    assert page.locator(inputs["new_bill_amount"]).is_visible()
    assert page.locator(inputs["new_bill_payday"]).is_visible()



def test_add_bill_missing_field(page):
    login(page)

    assert page.locator(buttons["add_new_bill"])
    assert page.locator(buttons["save"]).is_visible()
    assert page.locator(buttons["cancel"]).is_visible()


def test_cancel(page):
    login(page)

    assert page.locator(buttons.get("add_new_bill")).is_visible()

'''
