from django.db import models
from courses.models import Course
from users.models import MyUser


class StudentCourseMapping(models.Model):
    student = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f'{self.student.first_name} learns {self.course.name}'
