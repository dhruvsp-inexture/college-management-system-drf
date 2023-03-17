class TestFaculty:
    def test_get_assigned_course(self, client, test_faculty_email, test_faculty_password, get_logged_in_user):
        """test to get assigned course of the faculty"""
        get_logged_in_user(test_faculty_email, test_faculty_password)
        response = client.get('/show-course/')
        assert response.status_code == 200
        assert response.data[0]['course']['id'] == 1
        assert response.data[0]['course']['name'] == 'test123456'

    def test_grade_student_success(self, client, test_faculty_email, test_faculty_password, get_logged_in_user):
        """test to grade student by faculty"""
        get_logged_in_user(test_faculty_email, test_faculty_password)
        grade_student_data = {'student': 3, 'course': 6, 'grade': 'A'}
        response = client.put('/grade-student/', grade_student_data)
        assert response.status_code == 204
        assert response.data['message'] == 'Grade Updated Successfully'

    def test_grade_student_fail_grade_invalid_choice(self, client, test_faculty_email, test_faculty_password,
                                                     get_logged_in_user):
        """test to grade student by faculty where grade is invalid"""
        get_logged_in_user(test_faculty_email, test_faculty_password)
        grade_student_data = {'student': 3, 'course': 6, 'grade': 'ABC'}
        response = client.put('/grade-student/', grade_student_data)
        assert response.status_code == 400
        assert str(response.data['error']['grade'][0]) == '"ABC" is not a valid choice.'

    def test_grade_student_fail_course_not_ended(self, client, test_faculty_email, test_faculty_password,
                                                 get_logged_in_user):
        """test to grade student by faculty where course has not ended yet"""
        get_logged_in_user(test_faculty_email, test_faculty_password)
        grade_student_data = {'student': 3, 'course': 3, 'grade': 'A'}
        response = client.put('/grade-student/', grade_student_data)
        assert response.status_code == 400
        assert str(response.data['error']['non_field_errors'][0]) == \
               'Course has not ended yet. It will end on 2023-06-03. Grade can only be assigned after course has ended.'

    def test_grade_student_fail_not_found(self, client, test_faculty_email, test_faculty_password,
                                                 get_logged_in_user):
        """test to grade student which is not found"""
        get_logged_in_user(test_faculty_email, test_faculty_password)
        grade_student_data = {'student': 30, 'course': 3, 'grade': 'A'}
        response = client.put('/grade-student/', grade_student_data)
        assert response.status_code == 404
        assert response.data['error'] == 'Data not found'

    def test_grade_student_fail_bad_request(self, client, test_faculty_email, test_faculty_password,
                                                 get_logged_in_user):
        """test to grade student which is not found"""
        get_logged_in_user(test_faculty_email, test_faculty_password)
        grade_student_data = {'student': "abc", 'course': "def", 'grade': 'A'}
        response = client.put('/grade-student/', grade_student_data)
        assert response.status_code == 400
        assert response.data['error'] == 'Bad Request'

    def test_get_students(self, client, test_faculty_email, test_faculty_password,
                                                 get_logged_in_user):
        """test to get students for grading by faculty"""
        get_logged_in_user(test_faculty_email, test_faculty_password)
        response = client.get('/view-grades/')
        assert response.status_code == 200
        assert len(response.data) == 2
        assert response.data[0]['grade'] == 'A'
        assert response.data[0]['student'] == 3
        assert response.data[0]['course'] == 3

