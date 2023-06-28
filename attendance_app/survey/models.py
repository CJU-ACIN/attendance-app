from django.db import models
from course.models import Course


# Create your models here.



class Survey(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    question_num = models.IntegerField()
    question = models.CharField(max_length=100)


class SurveyReply(models.Model):
    survey_id = models.ForeignKey(Survey, on_delete=models.CASCADE)
    reply_num = models.IntegerField()
    reply = models.TextField()


# 사용 안함
class FixedSurveyReply(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    reply1 = models.CharField(max_length=300)
    reply2 = models.CharField(max_length=300)
    reply3 = models.CharField(max_length=300)