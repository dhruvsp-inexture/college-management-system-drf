from django.urls import reverse

from tests.test_setup import TestSetUp


class TestStudent(TestSetUp):
    def test_enroll_course_success(self):
        self.add_course()
        self.get_logged_in_student()
        enroll_course_data = {"course": 1}
        response = self.client.post(reverse('enroll-course'), enroll_course_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['student'], 2)
        self.assertEqual(response.data['course'], 1)

    def test_enroll_course_fail(self):
        self.add_course()
        self.get_logged_in_student()
        enroll_course_data = {"course": 2}
        response = self.client.post(reverse('enroll-course'), enroll_course_data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['error'], 'Course not found.')

    def test_get_enrolled_course(self):
        self.test_enroll_course_success()
        response = self.client.get(reverse('enroll-course'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['course']['name'], 'test course')

