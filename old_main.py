from fastapi import FastAPI
from pydantic import BaseModel
from playwright.sync_api import sync_playwright
from time import sleep
import json
import os

app = FastAPI()
browser = None
context = None
page = None

class LoginRequest(BaseModel):
    username: str
    password: str

class OTPRequest(BaseModel):
    code: str

@app.post('/login')
def login(request: LoginRequest):
    global browser, context, page
    _username = request.username.lower()
    _password = request.password

    if not browser:
        p = sync_playwright().start()
        browser = p.firefox.launch(headless=False) 

    if not context:
        # Check if context exists
        if os.path.exists('context.json'):
            # Load context from the file
            with open('context.json', 'r') as f:
                context_state = json.load(f)
            context = browser.new_context(storage_state=context_state)
        else:
            context = browser.new_context()

    page = context.new_page()
    api_request_context = context.request

    
    # Listen for the API response
    def handle_response(response):
        if response.url == 'https://e.khanbank.com/v1/cfrm/auth/token?grant_type=client_credentials&channelId=I&languageId=003' \
                or 'https://e.khanbank.com/v1/omni/user/custom/operativeaccounts/5429348172/transactions' in response.url:
            
            print('API Response: --------------------------------------------')
            print(response.url)
            print(response.json())


    # page.on('request', handle_request)
    page.on('response', handle_response)

    # Check if already logged in
    page.goto('https://e.khanbank.com/')
    if page.url == 'https://e.khanbank.com/':
        return {'message': 'Already logged in'}
    else:
        login_khan(page, _username, _password)
        if os.path.exists('context.json'):
    
            sleep(3)
            page.get_by_role("complementary").get_by_role("link", name=" Данс").click()
            page.click("//a[contains(@class, 'ctrl-btn') and .//span[text()='Хуулга']]")
            sleep(5)
            page.locator("div.statement-list-header-control a").first.click()

            context_state = context.storage_state()
            with open('context.json', 'w') as f:
                json.dump(context_state, f)

            page.close()
            browser.close()
            return {'message': 'Logged in successfully'}

@app.post('/sms')
def sms(request: OTPRequest):
    global context, page
    code = request.code
    # sleep(5)
    # enter_otp(page, code)

    page.fill('#otp', code)
    page.check("input[type='checkbox']")
    page.click("//span[text()='Үргэлжлүүлэх']")

    # Save context to a file after filling the OTP
    context_state = context.storage_state()
    with open('context.json', 'w') as f:
        json.dump(context_state, f)
    
    page.close()

    return {'message': 'OTP entered successfully'}

def login_khan(page, _username, _password):
    page.goto('https://e.khanbank.com/auth/login')
    page.fill('#username', _username)
    page.fill('#password', _password)
    page.click("//button[contains(@class,'ant-btn ant-btn-primary')]")
    
    if not os.path.exists('context.json'):
        sleep(3)
        page.click("//span[@class='ant-radio']/following-sibling::span")
        sleep(3)
        page.click("//span[text()='Үргэлжлүүлэх']")
    return True

def enter_otp(page, code):
    page.fill('#otp', code)
    page.check("input[type='checkbox']")
    page.click("//span[text()='Үргэлжлүүлэх']")

@app.on_event('shutdown')
def close_browser():
    global browser
    if browser:
        browser.close()
        browser = None

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)