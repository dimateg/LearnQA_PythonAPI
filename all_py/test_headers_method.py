import requests

class TestHeadersMethod:
    def test_headers_method(self):
        response = requests.get(" https://playground.learnqa.ru/api/homework_header")
        headers = response.headers['x-secret-homework-header']
        print(headers)

        assert headers == "Some secret value", 'Incorrect headers value'
