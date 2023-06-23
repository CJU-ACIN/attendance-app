from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_num = models.CharField(max_length=20)
    qr_code = models.ImageField(upload_to='qr_student/')


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_num = models.CharField(max_length=20)
    qr_code = models.ImageField(upload_to='qr_teacher/')
