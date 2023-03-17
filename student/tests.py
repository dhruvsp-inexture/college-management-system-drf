import json
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

    def test_enroll_course_fail_not_found(self):
        self.add_course()
        self.get_logged_in_student()
        enroll_course_data = {"course": 200}
        response = self.client.post(reverse('enroll-course'), enroll_course_data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['error'], 'Course not found.')

    def test_enroll_course_fail_unique_together(self):
        self.test_enroll_course_success()
        enroll_course_data = {"course": 1}
        response = self.client.post(reverse('enroll-course'), enroll_course_data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['error'], 'You have already enrolled in this course.')

    def test_get_enrolled_course(self):
        self.test_enroll_course_success()
        response = self.client.get(reverse('enroll-course'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['course']['name'], 'test course')

    def test_drop_course_success(self):
        self.test_enroll_course_success()
        drop_course_data = {"course": 1}
        response = self.client.delete(reverse('drop-course'), data=json.dumps(drop_course_data), content_type='application/json')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data['success'], 'Course Dropped.')

    def test_drop_course_fail(self):
        self.test_enroll_course_success()
        drop_course_data = {"course": 100}
        response = self.client.delete(reverse('drop-course'), data=json.dumps(drop_course_data), content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['error'], 'Data not found')

