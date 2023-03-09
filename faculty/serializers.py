from rest_framework import serializers
from admin_user.models import FacultyCourseMapping
from admin_user.serializers import FacultyCourseMappingSerializer
from courses.serializers import CourseSerializer
from student.models import StudentCourseMapping
from users.serializers import UserUpdateSerializer


class ShowAssignedCoursesSerializer(serializers.ModelSerializer):
    course = CourseSerializer()

    class Meta:
        model = FacultyCourseMapping
        fields = ['course']


class GradeStudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = StudentCourseMapping
        fields = '__all__'
