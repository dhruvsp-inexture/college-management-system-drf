from rest_framework import serializers
from courses.serializers import CourseSerializer
from .models import StudentCourseMapping


class StudentCourseMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentCourseMapping
        fields = ['id', 'student', 'course']


class StudentCourseGetSerializer(serializers.ModelSerializer):
    course = CourseSerializer()

    class Meta:
        model = StudentCourseMapping
        fields = ['id', 'course']
