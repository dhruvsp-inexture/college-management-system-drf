class TestAdmin:
    def test_assign_course_to_faculty_success(self, client, test_admin_email, test_admin_password,
                                              get_logged_in_user):
        """test to assign course to faculty"""
        get_logged_in_user(test_admin_email, test_admin_password)
        assign_course_data = {"faculty": "12", "course": "12"}
        response = client.post('/assign-course/', assign_course_data)
        assert response.status_code == 201
        assert response.data['course'] == 12
        assert response.data['faculty'] == 12

    def test_assign_course_to_faculty_fail(self, client, test_admin_email, test_admin_password,
                                           get_logged_in_user):
        """test to assign course to faculty which is already assigned previously"""
        get_logged_in_user(test_admin_email, test_admin_password)
        assign_course_data = {"faculty": "12", "course": "3"}
        response = client.post('/assign-course/', assign_course_data)
        assert response.status_code == 400
        assert response.data['non_field_errors'][0] == 'The faculty has been already assigned with the same course.'

    def test_get_all_assigned_courses(self, client, test_admin_email, test_admin_password,
                                      get_logged_in_user):
        """test to assign course to faculty which is already assigned previously"""
        get_logged_in_user(test_admin_email, test_admin_password)
        response = client.get('/assign-course/')
        assert response.status_code == 200
        assert response.data[0]['id'] == 3
        assert response.data[0]['course'] == 1
        assert response.data[0]['faculty'] == 5

    def test_update_assign_course(self, client, test_admin_email, test_admin_password,
                                  get_logged_in_user):
        """test to update assigned course """
        get_logged_in_user(test_admin_email, test_admin_password)
        update_assign_course_data = {'course': 3, 'faculty': 5}
        response = client.put('/assign-course/3/', update_assign_course_data)
        assert response.status_code == 200
        assert response.data['id'] == 3
        assert response.data['course'] == 3
        assert response.data['faculty'] == 5

    def test_get_a_assigned_course(self, client, test_admin_email, test_admin_password,
                                   get_logged_in_user):
        """test to get a single assigned course"""
        get_logged_in_user(test_admin_email, test_admin_password)
        response = client.get('/assign-course/3/')
        assert response.status_code == 200
        assert response.data['id'] == 3
        assert response.data['course'] == 1
        assert response.data['faculty'] == 5

    def test_delete_assigned_course(self, client, test_admin_email, test_admin_password,
                                    get_logged_in_user):
        """test to delete assigned course to a faculty"""
        get_logged_in_user(test_admin_email, test_admin_password)

        response = client.delete('/assign-course/3/')
        assert response.status_code == 204


