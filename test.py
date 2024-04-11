import subprocess

curl_command = [
    "curl",
    "--location",
    "https://e.khanbank.com/v1/cfrm/auth/token?grant_type=refresh_token&refresh_token=PXDZa8ACW7xjOujMoou89RjGs0HzAqvT",
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
    print("Output:")
    print(result.stdout)
except subprocess.CalledProcessError as e:
    print("Error:")
    print(e)
