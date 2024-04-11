import re
from flask import Flask, request
from playwright.sync_api import Playwright, sync_playwright, expect

app = Flask(__name__)

def run_playwright(playwright: Playwright) -> str:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://e.khanbank.com/home")
    page.goto("https://e.khanbank.com/auth/login")

    page.get_by_placeholder("Нэвтрэх нэр").click()
    page.get_by_placeholder("Нэвтрэх нэр").fill("8809b")

    page.get_by_placeholder("Нууц үг").click()
    page.get_by_placeholder("Нууц үг").fill("611202Gd")

    page.get_by_label("Сануулах").check()
    page.get_by_role("button", name="Нэвтрэх").click()

    # Use regular expressions to extract the account number from the label text
    account_label = page.get_by_label("941****8").inner_text()
    account_number = re.search(r'\d+', account_label).group()
    print(f"Extracted account number: {account_number}")

    page.get_by_label(account_label).check()
    page.get_by_role("button", name="Үргэлжлүүлэх").click()

    page.get_by_placeholder("Нэг удаагийн нууц үгээ оруулна уу").click()
    page.get_by_placeholder("Нэг удаагийн нууц үгээ оруулна уу").fill("180590")

    page.get_by_label("Төхөөрөмж сануулах").check()
    page.get_by_role("button", name="Үргэлжлүүлэх").click()

    # Get the final page content
    final_content = page.content()

    context.close()
    browser.close()

    return final_content

@app.route('/scrape', methods=['POST'])
def scrape_website():
    print('hello')
    with sync_playwright() as playwright:
        final_content = run_playwright(playwright)
    return final_content

@app.route('/')
def home():
    return 'Flask is running!'

if __name__ == '__main__':
    app.run()