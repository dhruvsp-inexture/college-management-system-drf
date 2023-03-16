from django.urls import reverse
from courses.models import Course
from tests.test_setup import TestSetUp


class TestUsers(TestSetUp):
    def test_get_assigned_course(self):
        """test to get assigned course of the faculty"""
        self.add_course()
        self.add_faculty()
        assign_course_data = {'course': 1, 'faculty': 2}
        self.client.post(reverse('assign_course-list'), assign_course_data)
        self.get_logged_in_faculty()
        response = self.client.get(reverse('show-course'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['course']['id'], 1)
        self.assertEqual(response.data[0]['course']['name'], 'test course')

    def test_grade_student_success(self):
        """test to grade student by faculty"""
        self.test_get_assigned_course()
        self.get_logged_in_student()
        enroll_course_data = {"course": 1}
        self.client.post(reverse('enroll-course'), enroll_course_data)
        self.get_logged_in_faculty()
        Course.objects.filter(id=1).update(start_date="2023-03-13", end_date="2023-03-14")
        grade_student_data = {"student": 3, "course": 1, "grade": "A"}
        response = self.client.put(reverse('grade-student'), grade_student_data)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data['message'], 'Grade Updated Successfully')

    def test_grade_student_fail_grade_invalid_choice(self):
        """test to grade student by faculty where grade is invalid"""
        self.test_get_assigned_course()
        self.get_logged_in_student()
        enroll_course_data = {"course": 1}
        self.client.post(reverse('enroll-course'), enroll_course_data)
        self.get_logged_in_faculty()
        Course.objects.filter(id=1).update(start_date="2023-03-13", end_date="2023-03-14")
        grade_student_data = {"student": 3, "course": 1, "grade": "ABC"}
        response = self.client.put(reverse('grade-student'), grade_student_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(str(response.data['error']['grade'][0]), '"ABC" is not a valid choice.')

    def test_grade_student_fail_course_not_ended(self):
        """test to grade student by faculty where course has not ended yet"""
        self.test_get_assigned_course()
        self.get_logged_in_student()
        enroll_course_data = {"course": 1}
        self.client.post(reverse('enroll-course'), enroll_course_data)
        self.get_logged_in_faculty()
        grade_student_data = {"student": 3, "course": 1, "grade": "A"}
        response = self.client.put(reverse('grade-student'), grade_student_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(str(response.data['error']['non_field_errors'][0]),
                         'Course has not ended yet. It will end on 2023-06-15. Grade can only be assigned after course has ended.')

    def test_grade_student_fail_not_found(self):
        """test to grade student which is not found"""
        self.get_logged_in_faculty()
        grade_student_data = {"student": 3, "course": 1, "grade": "A"}
        response = self.client.put(reverse('grade-student'), grade_student_data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['error'], 'Data not found')

    def test_grade_student_fail_bad_request(self):
        """test to grade student which is not found"""
        self.get_logged_in_faculty()
        grade_student_data = {"student": "abc", "course": "def", "grade": "A"}
        response = self.client.put(reverse('grade-student'), grade_student_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['error'], 'Bad Request')

    def test_get_students(self):
        """test to get students for grading by faculty"""
        self.test_grade_student_success()
        response = self.client.get(reverse('view-grades'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['id'], 1)
        self.assertEqual(response.data[0]['grade'], 'A')
        self.assertEqual(response.data[0]['student'], 3)
        self.assertEqual(response.data[0]['course'], 1)
