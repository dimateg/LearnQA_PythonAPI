import allure
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions

@allure.epic("get user cases")
class TestUserGet(BaseCase):
    @allure.description("This get user details not auth")
    @allure.feature('Positive')
    def test_get_user_details_not_auth(self):
        response = MyRequests.get("/user/2")
        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_not_key(response, "email")
        Assertions.assert_json_has_not_key(response, "firstName")
        Assertions.assert_json_has_not_key(response, "lastName")

    @allure.description("This get user details auth as same user")
    @allure.feature('Positive')
    def test_get_user_details_auth_as_same_user(self):
        data = {
            "email": 'vinkotov@example.com',
            "password": '1234'
        }

        response1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response1, 'auth_sid')
        token = self.get_header(response1, 'x-csrf-token')
        user_is_from_auth_method = self.get_json_value(response1, 'user_id')

        response2 = MyRequests.get(f"/user/{user_is_from_auth_method}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid}
                                   )

        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response2, expected_fields)

    @allure.description("This get user auth without id")
    @allure.feature('Positive')
    def test_get_user_auth_without_id(self):
        data = {
            "email": 'vinkotov@example.com',
            "password": '1234'
        }

        response1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response1, 'auth_sid')
        token = self.get_header(response1, 'x-csrf-token')
        user_is_from_auth_method = self.get_json_value(response1, 'user_id')
        user_id = '33446'

        response2 = MyRequests.get(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid}
                                   )

        Assertions.assert_json_has_key(response2, "username")
        Assertions.assert_json_has_not_key(response2, "email")
        Assertions.assert_json_has_not_key(response2, "firstName")
        Assertions.assert_json_has_not_key(response2, "lastName")