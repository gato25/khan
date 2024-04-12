import httpx
import json
import base64
from .models.token import Token, Transaction
import subprocess
import datetime
# from dateutil import parser
import traceback

url = "https://e.khanbank.com/v1/cfrm/auth/token"

headers = {
  'Accept': 'application/json, text/plain, */*',
  'Accept-Language': 'mn-MN',
  'Authorization': '',
  'Connection': 'keep-alive',
  'Content-Type': 'application/json',
  'Origin': 'https://e.khanbank.com',
  'Referer': 'https://e.khanbank.com/auth/login',
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'same-origin',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0',
  # 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_1_0; en-US) AppleWebKit/533.21 (KHTML, like Gecko) Chrome/48.0.3677.296 Safari/534',
  'app-version': '1.3.48-rc.718',
  'channelcontext': '',
  'sec-ch-ua': '"Microsoft Edge";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'secure': 'yes'
}

def get_otp(username, password):
  try:
    encoded_password = base64.b64encode(bytes(password, 'utf-8')).decode('utf-8')
    print(password,encoded_password)

    payload = json.dumps({
      "grant_type": "password",
      "username": username,
      "password": encoded_password,
      "channelId": "I",
      "languageId": "003"
    })

    response = httpx.post(url, data = payload, headers=headers)
    print(response.json())
    req_id = response.json()['unique_id']

    secondary_data = json.dumps({
        "grant_type": "password",
        "username": username,
        "password": encoded_password,
        "languageId": "mn",
        "channelId": "I",
        "isPrelogin": "N",
        "requestId": req_id,
        "secondaryMode": "SOTP"
    })

    secondary_response = httpx.post(url, data=secondary_data, headers=headers)
    print(secondary_response)
    return secondary_response.json()
  except Exception as e:
    print(e)
    traceback.print_exc()
    

def login(otp, req_id, username):
  try:
    encoded_password = base64.b64encode(bytes(otp, 'utf-8')).decode('utf-8')

    final_data = json.dumps({
        "grant_type": "password",
        "username": username,
        "password": encoded_password,
        "channelId": "I",
        "isPrelogin": "N",
        "requestId": req_id,
        "secondaryMode": "",
        "rememberDevice": "N"
    })
    
    print(final_data)

    final_response = httpx.post(url, data = final_data, headers=headers)
    print(final_response)
    return final_response.json()
  except Exception as e:
    print(e)
    traceback.print_exc()

def get_token(db):
  
  token = db.query(Token).order_by(Token.created_at.desc()).first()
    
  curl_command = [
    "curl",
    "--location",
    f"https://e.khanbank.com/v1/cfrm/auth/token?grant_type=refresh_token&refresh_token={token.refresh_token}",
    "--header", "Accept: application/json, text/plain, */*",
    "--header", "Accept-Language: mn-MN",
    "--header", "Authorization: Basic Vm00eHFtV1BaQks3Vm5UYjNRRXJZbjlJZkxoWmF6enI6dElJQkFsU09pVXIwclV5cA==",
    "--header", "Connection: keep-alive",
    "--header", "Content-Type: application/x-www-form-urlencoded",
    "--header", "Cookie: __ssds=2; __ssuzjsr2=a9be0cd8e; __uzmaj2=d0808813-b375-4037-aa28-1b2502fb7b8b; __uzmbj2=1712585575; _ga=GA1.1.829643620.1712585579; __uzma=2681e7e4-76e3-1b24-bc30-c6415ecb7466; __uzmb=1712585582; __uzme=3876; _ga_XY11GTD04T=GS1.1.1712585578.1.0.1712585591.47.0.0; SL_ClassKey=0.1.1; __uzmcj2=185825560972; __uzmdj2=1712766258; __uzmd=1712766601; __uzmc=1864890494732; __uzma=708c7feb-887e-f6fc-e90e-a379cc3c33af; __uzmb=1712591992; __uzmc=3327390758677; __uzmd=1712767576; __uzme=8751",
    "--header", "Origin: https://e.khanbank.com",
    "--header", "Referer: https://e.khanbank.com/account/statement/5429348172/MNT/OPR",
    "--header", "Sec-Fetch-Dest: empty",
    "--header", "Sec-Fetch-Mode: cors",
    "--header", "Sec-Fetch-Site: same-origin",
    "--header", "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0",
    "--header", "app-version: 1.3.48-rc.718",
    "--header", 'sec-ch-ua: "Microsoft Edge";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
    "--header", "sec-ch-ua-mobile: ?0",
    "--header", 'sec-ch-ua-platform: "Windows"',
    "--header", "secure: yes",
    "--data-urlencode", "{}="
  ]

  # Run the curl command
  try:
    result = subprocess.run(curl_command, capture_output=True, text=True, check=True)
    # print("Output:")
    print(result.stdout)
    response_token = json.loads(result.stdout)
    access_token = response_token['access_token']
    refresh_token = response_token['refresh_token']
    token = Token(access_token=access_token, refresh_token=refresh_token)
    db.add(token)
    db.commit()
    db.refresh(token)

  except subprocess.CalledProcessError as e:
      print("Error:")
      print(e)


def get_transaction(db):
  url = "https://e.khanbank.com/v1/omni/user/custom/operativeaccounts/5429348172/transactions?transactionValue=0&transactionDate=%7B%22lt%22:%222024-04-09T00:00:00%22,%22gt%22:%222024-04-11T00:00:00%22%7D&amount=%7B%22lt%22:%220%22,%22gt%22:%220%22%7D&amountType=&transactionCategoryId=&transactionRemarks=&customerName=%D0%94%D0%90%D0%9C%D0%91%D0%90+%D0%91%D0%90%D0%94%D0%90%D0%9C%D0%93%D0%90%D0%A0%D0%90%D0%92&transactionCurrency=MNT&branchCode=5029"
  get_token(db)
  token = db.query(Token).order_by(Token.created_at.desc()).first()
  
  payload = {}
  
  # curl_command = [
  #   'curl',
  #   '--location',
  #   'https://e.khanbank.com/v1/omni/user/custom/operativeaccounts/5429348172/transactions?transactionValue=0&transactionDate=%7B%22lt%22%3A%222024-04-08T00%3A00%3A00%22%2C%22gt%22%3A%222024-04-10T00%3A00%3A00%22%7D&amount=%7B%22lt%22%3A%220%22%2C%22gt%22%3A%220%22%7D&transactionCategoryId=&transactionRemarks=&customerName=%D0%94%D0%90%D0%9C%D0%91%D0%90%2B%D0%91%D0%90%D0%94%D0%90%D0%9C%D0%93%D0%90%D0%A0%D0%90%D0%92&transactionCurrency=MNT&branchCode=5029',
  #   '--header', 'Accept: application/json, text/plain, */*',
  #   '--header', 'Accept-Language: mn-MN',
  #   '--header', f'Authorization: Bearer {token.access_token}',
  #   '--header', 'Connection: keep-alive',
  #   '--header', 'Referer: https://e.khanbank.com/account/statement/5429348172/MNT/OPR',
  #   '--header', 'Sec-Fetch-Dest: empty',
  #   '--header', 'Sec-Fetch-Mode: cors',
  #   '--header', 'Sec-Fetch-Site: same-origin',
  #   '--header', 'Cookie: __uzma=708c7feb-887e-f6fc-e90e-a379cc3c33af; __uzmb=1712591992; __uzmc=2973691668650; __uzmd=1712847255; __uzme=8751'
  # ]

  # response = subprocess.run(curl_command, capture_output=True, text=True)
  # print(response.stdout)
  headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'mn-MN',
    'Authorization': f'Bearer {token.access_token}',
    'Connection': 'keep-alive',
    # 'Cookie': '_ga=GA1.1.491542904.1709608750; __ssds=2; __ssuzjsr2=a9be0cd8e; __uzmaj2=97f36607-bc79-4c5c-8a4d-df21677a36e2; __uzmbj2=1709608750; __uzma=2fd083d4-64e1-8a5f-089c-45515714c4f3; __uzmb=1712305789; __uzme=6444; SL_ClassKey=0.1.1; _ga_XY11GTD04T=GS1.1.1712799055.6.0.1712799055.60.0.0; __uzmcj2=572836129519; __uzmdj2=1712799059; __uzmd=1712799721; __uzmc=5993228911758; SL_ClassKey=0.1.1; __uzma=ff157351-6a7c-bc64-1a8a-d4bd27d5a592; __uzmb=1712799658; __uzmc=6214729287378; __uzmd=1712799852; __uzme=8043',
    'Referer': 'https://e.khanbank.com/account/statement/5429348172/MNT/OPR',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0',
    'app-version': '1.3.48-rc.718',
    'sec-ch-ua': '"Microsoft Edge";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'secure': 'yes'
  }

  response = httpx.get(url, headers=headers)
  
  # for row in response.json():
  #   transaction = Transaction(
  #     transaction_date =  parser.parse(row['transactionDate']),
  #     account_id = row['accountId'],
  #     amount_type = row['amountType']['codeDescription'],
  #     amount = row['amount']['amount'],
  #     transaction_remarks = row['transactionRemarks'],
  #     txn_time = datetime.strptime(row['txn_time'], "%H:%M").time(),
  #     begin_balance = row['beginBalance']['amount'],
  #     end_balance = row['endBalance']['amount']
  #   )
    
  #   db.add(transaction)
  #   print(transaction)

  # db.commit()
  return response.json()