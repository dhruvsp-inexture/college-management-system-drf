from rest_framework import generics, status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
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


class MyStudentGradeView(generics.ListAPIView):
    student_mappings = StudentCourseMapping.objects.all()
    serializer_class = GradeStudentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [FacultyOnly]

    def get_queryset(self, *args, **kwargs):
        faculty_mappings = FacultyCourseMapping.objects.filter(faculty_id=self.request.user.id)
        students_to_grade = self.student_mappings.filter(course__in=faculty_mappings.values('course'))
        return students_to_grade


class GradeStudentView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [FacultyOnly]

    def put(self, request):
        try:
            student_to_grade = StudentCourseMapping.objects.get(student=request.data.get('student'),
                                                                   course=request.data.get('course'))
            serializer = GradeStudentSerializer(instance=student_to_grade, data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                data = {"message": "Grade Updated Successfully", "status_code": status.HTTP_204_NO_CONTENT}
                return Response(data=data, status=status.HTTP_204_NO_CONTENT)
            else:
                data = {"error": serializer.errors, "status_code": 400}
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        except StudentCourseMapping.DoesNotExist:
            data = {"error": "Data not found", "status_code": 404}
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            data = {"error": "Bad Request", "status_code": 400}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


