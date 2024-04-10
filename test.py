import subprocess
import json

curl_command = '''
curl --location 'https://e.khanbank.com/v1/cfrm/auth/token?grant_type=refresh_token&refresh_token=xEJmzAyj2Gn8snCOqPtMN32aF1xF4IYp' \\
--header 'Accept: application/json, text/plain, */*' \\
--header 'Accept-Language: mn-MN' \\
--header 'Connection: keep-alive' \\
--header 'Content-Type: application/x-www-form-urlencoded' \\
--header 'Origin: https://e.khanbank.com' \\
--header 'Referer: https://e.khanbank.com/account/statement/5429348172/MNT/OPR' \\
--header 'Sec-Fetch-Dest: empty' \\
--header 'Sec-Fetch-Mode: cors' \\
--header 'Sec-Fetch-Site: same-origin' \\
--header 'app-version: 1.3.48-rc.718' \\
--header 'sec-ch-ua: "Microsoft Edge";v="123", "Not:A-Brand";v="8", "Chromium";v="123"' \\
--header 'sec-ch-ua-mobile: ?0' \\
--header 'sec-ch-ua-platform: "Windows"' \\
--header 'secure: yes' \\
--data-urlencode '%7B%7D='
'''

process = subprocess.Popen(curl_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
stdout, stderr = process.communicate()

if process.returncode == 0:
    response_text = stdout.decode('utf-8')
    print(response_text)
    try:
        response_json = json.loads(response_text)
        print(response_json)
    except json.JSONDecodeError:
        print("Failed to parse JSON response:", response_text)
else:
    print("cURL command failed with error:")
    print(stderr.decode('utf-8'))