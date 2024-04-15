import psycopg2
from psycopg2 import Error
from playwright.sync_api import sync_playwright
from time import sleep
import json
import os
from models.token import Transaction
from database import get_db
from pprint import pprint
from datetime import datetime

from sqlalchemy.exc import OperationalError

connection = psycopg2.connect(
    host=os.getenv('db_host'),
    port="5432",
    database=os.getenv('db_database'),
    user=os.getenv('db_user'),
    password=os.getenv('db_password')
)

KHAN_ACCOUNT = os.getenv('KHAN_ACCOUNT')

def handle_response(response):
    if f'https://e.khanbank.com/v1/omni/user/custom/operativeaccounts/{KHAN_ACCOUNT}/transactions' in response.url:
        print('API Response: --------------------------------------------')
        print(response.url)

        max_retries = 3
        retry_delay = 1

        for retry in range(max_retries):
            try:
                # Establish a new database connection for each retry
                cursor = connection.cursor()

                for row in response.json():
                    pprint(row)
                    transaction_date = row['transactionDate']
                    account_id = row.get('accountId', None)
                    amount_type = row['amountType']['codeDescription']
                    amount = row['amount']['amount']
                    transaction_remarks = row['transactionRemarks']
                    txn_time = datetime.strptime(row['txnTime'], "%H:%M").time()
                    begin_balance = row['beginBalance']['amount']
                    end_balance = row['endBalance']['amount']

                    # Check if the transaction already exists in the database
                    check_query = """
                        SELECT COUNT(*) FROM transactions
                        WHERE transaction_date = %s AND transaction_remarks = %s AND amount = %s AND txn_time = %s AND begin_balance = %s
                    """
                    cursor.execute(check_query, (transaction_date, transaction_remarks, amount, txn_time, begin_balance))
                    count = cursor.fetchone()[0]

                    if count == 0:
                        # Insert the transaction data into the database if it doesn't exist
                        insert_query = """
                            INSERT INTO transactions (
                                transaction_date, account_id, amount_type, amount,
                                transaction_remarks, txn_time, begin_balance, end_balance
                            )
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        """
                        cursor.execute(insert_query, (
                            transaction_date, account_id, amount_type, amount,
                            transaction_remarks, txn_time, begin_balance, end_balance
                        ))
                    else:
                        print("Transaction already exists. Skipping insertion.")

                connection.commit()
                break  # Break the retry loop if the commit is successful
            except psycopg2.OperationalError as e:
                print(f"Database error: {str(e)}")
                if retry < max_retries - 1:
                    print(f"Retrying in {retry_delay} seconds...")
                    connection.rollback()  # Rollback the transaction before retrying
                    sleep(retry_delay)
                else:
                    print("Max retries exceeded. Skipping the transaction.")
            except Exception as e:
                connection.rollback()
                raise e
            finally:
                cursor.close()
                connection.close()

            
def get_transaction_data(page):
    page.on('response', handle_response)
    
    page.goto('https://e.khanbank.com/auth/login')
    page.fill('#username', os.getenv('KHAN_USERNAME'))
    page.fill('#password', os.getenv('KHAN_PASSWORD'))
    page.click("//button[contains(@class,'ant-btn ant-btn-primary')]")
    
    page.wait_for_load_state("networkidle")
    page.get_by_role("complementary").get_by_role("link", name=" Данс").click()
    page.wait_for_load_state("networkidle")
    page.click("//a[contains(@class, 'ctrl-btn') and .//span[text()='Хуулга']]")
    page.wait_for_load_state("networkidle")
    sleep(5)
    
    for _ in range(3):
        try:
            page.locator("div.statement-list-header-control a").first.click()
            break
        except Exception as e:
            sleep(1) 

def main():
    # Check if context exists
    if not os.path.exists('context.json'):
        print("Context file not found. Please log in first.")
        return

    # Load context from the file
    with open('context.json', 'r') as f:
        context_state = json.load(f)

    # Start Playwright
    p = sync_playwright().start()
    browser = p.firefox.launch(headless=True)
    context = browser.new_context(storage_state=context_state)
    page = context.new_page()

    # Get transaction data
    get_transaction_data(page)

    # Close the browser and context
    page.close()
    browser.close()
    p.stop()

if __name__ == '__main__':
    main()