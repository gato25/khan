import httpx
import json
import base64
from .models.token import Token

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
  'app-version': '1.3.48-rc.718',
  'channelcontext': '',
  'sec-ch-ua': '"Microsoft Edge";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'secure': 'yes'
}

def get_otp(username, password):
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
  return secondary_response.json()

def login(otp, req_id, username):
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

def refresh_token(db):
  try:
    token = db.query(Token).order_by(Token.created_at.desc()).first()
    
    payload = '%7B%7D='
    headers = {
      'Accept': 'application/json, text/plain, */*',
      'Accept-Language': 'mn-MN',
      # 'Authorization': f'Basic {token.access_token}',
      'Connection': 'keep-alive',
      'Content-Type': 'application/x-www-form-urlencoded',
      'Origin': 'https://e.khanbank.com',
      'Referer': 'https://e.khanbank.com/account/statement/5429348172/MNT/OPR',
      'Sec-Fetch-Dest': 'empty',
      'Sec-Fetch-Mode': 'cors',
      'Sec-Fetch-Site': 'same-origin'
    }
    
    url = f"https://e.khanbank.com/v1/cfrm/auth/token?grant_type=refresh_token&refresh_token={token.refresh_token}"

    response = httpx.post(url, headers=headers)
    print(response)
    return response.json()
  except Exception as e:
    print(e)
    import traceback
    traceback.print_exc()