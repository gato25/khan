import httpx
import json
import base64

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