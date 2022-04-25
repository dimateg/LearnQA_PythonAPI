import pytest
import allure
from datetime import datetime
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions

@allure.epic("Register user")
class TestUserRegister(BaseCase):
    parametrized_data = [
        (
            None,
            "learnqa",
            "learnqa",
            "learnqa",
            "vinkotov@example.com"
        ),
        (
            "123",
            None,
            "learnqa",
            "learnqa",
            "vinkotov@example.com"
        ),
        (
            "123",
            "learnqa",
            None,
            "learnqa",
            "vinkotov@example.com"
        ),
        (
            "123",
            "learnqa",
            "learnqa",
            None,
            "vinkotov@example.com"
        ),
        (
            "123",
            "learnqa",
            "learnqa",
            "learnqa",
            None
        )
    ]

    @allure.description("This test create user successfully")
    @allure.feature('Positive')
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    @allure.description("This test create user with existing email")
    @allure.feature('Positive')
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content {response.content}"

    @allure.description("This test create user without @ on email")
    @allure.feature('Positive')
    def test_create_user_without(self):
        email = 'vinkotovexample.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "utf-8") == "Invalid email format", f"Unexpected response content {response.content}"

    @allure.description("This test create user username one symbol")
    @allure.feature('Positive')
    def test_create_user_username_one_symbol(self):
        data ={
            "password": '123',
            "username": 'a',
            "firstName": 'learnqa',
            "lastName": 'learnqa',
            "email": 'vinkotov@example.com'
        }

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "utf-8") == "The value of 'username' field is too short", f"Unexpected response content {response.content}"

    @allure.description("This test create user username longname")
    @allure.feature('Positive')
    def test_create_user_username_longname(self):
        username = ('a' * 250)
        base_part = "learnqa"
        domain = "example.com"
        random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        email = f"{base_part}{random_part}@{domain}"

        data = {
            "password": '123',
            "username": username,
            "firstName": 'learnqa',
            "lastName": 'learnqa',
            "email": email
        }

        response = MyRequests.post("/user", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    @allure.description("This test create user without required parameter")
    @allure.feature('Negative')
    @pytest.mark.parametrize('password, username, firstName, lastName, email', parametrized_data)
    def test_create_user_without_required_parameter(self, password, username, firstName, lastName, email):
        data = {
            'password': password,
            'username': username,
            'firstName': firstName,
            'lastName': lastName,
            'email': email
        }
        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        response_text = response.text[42:]
        assert response.text == f"The following required params are missed: {response_text}", f"Unexpected response content {response.text}"