"""college_management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.conf import settings
# settings.configure(DJANGO_SETTINGS_MODULE='college_management_system.settings')
from django.contrib import admin
from django.contrib import admin
from django.urls import path, include
from courses import views as courses_views
from student.views import EnrollCourseView, DropCourseView
from users import views as user_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework.routers import DefaultRouter
from admin_user import views as admin_views
from admin_user.views import AssignCourseToFacultyView
from faculty.views import ShowAssignedCoursesView

router = DefaultRouter()
router.register('course', courses_views.CourseModelViewSet, basename='course')
router.register('user', user_views.UserModelViewSet, basename='user')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('gettoken/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refreshtoken/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verifytoken/', TokenVerifyView.as_view(), name='token_verify'),
    path('change-password/', user_views.UserChangePasswordView.as_view(), name='change_password'),
    path('reset-password/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('assign-course/', AssignCourseToFacultyView.as_view({'get': 'list', 'post': 'create'}),
         name='assign_course-list'),
    path('assign-course/<int:pk>/',
         AssignCourseToFacultyView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
         name='assign_course-detail'),
    path('show-course/', ShowAssignedCoursesView.as_view(), name='show-course'),
    path('enroll-course/', EnrollCourseView.as_view(), name='enroll-course'),
    path('drop-course/', DropCourseView.as_view(), name='drop-course')
]
