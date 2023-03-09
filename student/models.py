from django.db import models
from courses.models import Course
from users.models import MyUser


class StudentCourseMapping(models.Model):
    GRADE_CHOICES = (
        ('A', 'Excellent'),
        ('B', 'Good'),
        ('C', 'Satisfactory'),
        ('D', 'Poor'),
        ('F', 'Fail')
    )
    student = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.CharField(max_length=1, choices=GRADE_CHOICES, null=True, blank=True)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f'{self.student.first_name} learns {self.course.name}'
