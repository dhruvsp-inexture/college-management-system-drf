import glob
from django.core.management import call_command
import pytest
from rest_framework.test import APITestCase, APIClient


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def load_initial_data():
    call_command('loaddata', glob.glob('fixtures/*'))


@pytest.fixture(autouse=True)
def autouse_db(db, load_initial_data):
    """This will allow all testcases to access database"""
    pass


@pytest.fixture
def test_admin_email():
    return "admin@gmail.com"


@pytest.fixture
def test_admin_password():
    return "admin"


@pytest.fixture
def test_student_email():
    return "student@gmail.com"


@pytest.fixture
def test_student_password():
    return "pass@123"


@pytest.fixture
def test_faculty_email():
    return "faculty@gmail.com"


@pytest.fixture
def test_faculty_password():
    return "pass@123"


@pytest.fixture
def get_logged_in_admin(client, test_admin_email, test_admin_password):
    """fixture to get logged in admin"""
    login_response = client.post('/gettoken/', data={"email": test_admin_email, "password": test_admin_password})
    # set bearer token for authentication
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + login_response.data.get('access'))
    return login_response


@pytest.fixture
def get_logged_in_user(client):
    """fixture to get logged in user"""

    def _get_logged_in_user(email, password):
        login_response = client.post('/gettoken/', data={"email": email, "password": password})
        # set bearer token for authentication
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + login_response.data.get('access'))
        return login_response

    return _get_logged_in_user
