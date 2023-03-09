from rest_framework import viewsets, generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from college_management.permissions import UserTypePermission
from .models import FacultyCourseMapping
from .serializers import FacultyCourseMappingSerializer


class AssignCourseToFacultyView(viewsets.ModelViewSet):
    queryset = FacultyCourseMapping.objects.all()
    serializer_class = FacultyCourseMappingSerializer
    authentication_classes = [JWTAuthentication]
    allowed_user_types = ['A']
    permission_classes = [UserTypePermission]
