from rest_framework import serializers
from admin_user.models import FacultyCourseMapping
from courses.serializers import CourseSerializer


class ShowAssignedCoursesSerializer(serializers.ModelSerializer):
    course = CourseSerializer()

    class Meta:
        model = FacultyCourseMapping
        fields = ['course']
