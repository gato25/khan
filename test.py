import subprocess

curl_command = [
    "curl",
    "--location",
    "https://e.khanbank.com/v1/cfrm/auth/token?grant_type=refresh_token&refresh_token=",
    "--header", "Accept: application/json, text/plain, */*",
    "--header", "Accept-Language: mn-MN",
    "--header", "Authorization: Basic ==",
    "--header", "Connection: keep-alive",
    "--header", "Content-Type: application/x-www-form-urlencoded",
    "--header", "Origin: https://e.khanbank.com",
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
