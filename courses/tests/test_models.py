from courses.models import Course


class TestCourseModel:
    def test_fields(self):
        course = Course.objects.create(
            name="test course model",
            description="test description",
            start_date="2025-05-05",
            end_date="2025-07-07",
            price=100
        )
        assert course.name == "test course model"
        assert course.description == "test description"
        assert course.start_date == "2025-05-05"
        assert course.end_date == "2025-07-07"
        assert course.price == 100

    def test_str_method(self):
        course_obj = Course.objects.get(name="course1")
        assert str(course_obj) == 'course1'