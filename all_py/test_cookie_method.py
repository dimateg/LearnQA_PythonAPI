import requests

class TestCookieMethod:
    def test_cookie_method(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_cookie")
        cookie = response.cookies['HomeWork']
        print(response.cookies['HomeWork'])
        print(cookie)

        assert cookie == "hw_value", 'Incorrect cookie value'
