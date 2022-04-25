from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserDelete(BaseCase):
    def test_delete_user_id_2(self):
        user_id = 2
        email = 'vinkotov@example.com'
        password = "1234"

        auth_sid, token = self.login_user(email, password)

        response = MyRequests.delete(f"/user/{user_id}",
                                     headers={"x-csrf-token": token},
                                     cookies={"auth_sid": auth_sid})

        Assertions.assert_code_status(response, 400)
        assert response.text == "Please, do not delete test users with ID 1, 2, 3, 4 or 5.", \
            f"Response does not match what is expected with ID 1, 2, 3, 4 or 5. Your ID {user_id}"

    def test_delete_new_user(self):
        email, username, first_name, last_name, password, user_id = self.registration_user()

        auth_sid, token = self.login_user(email, password)

        response = MyRequests.delete(f"/user/{user_id}",
                                     headers={"x-csrf-token": token},
                                     cookies={"auth_sid": auth_sid})

        Assertions.assert_code_status(response, 200)

        login_data = {
            'email': email,
            'password': password
        }

        response2 = MyRequests.post("/user/login", data=login_data)

        Assertions.assert_code_status(response2, 400)
        assert response2.text == "Invalid username/password supplied", \
            f"Deletion failed for user {user_id, email, password}"

    def test_deletion_by_another_user(self):
        email, username, first_name, last_name, password, user_id = self.registration_user()

        email2, username2, first_name2, last_name2, password2, user_id2 = self.registration_user()
        auth_sid2, token2 = self.login_user(email2, password2)

        response3 = MyRequests.delete(f"/user/{user_id}",
                                      headers={"x-csrf-token": token2},
                                      cookies={"auth_sid": auth_sid2})

        Assertions.assert_code_status(response3, 200)

        auth_sid, token = self.login_user(email, password)
