from django_rest_passwordreset.models import ResetPasswordToken

from tests.test_setup import TestSetUp


class TestUsers(TestSetUp):

    def test_user_login_success(self):
        """ test for user successful login"""
        response = self.client.post(self.login_url, self.admin_login_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['access'])

    def test_user_login_fail_email_required(self):
        """test for email not provided while login"""

        del self.admin_login_data['email']
        response = self.client.post(self.login_url, self.admin_login_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(str(response.data['email'][0]), 'This field is required.')

    def test_user_login_fail_password_required(self):
        """test for password not provided while login"""

        del self.admin_login_data['password']
        response = self.client.post(self.login_url, self.admin_login_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(str(response.data['password'][0]), 'This field is required.')

    def test_user_login_fail_incorrect_email(self):
        """test for incorrect email while login"""

        self.admin_login_data['email'] = 'abc@gmail.com'
        response = self.client.post(self.login_url, self.admin_login_data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(str(response.data['detail']), 'No active account found with the given credentials')

    def test_user_login_fail_incorrect_password(self):
        """test for incorrect password while login"""

        self.admin_login_data['password'] = 'pass'
        response = self.client.post(self.login_url, self.admin_login_data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(str(response.data['detail']), 'No active account found with the given credentials')

    def test_register_user_success(self):
        """test for successful user registration"""

        self.get_logged_in_admin()
        response = self.client.post(self.register_url, self.user_data)
        del self.user_data['password']
        self.user_data['id'] = 2
        self.assertEqual(response.data, self.user_data)
        self.assertEqual(response.status_code, 201)

    def test_register_user_fail_incorrect_email_format(self):
        """test for incorrect email format while user registration"""

        self.get_logged_in_admin()
        self.user_data["email"] = 'abc'
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(str(response.data['email'][0]), 'Enter a valid email address.')
        self.assertEqual(response.status_code, 400)

    def test_register_user_fail_incorrect_password_format(self):
        """test for incorrect password format while user registration"""

        self.get_logged_in_admin()
        self.user_data["password"] = 'abc'
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(str(response.data['password'][0]),
                         'This password is too short. It must contain at least 8 characters.')
        self.assertEqual(str(response.data['password'][1]), 'This password is too common.')
        self.assertEqual(response.status_code, 400)

    def test_register_user_fail_invalid_user_type(self):
        """test for invalid user type while user registration"""

        self.get_logged_in_admin()
        self.user_data["user_type"] = 'abc'
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual((response.data['user_type'][0]), '"abc" is not a valid choice.')
        self.assertEqual(response.status_code, 400)

    def test_register_user_fail_field_required(self):
        """test for multiple fields not provided while registration"""

        self.get_logged_in_admin()
        del self.user_data['email']
        del self.user_data['password']
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(str(response.data['email'][0]), 'This field is required.')
        self.assertEqual(str(response.data['password'][0]), 'This field is required.')
        self.assertEqual(response.status_code, 400)

    def test_register_user_fail_email_exists(self):
        """test for user registration with existing email"""

        self.get_logged_in_admin()
        self.user_data['email'] = "admin@example.com"
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(str(response.data['email'][0]), 'User with this email address already exists.')
        self.assertEqual(response.status_code, 400)

    def test_get_all_user(self):
        """test to get all users"""

        self.get_logged_in_admin()
        self.test_register_user_success()  # adding another user
        response = self.client.get(self.register_url)
        self.assertEqual(response.data[0]['id'], 1)
        self.assertEqual(response.data[0]['email'], 'admin@example.com')
        self.assertEqual(response.data[0]['user_type'], 'A')
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.status_code, 200)

    def test_get_a_user(self):
        """test to get a single user by providing its id in url"""

        self.get_logged_in_admin()
        response = self.client.get("/user/1/")
        self.assertEqual(response.data['id'], 1)
        self.assertEqual(response.data['email'], 'admin@example.com')
        self.assertEqual(response.status_code, 200)

    def test_user_not_found(self):
        """test when providing user id which doesn't exist in db"""

        self.get_logged_in_admin()
        response = self.client.get("/user/111/")
        self.assertEqual(str(response.data['detail']), 'Not found.')
        self.assertEqual(response.status_code, 404)

    def test_get_my_details(self):
        """test to get logged in user's detail"""

        self.get_logged_in_student()
        response = self.client.get('/user/2/')
        self.assertEqual(response.data["first_name"], 'student')
        self.assertEqual(response.data["email"], 'student@gmail.com')
        self.assertEqual(response.status_code, 200)

    def test_update_user_details(self):
        """test to update user's details"""

        self.get_logged_in_admin()
        response = self.client.patch('/user/1/', {"email": "updated@gmail.com"})
        self.assertEqual(response.data["email"], "updated@gmail.com")
        self.assertEqual(response.status_code, 200)

    def test_change_user_password_success(self):
        """test to change user password"""
        self.get_logged_in_student()
        change_password_data = {"current_password": "pass@123", "new_password": "student@123",
                                "confirm_new_password": "student@123"}
        response = self.client.put('/change-password/', change_password_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'Password changed successfully.')

    def test_change_user_password_fail_field_required(self):
        """test to change user password when confirm new password field is not provided"""
        self.get_logged_in_student()
        change_password_data = {"current_password": "pass@123", "new_password": "student@123"}
        response = self.client.put('/change-password/', change_password_data)
        self.assertEqual(str(response.data['confirm_new_password'][0]), 'This field is required.')
        self.assertEqual(response.status_code, 400)

    def test_change_user_password_fail_incorrect_current_password(self):
        """test to change user password and providing incorrect current password"""
        self.get_logged_in_student()
        change_password_data = {"current_password": "abc@123", "new_password": "student@123",
                                "confirm_new_password": "student@123"}
        response = self.client.put('/change-password/', change_password_data)
        self.assertEqual(str(response.data['current_password'][0]), 'Incorrect Current Password!')
        self.assertEqual(response.status_code, 400)

    def test_change_user_password_fail_fields_dont_match(self):
        """test to change user password when the new_password and confirm_new_password doesn't match"""
        self.get_logged_in_student()
        change_password_data = {"current_password": "pass@123", "new_password": "student@123",
                                "confirm_new_password": "student@456"}
        response = self.client.put('/change-password/', change_password_data)
        self.assertEqual(str(response.data['non_field_errors'][0]), 'New password fields are not matching!')
        self.assertEqual(response.status_code, 400)

    def test_reset_password_request_link_success(self):
        """test to reset user password"""
        self.test_register_user_success()
        response = self.client.post('/reset-password/',
                                    data={'email': 'admin@example.com'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'], 'OK')

    def test_reset_password_request_link_fail_invalid_user(self):
        """test to reset user password which is not registered"""

        response = self.client.post('/reset-password/',
                                    data={'email': 'user1@gmail.com'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(str(response.data['email'][0]),
                         "We couldn't find an account associated with that email. Please try a different e-mail address.")

    def test_reset_password_success(self):
        """test to reset user password using token """

        user_id = self.get_logged_in_student()
        self.client.post('/reset-password/',
                         data={'email': 'student@gmail.com'})

        token = ResetPasswordToken.objects.filter().latest('id').key
        response = self.client.post('/reset-password/confirm/',
                                    data={'password': 'testing@1234', 'token': token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('status'), 'OK')

        # Login after password reset with new password.
        login_response = self.client.post(self.login_url,
                                          {'email': 'student@gmail.com', 'password': 'testing@1234'})
        self.assertEqual(login_response.status_code, 200)

    def test_reset_password_fail_invalid_token(self):
        """test to reset user password using invalid token"""

        user_id = self.get_logged_in_student()
        self.client.post('/reset-password/',
                         data={'email': 'student@gmail.com'})
        token = "abcd1234"
        response = self.client.post('/reset-password/confirm/',
                                    data={'password': 'testing@1234', 'token': token})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(str(response.data['detail']), 'Not found.')
