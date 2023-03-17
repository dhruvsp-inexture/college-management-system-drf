import json


class TestStudent:
    def test_enroll_course_success(self, client, get_logged_in_user, test_student_email, test_student_password):
        """test to enroll course by student"""
        get_logged_in_user(test_student_email, test_student_password)
        enroll_course_data = {"course": 14}
        response = client.post('/enroll-course/', enroll_course_data)
        assert response.status_code == 201
        assert response.data['student'] == 3
        assert response.data['course'] == 14

    def test_enroll_course_fail_not_found(self, client, get_logged_in_user, test_student_email, test_student_password):
        """test to enroll course which doesn't exist"""
        get_logged_in_user(test_student_email, test_student_password)
        enroll_course_data = {"course": 100}
        response = client.post('/enroll-course/', enroll_course_data)
        assert response.status_code == 404
        assert response.data['error'] == 'Course not found.'

    def test_enroll_course_fail_unique_together(self, client, get_logged_in_user, test_student_email, test_student_password):
        """test to enroll course which is already enrolled previously"""
        get_logged_in_user(test_student_email, test_student_password)
        enroll_course_data = {"course": 3}
        response = client.post('/enroll-course/', enroll_course_data)
        assert response.status_code == 404
        assert response.data['error'] == 'You have already enrolled in this course.'

    def test_get_enrolled_course(self, client, get_logged_in_user, test_student_email, test_student_password):
        """test to get all enrolled course of the logged in student"""
        get_logged_in_user(test_student_email, test_student_password)
        response = client.get('/enroll-course/')
        assert response.status_code == 200
        assert len(response.data) == 6
        assert response.data[0]['course']['id'] == 3
        assert response.data[0]['course']['name'] == 'test12345678'

    def test_drop_course_success(self, client, get_logged_in_user, test_student_email, test_student_password):
        """test to drop course"""
        get_logged_in_user(test_student_email, test_student_password)
        drop_course_data = {"course": 3}
        response = client.delete('/drop-course/', data=json.dumps(drop_course_data), content_type='application/json')
        assert response.status_code == 204
        assert response.data['success'] == 'Course dropped'

    def test_drop_course_fail(self, client, get_logged_in_user, test_student_email, test_student_password):
        """test to drop course fail as course not found"""
        get_logged_in_user(test_student_email, test_student_password)
        drop_course_data = {"course": 100}
        response = client.delete('/drop-course/', data=json.dumps(drop_course_data), content_type='application/json')
        assert response.status_code == 404
        assert response.data['error'] == 'Data not found'

