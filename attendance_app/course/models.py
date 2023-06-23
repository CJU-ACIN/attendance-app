from django.db import models
from user.models import Teacher, Student


# Create your models here.
class Course(models.Model):
    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=50)
    start_at = models.TimeField()
    minute = models.IntegerField()


class ClassAttend(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    student_id = models.ForeignKey(Student, on_delete=models.Model)
    start_at = models.TimeField()
    end_at = models.TimeField()

