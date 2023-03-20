class TestCourses:
    def test_get_all_course(self, client, load_initial_data, test_admin_email, test_admin_password, get_logged_in_user):
        """test to get all courses"""
        get_logged_in_user(test_admin_email, test_admin_password)
        response = client.get('/course/')
        assert response.status_code == 200
        assert len(response.data) == 14
        assert response.data[0]['id'] == 1
        assert response.data[0]['name'] == "test123456"

    def test_add_course_success(self, client, load_initial_data, test_admin_email, test_admin_password,
                                get_logged_in_user):
        """test to add course"""
        get_logged_in_user(test_admin_email, test_admin_password)
        course_data = {"name": "course test", "description": "test description", "start_date": "2023-06-15"}
        response = client.post('/course/', course_data)
        assert response.status_code == 201
        assert response.data['name'] == 'course test'
        assert response.data['description'] == 'test description'

    def test_add_course_fail_course_exists(self, client, load_initial_data, test_admin_email, test_admin_password,
                                           get_logged_in_user):
        """test to add course with a name that already exists"""
        get_logged_in_user(test_admin_email, test_admin_password)
        course_data = {"name": "course1", "description": "test description"}
        response = client.post('/course/', course_data)
        assert response.status_code == 400
        assert str(response.data['name'][0]) == 'course with this name already exists.'

    def test_add_course_fail_invalid_start_date(self, client, load_initial_data, test_admin_email, test_admin_password,
                                                get_logged_in_user):
        """test for adding course with invalid start date"""
        get_logged_in_user(test_admin_email, test_admin_password)
        course_data = {"name": "new course", "description": "test description", "start_date": "2000-02-01"}
        response = client.post('/course/', course_data)
        assert response.status_code == 400
        assert str(response.data['start_date'][0]) == "Start Date shouldn't be before today!"

    def test_add_course_fail_invalid_end_date(self, client, load_initial_data, test_admin_email, test_admin_password,
                                                get_logged_in_user):
        """test for adding course with invalid end date"""
        get_logged_in_user(test_admin_email, test_admin_password)
        course_data = {"name": "new course", "description": "test description", "start_date": "2023-05-05", "end_date": "2023-05-01"}
        response = client.post('/course/', course_data)
        assert response.status_code == 400
        assert str(response.data['non_field_errors'][0]) == "End Date should be after Start Date!"

    def test_add_course_fail_invalid_price(self, client, load_initial_data, test_admin_email, test_admin_password,
                                                get_logged_in_user):
        """test for adding course with invalid price"""
        get_logged_in_user(test_admin_email, test_admin_password)
        course_data = {"name": "new course", "description": "test description", "start_date": "2023-05-05", "end_date": "2023-05-01", "price": -100}
        response = client.post('/course/', course_data)
        assert response.status_code == 400
        assert str(response.data['price'][0]) == 'Ensure this value is greater than or equal to 0.'

    def test_get_a_course(self, client, load_initial_data, test_admin_email, test_admin_password,
                                                get_logged_in_user):
        """test to get a single course details"""
        get_logged_in_user(test_admin_email, test_admin_password)
        response = client.get('/course/1/')
        assert response.status_code == 200
        assert response.data["id"] == 1
        assert response.data["name"] == 'test123456'
        assert response.data["description"] == 'test description123456'

    def test_update_course_success(self, client, load_initial_data, test_admin_email, test_admin_password,
                                                get_logged_in_user):
        """test to update a course"""
        get_logged_in_user(test_admin_email, test_admin_password)
        update_course_data = {"name": "updated course"}
        response = client.patch('/course/1/', update_course_data)
        assert response.status_code == 200
        assert response.data['name'] == 'updated course'

    def test_update_course_fail_invalid_end_date(self, client, load_initial_data, test_admin_email, test_admin_password,
                                                get_logged_in_user):
        """test to update a course with invalid end date"""
        get_logged_in_user(test_admin_email, test_admin_password)
        update_course_data = {"end_date": "2000-01-01"}
        response = client.patch('/course/1/', update_course_data)
        assert response.status_code == 400
        assert str(response.data[0]) == 'End Date should be after Start Date!'

    def test_update_course_fail_invalid_start_date(self, client, load_initial_data, test_admin_email, test_admin_password,
                                                get_logged_in_user):
        """test to update a course with invalid start date"""
        get_logged_in_user(test_admin_email, test_admin_password)
        update_course_data = {"start_date": "2025-01-01"}
        response = client.patch('/course/1/', update_course_data)
        assert response.status_code == 400
        assert str(response.data[0]) == 'Start Date should be before End Date!'

    def test_update_course_fail_invalid_price(self, client, load_initial_data, test_admin_email, test_admin_password,
                                                get_logged_in_user):
        """test to update a course with invalid price"""
        get_logged_in_user(test_admin_email, test_admin_password)
        update_course_data = {"price": "abc"}
        response = client.patch('/course/1/', update_course_data)
        assert response.status_code == 400
        assert str(response.data['price'][0]) == 'A valid number is required.'

    def test_delete_course(self, client, load_initial_data, test_admin_email, test_admin_password,
                                                get_logged_in_user):
        """test to delete course"""
        get_logged_in_user(test_admin_email, test_admin_password)
        response = client.delete('/course/1/')
        assert response.status_code == 204

