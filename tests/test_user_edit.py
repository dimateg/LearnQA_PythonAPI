import json
import time
import allure
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions

@allure.epic("Edit user cases")
class TestUserEdit(BaseCase):
    @allure.description("This test edit just created user")
    @allure.feature('Positive')
    def test_edit_just_created_user(self):
        # register

        email, username, first_name, last_name, password, user_id = self.registration_user()

        # login

        auth_sid, token = self.login_user(email, password)

        # edit
        new_name = "Changed Name"

        response3 = MyRequests.put(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   data={"firstName": new_name})

        Assertions.assert_code_status(response3, 200)

        # get
        response4 = MyRequests.get(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid}
                                   )

        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            "Wrong name of the user after edit"
        )

    @allure.description("This test no auth")
    @allure.feature('Negative')
    def test_not_auth(self):
        new_name = "Changed Name"
        user_id = 33459
        response = MyRequests.put(f"/user/{user_id}",
                                  data={"firstName": new_name})

        Assertions.assert_code_status(response, 400)
        assert response.text == "Auth token not supplied", "Response is changed when unauthorized user tries to edit"

    @allure.description("This test authorized by other users")
    @allure.feature('Negative')
    def test_authorized_by_other_users(self):
        # register

        email, username, first_name, last_name, password, user_id = self.registration_user()
        auth_sid, token = self.login_user(email, password)

        time.sleep(2)

        email2, username2, first_name2, last_name2, password2, user_id2 = self.registration_user()
        auth_sid2, token2 = self.login_user(email2, password2)

        # edit
        new_name = "Changed Name Test"
        response3 = MyRequests.put(f"/user/{user_id}",
                                  headers={"x-csrf-token": token2},
                                  cookies={"auth_sid": auth_sid2},
                                  data={"firstName": new_name})

        Assertions.assert_code_status(response3, 200)
        #assert response.text == "Response is changed when unauthorized user tries to edit",\
        #    "Response is changed when unauthorized user tries to edit"

        # get
        response4 = MyRequests.get(f"/user/{user_id}",
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid}
                                   )

        old_name = "learnqa"
        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            old_name,
            "Wrong name of the user after edit"
        )

    @allure.description("This test new email without the symbol")
    @allure.feature('Negative')
    def test_new_email_without_the_symbol(self):
        # register

        email, username, first_name, last_name, password, user_id = self.registration_user()

        # login

        auth_sid, token = self.login_user(email, password)

        # edit

        new_email = "testemailexample.com"

        response = MyRequests.put(f"/user/{user_id}",
                                  headers={"x-csrf-token": token},
                                  cookies={"auth_sid": auth_sid},
                                  data={"email": new_email})

        Assertions.assert_code_status(response, 400)
        assert response.text == "Invalid email format", "Response does not match what is expected with invalid email"

    @allure.description("This test firstname short")
    @allure.feature('Negative')
    def test_firstname_short(self):
        # register

        email, username, first_name, last_name, password, user_id = self.registration_user()

        # login

        auth_sid, token = self.login_user(email, password)

        # edit

        new_first_name = "a"

        response = MyRequests.put(f"/user/{user_id}",
                                  headers={"x-csrf-token": token},
                                  cookies={"auth_sid": auth_sid},
                                  data={"firstName": new_first_name})

        media = json.loads(response.text)
        pars_json = media['error']

        Assertions.assert_code_status(response, 400)
        assert pars_json == "Too short value for field firstName",\
            "Response does not match what is expected with invalid firstName"

