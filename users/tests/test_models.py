from users.models import MyUser


class TestUserModel:
    def test_fields(self):
        """test for checking fields in user model"""
        user = MyUser.objects.create(
            email='testuser@example.com',
            first_name='Test',
            last_name='User',
            address='123 Test St',
            user_type='S',
            phone_number='555-1234'
        )
        assert user.email == 'testuser@example.com'
        assert user.first_name == 'Test'
        assert user.last_name == 'User'
        assert user.address == '123 Test St'
        assert user.user_type == 'S'
        assert user.phone_number == '555-1234'
        assert user.is_active
        assert user.is_admin == False

    def test_str_method(self):
        obj = MyUser.objects.get(email='admin@gmail.com')
        assert str(obj) == 'admin@gmail.com'

