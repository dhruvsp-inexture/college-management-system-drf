from django_rest_passwordreset.models import ResetPasswordToken

class TestUsers:

    def test_user_register_success(self, client, load_initial_data, get_logged_in_user, test_admin_email,
                                   test_admin_password):
        """test for user registration success"""
        get_logged_in_user(test_admin_email, test_admin_password)
        user_data = {"email": "testuser@gmail.com", "password": "pass@123"}
        response = client.post("/user/", user_data)
        assert response.status_code == 201
        assert response.data['email'] == 'testuser@gmail.com'

    def test_register_user_fail_incorrect_email_format(self, client, load_initial_data, get_logged_in_user,
                                                       test_admin_email, test_admin_password):
        """test for user registration fail due to incorrect email format"""
        get_logged_in_user(test_admin_email, test_admin_password)
        user_data = {"email": "testuser", "password": "pass@123"}
        response = client.post("/user/", user_data)
        assert response.status_code == 400
        assert str(response.data['email'][0]) == 'Enter a valid email address.'

    def test_register_user_fail_incorrect_password_format(self, client, load_initial_data, get_logged_in_user,
                                                          test_admin_email, test_admin_password):
        """test for incorrect password format while user registration"""
        get_logged_in_user(test_admin_email, test_admin_password)
        user_data = {"email": "testuser@gmail.com", "password": "pass"}
        response = client.post("/user/", user_data)
        assert str(response.data['password'][0]) == 'This password is too short. It must contain at least 8 characters.'
        assert str(response.data['password'][1]) == 'This password is too common.'
        assert response.status_code == 400

    def test_register_user_fail_invalid_user_type(self, client, load_initial_data, get_logged_in_user, test_admin_email,
                                                  test_admin_password):
        """test for invalid user type while user registration"""
        get_logged_in_user(test_admin_email, test_admin_password)

        user_data = {"email": "testuser@gmail.com", "password": "pass@123", "user_type": "ABC"}
        response = client.post("/user/", user_data)
        assert str(response.data['user_type'][0]) == '"ABC" is not a valid choice.'
        assert response.status_code == 400

    def test_register_user_fail_field_required(self, client, load_initial_data, get_logged_in_user,
                                                       test_admin_email, test_admin_password):
        """test for multiple fields not provided while registration"""
        get_logged_in_user(test_admin_email, test_admin_password)
        user_data = {}
        response = client.post("/user/", user_data)
        assert response.status_code == 400
        assert str(response.data['email'][0]) == 'This field is required.'
        assert str(response.data['password'][0]) == 'This field is required.'

    def test_register_user_fail_email_exists(self, client, load_initial_data, get_logged_in_user, test_admin_email,
                                             test_admin_password):
        """test for user registration with existing email"""
        get_logged_in_user(test_admin_email, test_admin_password)

        user_data = {"email": "student@gmail.com", "password": "pass@123"}
        response = client.post("/user/", user_data)
        assert str(response.data['email'][0]) == 'User with this email address already exists.'
        assert response.status_code == 400

    def test_user_login_success(self, client, load_initial_data):
        """test user login success"""

        login_data = {"email": "admin@gmail.com", "password": "admin"}
        response = client.post("/gettoken/", login_data)
        assert 'access' in response.data

    def test_user_login_fail_email_required(self, client, load_initial_data):
        """test user login fail due to email required field"""

        login_data = {"password": "admin"}
        response = client.post("/gettoken/", login_data)
        assert str(response.data['email'][0]), 'This field is required.'

    def test_user_login_fail_password_required(self, client, load_initial_data):
        """test user login fail due to password required field"""

        login_data = {"email": "admin@gmail.com"}
        response = client.post("/gettoken/", login_data)
        assert str(response.data['password'][0]), 'This field is required.'

    def test_user_login_fail_incorrect_email(self, client, load_initial_data):
        """test user login fail due to incorrect email"""

        login_data = {"email": "email@gmail.com", "password": "admin"}
        response = client.post("/gettoken/", login_data)
        assert str(response.data['detail']), 'No active account found with the given credentials'

    def test_user_login_fail_incorrect_password(self, client, load_initial_data):
        """test user login fail due to incorrect password"""

        login_data = {"email": "email@gmail.com", "password": "abc@1234"}
        response = client.post("/gettoken/", login_data)
        assert str(response.data['detail']), 'No active account found with the given credentials'

    def test_get_all_user(self, client, load_initial_data, get_logged_in_user, test_admin_email, test_admin_password):
        """test to get all users"""
        get_logged_in_user(test_admin_email, test_admin_password)

        response = client.get('/user/')
        assert response.status_code == 200
        assert response.data[0]['id'] == 1
        assert response.data[0]['email'] == 'admin@gmail.com'
        assert response.data[0]['user_type'] == 'A'
        assert len(response.data) == 8

    def test_get_a_user(self, client, load_initial_data, get_logged_in_user, test_admin_email, test_admin_password):
        """test to get a single user by providing its id in url"""
        get_logged_in_user(test_admin_email, test_admin_password)
        response = client.get("/user/1/")
        assert response.status_code == 200
        assert response.data['id'] == 1
        assert response.data['email'] == 'admin@gmail.com'

    def test_user_not_found(self, client, load_initial_data, get_logged_in_user, test_admin_email, test_admin_password):
        """test when providing user id which doesn't exist in db"""
        get_logged_in_user(test_admin_email, test_admin_password)

        response = client.get("/user/111/")
        assert response.status_code == 404
        assert str(response.data['detail']) == 'Not found.'

    def test_get_my_details(self, client, load_initial_data, get_logged_in_user, test_student_email,
                            test_student_password):
        """test to get user details"""
        get_logged_in_user(test_student_email, test_student_password)

        response = client.get('/user/3/')
        assert response.status_code == 200
        assert response.data['id'] == 3
        assert response.data['email'] == 'student@gmail.com'

    def test_update_user_details(self, client, load_initial_data, get_logged_in_user, test_student_email,
                                 test_student_password):
        """test to update user's details"""
        get_logged_in_user(test_student_email, test_student_password)
        response = client.patch('/user/3/', {"email": "updated@gmail.com"})
        assert response.status_code == 200
        assert response.data['email'] == 'updated@gmail.com'

    def test_change_user_password_success(self, client, load_initial_data, get_logged_in_user, test_student_email,
                                          test_student_password):
        """test to change user password"""
        get_logged_in_user(test_student_email, test_student_password)

        change_password_data = {"current_password": "pass@123", "new_password": "student@123",
                                "confirm_new_password": "student@123"}
        response = client.put('/change-password/', change_password_data)
        assert response.status_code == 200
        assert response.data['message'] == 'Password changed successfully.'

    def test_change_user_password_fail_field_required(self, client, load_initial_data, get_logged_in_user,
                                                      test_student_email, test_student_password):
        """test to change user password when confirm new password field is not provided"""

        get_logged_in_user(test_student_email, test_student_password)

        change_password_data = {"current_password": "pass@123", "new_password": "student@123"}

        response = client.put('/change-password/', change_password_data)
        assert response.status_code == 400
        assert response.data['confirm_new_password'][0] == 'This field is required.'

    def test_change_user_password_fail_incorrect_current_password(self, client, load_initial_data, get_logged_in_user,
                                                                  test_student_email, test_student_password):
        """test to change user password and providing incorrect current password"""
        get_logged_in_user(test_student_email, test_student_password)

        change_password_data = {"current_password": "abc@123", "new_password": "student@123",
                                "confirm_new_password": "student@123"}

        response = client.put('/change-password/', change_password_data)
        assert response.status_code == 400
        assert response.data['current_password'][0] == 'Incorrect Current Password!'

    def test_change_user_password_fail_fields_dont_match(self, client, load_initial_data, get_logged_in_user,
                                                         test_student_email, test_student_password):
        """test to change user password when the new_password and confirm_new_password doesn't match"""
        get_logged_in_user(test_student_email, test_student_password)

        change_password_data = {"current_password": "pass@123", "new_password": "student@123",
                                "confirm_new_password": "student@456"}

        response = client.put('/change-password/', change_password_data)
        assert response.status_code == 400
        assert response.data['non_field_errors'][0] == 'New password fields are not matching!'

    def test_reset_password_request_link_success(self, client, load_initial_data):
        """test to reset user password"""
        response = client.post('/reset-password/',
                               data={'email': 'admin@gmail.com'})
        assert response.status_code == 200
        assert response.data['status'] == 'OK'

    def test_reset_password_request_link_fail_invalid_user(self, client, load_initial_data):
        """test to reset user password which is not registered"""
        response = client.post('/reset-password/',
                               data={'email': 'user1@gmail.com'})
        assert response.status_code == 400
        assert str(response.data['email'][
                       0]) == "We couldn't find an account associated with that email. Please try a different e-mail address."

    def test_reset_password_success(self, client, load_initial_data):
        """test to reset user password using token"""

        self.test_reset_password_request_link_success(client, load_initial_data)
        token = ResetPasswordToken.objects.filter().latest('id').key
        response = client.post('/reset-password/confirm/',
                               data={'password': 'testing@1234', 'token': token})
        assert response.status_code == 200
        assert response.data.get('status') == 'OK'
        login_response = client.post('/gettoken/',
                                     {'email': 'student@gmail.com', 'password': 'testing@1234'})
        assert login_response.status_code, 200

    def test_reset_password_fail_invalid_token(self, client, load_initial_data):
        """test to reset user password using invalid token"""

        self.test_reset_password_request_link_success(client, load_initial_data)
        token = ResetPasswordToken.objects.filter().latest('id').key + "abc"
        response = client.post('/reset-password/confirm/',
                                    data={'password': 'testing@1234', 'token': token})
        assert response.status_code == 404
        assert str(response.data['detail']) == 'Not found.'