from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=10)
    birth_date = models.CharField(max_length=6)
    gender = models.CharField(max_length=10)
    division = models.CharField(max_length=30)
    qr_code = models.ImageField(upload_to='qr_student/')


