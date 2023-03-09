from rest_framework import generics
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from admin_user.models import FacultyCourseMapping
from admin_user.serializers import FacultyCourseMappingSerializer
from college_management.permissions import FacultyOnly
from faculty.serializers import ShowAssignedCoursesSerializer


class ShowAssignedCoursesView(generics.ListAPIView):
    queryset = FacultyCourseMapping.objects.all()
    serializer_class = FacultyCourseMappingSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [FacultyOnly]

    def get(self, request, *args, **kwargs):
        assigned_courses = self.get_queryset(faculty_id=request.user.id)
        serializer = ShowAssignedCoursesSerializer(assigned_courses, many=True)
        return Response(serializer.data)

    def get_queryset(self, *args, **kwargs):
        assigned_courses = FacultyCourseMapping.objects.filter(faculty=kwargs.get('faculty_id'))
        return assigned_courses

