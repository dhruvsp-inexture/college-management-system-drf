from rest_framework.test import APITestCase, APIClient
from django.urls import reverse

from users.models import MyUser


class TestSetUp(APITestCase):

    @classmethod
    def setUpTestData(cls):
        # Create a superuser
        cls.superuser = MyUser.objects.create_superuser(email='admin@example.com',
                                                        password='password', user_type="A")

    def setUp(self):
        super().setUp()
        self.client = APIClient()
        self.login_url = reverse('token_obtain_pair')
        self.register_url = reverse('user-list')

        self.admin_login_data = {
            "email": 'admin@example.com',
            "password": 'password'
        }
        self.user_data = {
            "email": "testuser@gmail.com",
            "first_name": "test",
            "last_name": "user",
            "address": "dont know",
            "phone_number": "+919393939349",
            "password": "pass@123",
            "user_type": "S"
        }

        self.course_data = {"name": "test course", "description": "test description"}

    def get_logged_in_admin(self):
        """
        Get logged in admin.
        """
        login_response = self.client.post(self.login_url, self.admin_login_data)
        # set bearer token for authentication
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + login_response.data.get('access'))
        return login_response

    def get_logged_in_student(self):
        """
        Get logged in student
        """
        student_data = {"email": "student@gmail.com", "password": "pass@123", "user_type": "S", "first_name": "student"}
        self.get_logged_in_admin()
        self.client.post(self.register_url, student_data)
        login_response = self.client.post(self.login_url, {"email": "student@gmail.com", "password": "pass@123"})
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + login_response.data.get('access'))
        return login_response

    def add_course(self):
        """
        add a course
        """
        self.get_logged_in_admin()
        response = self.client.post(reverse('course-list'), self.course_data)
        return response

    def tearDown(self):
        return super().tearDown()
