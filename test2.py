import httpx

url = "https://e.khanbank.com/v1/omni/user/custom/operativeaccounts/transactions?transactionValue=0&transactionDate=%7B%22lt%22:%222024-04-09T00:00:00%22,%22gt%22:%222024-04-11T00:00:00%22%7D&amount=%7B%22lt%22:%220%22,%22gt%22:%220%22%7D&amountType=&transactionCategoryId=&transactionRemarks=&customerName=%D0%94%D0%90%D0%9C%D0%91%D0%90+%D0%91%D0%90%D0%94%D0%90%D0%9C%D0%93%D0%90%D0%A0%D0%90%D0%92&transactionCurrency=MNT&branchCode=5029"

payload = {}
headers = {
  'Accept': 'application/json, text/plain, */*',
  'Accept-Language': 'mn-MN',
  'Connection': 'keep-alive',
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

print(response.json())
