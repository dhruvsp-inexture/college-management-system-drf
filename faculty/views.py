from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from admin_user.models import FacultyCourseMapping
from admin_user.serializers import FacultyCourseMappingSerializer
from college_management.permissions import FacultyOnly
from faculty.serializers import ShowAssignedCoursesSerializer, GradeStudentSerializer
from student.models import StudentCourseMapping


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


class GradeStudentView(viewsets.ModelViewSet):
    student_mappings = StudentCourseMapping.objects.all()
    serializer_class = GradeStudentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [FacultyOnly]

    def get_queryset(self, *args, **kwargs):
        faculty_mappings = FacultyCourseMapping.objects.filter(faculty_id=self.request.user.id)
        students_to_grade = self.student_mappings.filter(course__in=faculty_mappings.values('course'))
        return students_to_grade

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'students_to_grade': self.get_queryset()})
        return context