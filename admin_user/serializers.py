from django.core.exceptions import NON_FIELD_ERRORS
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from users.models import MyUser
from .models import FacultyCourseMapping


class FacultyCourseMappingSerializer(serializers.ModelSerializer):
    # course = CourseSerializer(read_only=True)
    # faculty = UserCreateSerializer(read_only=True)

    class Meta:
        model = FacultyCourseMapping
        fields = ['id', 'course', 'faculty']

    def validate(self, validated_data):
        is_faculty = MyUser.objects.filter(id=validated_data['faculty'].id, user_type='F')
        if is_faculty:
            return validated_data
        raise serializers.ValidationError("You can only assign course to faculty!")
