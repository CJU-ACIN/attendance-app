from django.db import models
from user.models import Student


# Create your models here.



class Course(models.Model):
    teacher_id = models.CharField(max_length=20)
    division_name = models.CharField(max_length=50)
    course_name = models.CharField(max_length=50)
    start_date = models.DateField()
    start_at = models.TimeField()
    minute = models.IntegerField()


class ClassAttend(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    start_at = models.TimeField()
    end_at = models.TimeField()

