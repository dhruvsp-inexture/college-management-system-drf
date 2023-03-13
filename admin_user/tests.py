from django.urls import reverse

from tests.test_setup import TestSetUp


class TestAdmin(TestSetUp):

    def test_assign_course_to_faculty_success(self):
        """test to assign course to faculty"""
        self.add_course()
        self.add_faculty()
        assign_course_data = {'course': 1, 'faculty': 2}
        response = self.client.post(reverse('assign_course-list'), assign_course_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['course'], 1)
        self.assertEqual(response.data['faculty'], 2)

    def test_assign_course_to_faculty_fail(self):
        """test to assign course to faculty which is already assigned previously"""

        self.test_assign_course_to_faculty_success()
        assign_course_data = {'course': 1, 'faculty': 2}
        response = self.client.post(reverse('assign_course-list'), assign_course_data)
