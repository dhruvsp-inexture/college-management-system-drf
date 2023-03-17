from student.models import StudentCourseMapping


class TestStudentCourseMappingModel:
    def test_fields(self):
        student_course_mapping = StudentCourseMapping.objects.create(
            student_id=3, course_id=14
        )
        assert student_course_mapping.student.email == 'student@gmail.com'
        assert student_course_mapping.course.name == 'course13'

    def test_str_method(self):
        student_course_mapping_obj = StudentCourseMapping.objects.get(
            student_id=3, course_id=3
        )
        assert str(student_course_mapping_obj) == 'testyy learns test12345678'



