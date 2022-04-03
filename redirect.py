import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect", allow_redirects=True)

redirect = response.history
redirect_final = response

print(redirect.__len__())
print(redirect_final.url)