from datetime import date
from rest_framework import serializers
from admin_user.models import FacultyCourseMapping
from courses.models import Course
from courses.serializers import CourseSerializer
from student.models import StudentCourseMapping


class ShowAssignedCoursesSerializer(serializers.ModelSerializer):
    course = CourseSerializer()

    class Meta:
        model = FacultyCourseMapping
        fields = ['course']


class GradeStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentCourseMapping
        fields = '__all__'

    def validate(self, request):
        course_obj = Course.objects.get(id=request.get('course').id)
        if course_obj.end_date > date.today():
            raise serializers.ValidationError(
                f"Course has not ended yet. It will end on {course_obj.end_date}. Grade can only be assigned after course has ended.")
        if not FacultyCourseMapping.objects.filter(faculty=self.context['request'].user.id, course=request.get('course')).exists():
            raise serializers.ValidationError("You are not assigned this course so you cannot grade this student.")
        return request

    def validate_grade(self, value):
        if value not in ['A', 'B', 'C', 'D', 'F']:
            raise serializers.ValidationError(
                "Grade must be one of A(Excellent), B(Good), C(Satisfactory), D(Poor), F(Fail).")
        return value

    def update(self, instance, validated_data):
        instance.grade = validated_data.get('grade')
        instance.save()
        return instance
