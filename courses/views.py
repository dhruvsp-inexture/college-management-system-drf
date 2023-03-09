from django.shortcuts import render
from rest_framework import viewsets
from .models import Course
from .serializers import CourseSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from college_management.permissions import UserTypePermission


class CourseModelViewSet(viewsets.ModelViewSet):
    """CRUD for courses"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    authentication_classes = [JWTAuthentication]
    allowed_user_types = ['A']
    permission_classes = [UserTypePermission]
