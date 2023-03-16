from admin_user.models import FacultyCourseMapping


class TestFacultyCourseMappingModel:

    def test_fields(self):
        faculty_course_mapping = FacultyCourseMapping.objects.create(course_id=13, faculty_id=12)
        assert faculty_course_mapping.faculty.first_name == 'test'
        assert faculty_course_mapping.course.name == 'course12'

    def test_str_method(self):
        faculty_course_mapping_obj = FacultyCourseMapping.objects.get(faculty=12, course=3)
        assert str(faculty_course_mapping_obj) == 'test teaches test12345678'