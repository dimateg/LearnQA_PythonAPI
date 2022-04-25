import json.decoder
from datetime import datetime
from requests import Response
from lib.my_requests import MyRequests
from lib.assertions import Assertions

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

    def registration_user(self):
        register_data = self.prepare_registration_data()
        reg_user = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(reg_user, 200)
        Assertions.assert_json_has_key(reg_user, "id")

        email = register_data['email']
        username = register_data['username']
        first_name = register_data['firstName']
        last_name = register_data['lastName']
        password = register_data['password']
        user_id = self.get_json_value(reg_user, "id")

        return email, username, first_name, last_name, password, user_id

    def login_user(self, email, password):

        login_data = {
            'email': email,
            'password': password
        }

        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        return auth_sid, token
