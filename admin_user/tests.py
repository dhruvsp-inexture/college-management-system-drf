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
        self.assertEqual(response.status_code, 400)
        self.assertEqual(str(response.data['non_field_errors'][0]),
                         'The faculty has been already assigned with the same course.')

    def test_get_all_assigned_courses(self):
        self.test_assign_course_to_faculty_success()
        response = self.client.get(reverse('assign_course-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['id'], 1)
        self.assertEqual(response.data[0]['course'], 1)
        self.assertEqual(response.data[0]['faculty'], 2)


    def test_update_assign_course(self):
        """test to update assigned course"""
        self.test_assign_course_to_faculty_success()

        # adding new course which will be later assigned to faculty
        course_data = {"name": "course 2", "description": "test description"}
        self.client.post(reverse('course-list'), course_data)

        update_assign_course_data = {'course': 2, 'faculty': 2}
        response = self.client.put(reverse('assign_course-detail', args=[1]), update_assign_course_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['course'], 2)
        self.assertEqual(response.data['faculty'], 2)

    def test_get_a_assigned_course(self):
        """test to get a single assigned course"""

        self.test_assign_course_to_faculty_success()

        response = self.client.get(reverse('assign_course-detail', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['course'], 1)
        self.assertEqual(response.data['faculty'], 2)

    def test_delete_assigned_course(self):
        """test to delete assigned course to a faculty"""
        self.test_assign_course_to_faculty_success()

        response = self.client.delete(reverse('assign_course-detail', args=[1]))
        self.assertEqual(response.status_code, 204)
