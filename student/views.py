from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from college_management.permissions import UserTypePermission
from student.models import StudentCourseMapping
from student.serializers import StudentCourseMappingSerializer, StudentCourseGetSerializer
from rest_framework import generics, status
import json


class EnrollCourseView(generics.ListCreateAPIView):
    queryset = StudentCourseMapping.objects.all()
    serializer_class = StudentCourseMappingSerializer
    authentication_classes = [JWTAuthentication]
    allowed_user_types = ['S']
    permission_classes = [UserTypePermission]

    def get(self, request, *args, **kwargs):
        queryset = self.queryset.filter(student_id=request.user.id)
        serializer_data = StudentCourseGetSerializer(queryset, many=True)
        return Response(serializer_data.data)

    def post(self, request, *args, **kwargs):
        request.data.update({'student': request.user.id})
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class DropCourseView(APIView):
    serializer_class = StudentCourseMappingSerializer
    authentication_classes = [JWTAuthentication]
    allowed_user_types = ['S']
    permission_classes = [UserTypePermission]

    def delete(self, request):
        try:
            course_id = json.loads(request.body).get('course')
            enrolled_course = StudentCourseMapping.objects.get(student_id=request.user.id, course_id=course_id)
        except StudentCourseMapping.DoesNotExist:
            data = {"error": "Data not found", "status_code": 404}
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)

        enrolled_course.delete()
        data = {"error": "Successfully deleted", "status_code": 204}
        return Response(data=data, status=status.HTTP_204_NO_CONTENT)

