from rest_framework import viewsets, generics, status
from rest_framework.response import Response

from .models import MyUser
from .serializers import UserCreateSerializer, UserUpdateSerializer, ChangePasswordSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from college_management.permissions import UserUpdatePermission, AdminOnly


class UserModelViewSet(viewsets.ModelViewSet):
    """CRUD for Users"""
    queryset = MyUser.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [AdminOnly | UserUpdatePermission]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        else:
            return UserUpdateSerializer


class UserChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Password changed successfully."})
