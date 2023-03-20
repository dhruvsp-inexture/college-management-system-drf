from django.urls import reverse

from tests.test_setup import TestSetUp


class TestCourse(TestSetUp):

    def test_get_all_course(self):
        self.add_course()
        response = self.client.get(reverse('course-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], 1)
        self.assertEqual(response.data[0]['name'], 'test course')

    def test_add_course_success(self):
        """ test to add course successfully"""
        self.get_logged_in_admin()
        course_data = {"name": "course 1", "description": "test description", "start_date": "2024-03-15"}
        response = self.client.post(reverse('course-list'), course_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["name"], "course 1")
        self.assertEqual(response.data["end_date"], '2024-06-15')

    def test_add_course_fail_course_exists(self):
        self.add_course()
        response = self.client.post(reverse('course-list'), self.course_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(str(response.data['name'][0]), 'course with this name already exists.')

    def test_add_course_fail_invalid_start_date(self):
        """test for adding course with invalid start date"""
        self.get_logged_in_admin()
        self.course_data['start_date'] = "2000-01-01"
        response = self.client.post(reverse('course-list'), self.course_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(str(response.data['start_date'][0]), "Start Date shouldn't be before today!")

    def test_add_course_fail_invalid_end_date(self):
        """test for adding course with invalid end date"""

        self.get_logged_in_admin()
        self.course_data['start_date'] = "2024-03-03"
        self.course_data['end_date'] = "2024-03-01"
        response = self.client.post(reverse('course-list'), self.course_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(str(response.data['non_field_errors'][0]), "End Date should be after Start Date!")

    def test_add_course_fail_invalid_price(self):
        self.get_logged_in_admin()
        self.course_data['price'] = -1
        response = self.client.post(reverse('course-list'), self.course_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(str(response.data['price'][0]), 'Ensure this value is greater than or equal to 0.')

    def test_get_a_course(self):
        """test to get a single course details"""

        self.add_course()
        response = self.client.get('/course/1/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], 1)
        self.assertEqual(response.data['name'], 'test course')

    def test_update_course_success(self):
        """test to update a course"""
        self.add_course()
        self.course_data['name'] = 'updated course'
        self.course_data['start_date'] = '2023-04-01'
        response = self.client.put('/course/1/', self.course_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'updated course')
        self.assertEqual(response.data['start_date'], '2023-04-01')

    def test_update_course_fail_invalid_end_date(self):
        """test to update a course with invalid end date"""
        self.add_course()
        self.course_data['end_date'] = '2000-01-01'
        response = self.client.put('/course/1/', self.course_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(str(response.data['non_field_errors'][0]), 'End Date should be after Start Date!')

    def test_update_course_fail_invalid_start_date(self):
        """test to update a course with invalid start date"""
        self.add_course()
        self.course_data['start_date'] = '2025-07-01'
        response = self.client.put('/course/1/', self.course_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(str(response.data[0]), 'Start Date should be before End Date!')

    def test_update_course_fail_invalid_price(self):
        """test to update a course with invalid start date"""
        self.add_course()
        self.course_data['price'] = "abc"
        response = self.client.put('/course/1/', self.course_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(str(response.data['price'][0]), 'A valid number is required.')

    def test_delete_course(self):
        """test to delete course"""
        self.add_course()
        response = self.client.delete('/course/1/')
        self.assertEqual(response.status_code, 204)
