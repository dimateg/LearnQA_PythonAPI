import json.decoder
from datetime import datetime
from requests import Response

class BaseCase:
    def get_cookie(self, response: Response, cookie_name):
        assert cookie_name in response.cookies, f"Не найден куки для имени {cookie_name} в последнем запросе"
        return response.cookies[cookie_name]

    def get_header(self, response: Response, header_name):
        assert header_name in response.headers, f"Не найден куки для имени {header_name} в последнем запросе"
        return response.headers[header_name]

    def get_json_value(self, response: Response, name):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecoder:
            assert False, f"Ответ находится не в JSON фотрмате. Response text is {response.text}"

        assert name in response_as_dict, f"Ответ в JSON не имеет ключа {name}"

        return response_as_dict[name]

    def prepare_registration_data(self, email=None):
        if email is None:
            base_part = "learnqa"
            domain = "example.com"
            random_part = datetime.now().strftime("%m%d%Y%H%M%S")
            email = f"{base_part}{random_part}@{domain}"
        return {
            "password": '123',
            "username": 'learnqa',
            "firstName": 'learnqa',
            "lastName": 'learnqa',
            "email": email
        }
