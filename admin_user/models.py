from django.db import models
from courses.models import Course
from users.models import MyUser


class FacultyCourseMapping(models.Model):
    faculty = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('course', 'faculty')

    def __str__(self):
        return f'{self.faculty.first_name} teaches {self.course.name}'
