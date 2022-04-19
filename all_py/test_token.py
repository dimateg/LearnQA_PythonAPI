import requests
import json
import time

print('request 1')
response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job")
media = json.loads(response.text)
tokens = media['token']
seconds = media['seconds']
print('token =', tokens, 'seconds =', seconds)

print('request 2')
response2 = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params={"token": tokens})
media2 = json.loads(response2.text)
status = media2['status']

if 'Job is NOT ready' in status:
    print('status =', status, 'test 1 - true')
else:
    print('test 1 - false')

time.sleep(seconds)

print('request 3')
response3 = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params={"token": tokens})
media3 = json.loads(response3.text)
status = media3['status']

if 'result' in media3:
    result = media3['result']
    if 'Job is ready' in status:
        print('result =', result, 'status =', status, 'test 2 - true')
    else:
        print('test 2 - false')
else:
    print('test 2 - false')

print('finish')