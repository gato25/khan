import httpx

url = "https://e.khanbank.com/v1/omni/user/custom/operativeaccounts/5429348172/transactions?transactionValue=0&transactionDate=%7B%22lt%22:%222024-04-09T00:00:00%22,%22gt%22:%222024-04-11T00:00:00%22%7D&amount=%7B%22lt%22:%220%22,%22gt%22:%220%22%7D&amountType=&transactionCategoryId=&transactionRemarks=&customerName=%D0%94%D0%90%D0%9C%D0%91%D0%90+%D0%91%D0%90%D0%94%D0%90%D0%9C%D0%93%D0%90%D0%A0%D0%90%D0%92&transactionCurrency=MNT&branchCode=5029"

payload = {}
headers = {
  'Accept': 'application/json, text/plain, */*',
  'Accept-Language': 'mn-MN',
  'Authorization': 'Bearer jwrfyOnFFbn7oBmLdZUgsp4Pq9a7',
  'Connection': 'keep-alive',
  'Cookie': '_ga=GA1.1.491542904.1709608750; __ssds=2; __ssuzjsr2=a9be0cd8e; __uzmaj2=97f36607-bc79-4c5c-8a4d-df21677a36e2; __uzmbj2=1709608750; __uzma=2fd083d4-64e1-8a5f-089c-45515714c4f3; __uzmb=1712305789; __uzme=6444; SL_ClassKey=0.1.1; _ga_XY11GTD04T=GS1.1.1712799055.6.0.1712799055.60.0.0; __uzmcj2=572836129519; __uzmdj2=1712799059; __uzmd=1712799721; __uzmc=5993228911758; SL_ClassKey=0.1.1; __uzma=ff157351-6a7c-bc64-1a8a-d4bd27d5a592; __uzmb=1712799658; __uzmc=6214729287378; __uzmd=1712799852; __uzme=8043',
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

print(response.text)
