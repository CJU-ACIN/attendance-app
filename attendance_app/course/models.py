from django.db import models
from user.models import Client


# Create your models here.
class Division(models.Model):
    name = models.CharField(max_length=50)


class Course(models.Model):
    teacher_id = models.ForeignKey(Client, on_delete=models.CASCADE)
    division_name = models.CharField(max_length=50)
    course_name = models.CharField(max_length=50)
    start_date = models.DateField()
    start_at = models.TimeField()
    minute = models.IntegerField()


class ClassAttend(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    student_id = models.ForeignKey(Client, on_delete=models.CASCADE)
    start_at = models.TimeField()
    end_at = models.TimeField()

